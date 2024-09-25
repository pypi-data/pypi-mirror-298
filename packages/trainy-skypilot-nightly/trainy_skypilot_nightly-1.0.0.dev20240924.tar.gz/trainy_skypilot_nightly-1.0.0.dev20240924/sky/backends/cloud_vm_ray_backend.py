"""Backend: runs on cloud virtual machines, managed by Ray."""
import copy
import enum
import functools
import getpass
import inspect
import json
import math
import os
import pathlib
import re
import shlex
import signal
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
import typing
from typing import (Any, Callable, Dict, Iterable, List, Optional, Set, Tuple,
                    Union)

import colorama
import filelock

import sky
from sky import backends
from sky import cloud_stores
from sky import clouds
from sky import exceptions
from sky import global_user_state
from sky import jobs as managed_jobs
from sky import optimizer
from sky import provision as provision_lib
from sky import resources as resources_lib
from sky import serve as serve_lib
from sky import sky_logging
from sky import status_lib
from sky import task as task_lib
from sky.backends import backend_utils
from sky.backends import wheel_utils
from sky.clouds import service_catalog
from sky.clouds.utils import gcp_utils
from sky.data import data_utils
from sky.data import storage as storage_lib
from sky.provision import common as provision_common
from sky.provision import instance_setup
from sky.provision import metadata_utils
from sky.provision import provisioner
from sky.skylet import autostop_lib
from sky.skylet import constants
from sky.skylet import job_lib
from sky.skylet import log_lib
from sky.usage import usage_lib
from sky.utils import accelerator_registry
from sky.utils import command_runner
from sky.utils import common_utils
from sky.utils import controller_utils
from sky.utils import log_utils
from sky.utils import resources_utils
from sky.utils import rich_utils
from sky.utils import subprocess_utils
from sky.utils import timeline
from sky.utils import ux_utils

if typing.TYPE_CHECKING:
    from sky import dag

Path = str

SKY_REMOTE_APP_DIR = backend_utils.SKY_REMOTE_APP_DIR
SKY_REMOTE_WORKDIR = constants.SKY_REMOTE_WORKDIR

logger = sky_logging.init_logger(__name__)

_PATH_SIZE_MEGABYTES_WARN_THRESHOLD = 256

# Timeout (seconds) for provision progress: if in this duration no new nodes
# are launched, abort and failover.
_NODES_LAUNCHING_PROGRESS_TIMEOUT = {
    clouds.AWS: 90,
    clouds.Azure: 90,
    clouds.GCP: 240,
    clouds.Lambda: 300,
    clouds.IBM: 160,
    clouds.OCI: 300,
    clouds.Paperspace: 600,
    clouds.Kubernetes: 300,
    clouds.Vsphere: 240,
}

# Time gap between retries after failing to provision in all possible places.
# Used only if --retry-until-up is set.
_RETRY_UNTIL_UP_INIT_GAP_SECONDS = 30

# The maximum retry count for fetching IP address.
_FETCH_IP_MAX_ATTEMPTS = 3

_TEARDOWN_FAILURE_MESSAGE = (
    f'\n{colorama.Fore.RED}Failed to terminate '
    '{cluster_name}. {extra_reason}'
    'If you want to ignore this error and remove the cluster '
    'from the status table, use `sky down --purge`.'
    f'{colorama.Style.RESET_ALL}\n'
    '**** STDOUT ****\n'
    '{stdout}\n'
    '**** STDERR ****\n'
    '{stderr}')

_TEARDOWN_PURGE_WARNING = (
    f'{colorama.Fore.YELLOW}'
    'WARNING: Received non-zero exit code from {reason}. '
    'Make sure resources are manually deleted.\n'
    'Details: {details}'
    f'{colorama.Style.RESET_ALL}')

_RSYNC_NOT_FOUND_MESSAGE = (
    '`rsync` command is not found in the specified image. '
    'Please use an image with rsync installed.')

_TPU_NOT_FOUND_ERROR = 'ERROR: (gcloud.compute.tpus.delete) NOT_FOUND'

_CTRL_C_TIP_MESSAGE = ('INFO: Tip: use Ctrl-C to exit log streaming '
                       '(task will not be killed).')

_MAX_RAY_UP_RETRY = 5

# Number of retries for getting zones.
_MAX_GET_ZONE_RETRY = 3

_JOB_ID_PATTERN = re.compile(r'Job ID: ([0-9]+)')

# Path to the monkey-patched ray up script.
# We don't do import then __file__ because that script needs to be filled in
# (so import would fail).
_RAY_UP_WITH_MONKEY_PATCHED_HASH_LAUNCH_CONF_PATH = (
    pathlib.Path(sky.__file__).resolve().parent / 'backends' /
    'monkey_patches' / 'monkey_patch_ray_up.py')

# The maximum size of a command line arguments is 128 KB, i.e. the command
# executed with /bin/sh should be less than 128KB.
# https://github.com/torvalds/linux/blob/master/include/uapi/linux/binfmts.h
#
# If a user have very long run or setup commands, the generated command may
# exceed the limit, as we directly include scripts in job submission commands.
# If the command is too long, we instead write it to a file, rsync and execute
# it.
#
# We use 120KB as a threshold to be safe for other arguments that
# might be added during ssh.
_MAX_INLINE_SCRIPT_LENGTH = 120 * 1024


def _is_command_length_over_limit(command: str) -> bool:
    """Check if the length of the command exceeds the limit.

    We calculate the length of the command after quoting the command twice as
    when it is executed by the CommandRunner, the command will be quoted twice
    to ensure the correctness, which will add significant length to the command.
    """

    quoted_length = len(shlex.quote(shlex.quote(command)))
    return quoted_length > _MAX_INLINE_SCRIPT_LENGTH


def _get_cluster_config_template(cloud):
    cloud_to_template = {
        clouds.AWS: 'aws-ray.yml.j2',
        clouds.Azure: 'azure-ray.yml.j2',
        clouds.Cudo: 'cudo-ray.yml.j2',
        clouds.GCP: 'gcp-ray.yml.j2',
        clouds.Lambda: 'lambda-ray.yml.j2',
        clouds.IBM: 'ibm-ray.yml.j2',
        clouds.SCP: 'scp-ray.yml.j2',
        clouds.OCI: 'oci-ray.yml.j2',
        clouds.Paperspace: 'paperspace-ray.yml.j2',
        clouds.RunPod: 'runpod-ray.yml.j2',
        clouds.Kubernetes: 'kubernetes-ray.yml.j2',
        clouds.Vsphere: 'vsphere-ray.yml.j2',
        clouds.Fluidstack: 'fluidstack-ray.yml.j2'
    }
    return cloud_to_template[type(cloud)]


def write_ray_up_script_with_patched_launch_hash_fn(
    cluster_config_path: str,
    ray_up_kwargs: Dict[str, bool],
) -> str:
    """Writes a Python script that runs `ray up` with our launch hash func.

    Our patched launch hash has one difference from the non-patched version: it
    does not include any `ssh_proxy_command` under `auth` as part of the hash
    calculation.
    """
    with open(_RAY_UP_WITH_MONKEY_PATCHED_HASH_LAUNCH_CONF_PATH,
              'r',
              encoding='utf-8') as f:
        ray_up_no_restart_script = f.read().format(
            ray_yaml_path=repr(cluster_config_path),
            ray_up_kwargs=ray_up_kwargs)
    with tempfile.NamedTemporaryFile('w',
                                     prefix='skypilot_ray_up_',
                                     suffix='.py',
                                     delete=False) as f:
        f.write(ray_up_no_restart_script)
        logger.debug(f'`ray up` script: {f.name}')
    return f.name


class RayCodeGen:
    """Code generator of a Ray program that executes a sky.Task.

    Usage:

      >> codegen = RayCodegen()
      >> codegen.add_prologue()

      >> codegen.add_ray_task(...)
      >> codegen.add_ray_task(...)

      >> codegen.add_epilogue()
      >> code = codegen.build()
    """

    def __init__(self):
        # Code generated so far, to be joined via '\n'.
        self._code = []
        # Guard method calling order.
        self._has_prologue = False
        self._has_epilogue = False

        # For n nodes gang scheduling.
        self._has_gang_scheduling = False
        self._num_nodes = 0

        self._has_register_run_fn = False

        # job_id
        # Job ID is used to identify the job (also this generated code).
        # It is a int automatically generated by the DB on the cluster
        # and monotonically increasing starting from 1.
        # To generate the job ID, we use the following logic:
        #   code = job_lib.JobLibCodeGen.add_job(username,
        #                                              run_timestamp)
        #   job_id = get_output(run_on_cluster(code))
        self.job_id = None

    def add_prologue(self, job_id: int) -> None:
        assert not self._has_prologue, 'add_prologue() called twice?'
        self._has_prologue = True
        self.job_id = job_id
        # Should use 'auto' or 'ray://<internal_head_ip>:10001' rather than
        # 'ray://localhost:10001', or 'ray://127.0.0.1:10001', for public cloud.
        # Otherwise, ray will fail to get the placement group because of a bug
        # in ray job.
        ray_address = 'auto'
        self._code = [
            textwrap.dedent(f"""\
            import getpass
            import hashlib
            import io
            import os
            import pathlib
            import selectors
            import shlex
            import subprocess
            import sys
            import tempfile
            import textwrap
            import time
            from typing import Dict, List, Optional, Tuple, Union

            import ray
            import ray.util as ray_util

            from sky.skylet import autostop_lib
            from sky.skylet import constants
            from sky.skylet import job_lib
            from sky.utils import log_utils

            SKY_REMOTE_WORKDIR = {constants.SKY_REMOTE_WORKDIR!r}

            kwargs = dict()
            # Only set the `_temp_dir` to SkyPilot's ray cluster directory when
            # the directory exists for backward compatibility for the VM
            # launched before #1790.
            if os.path.exists({constants.SKY_REMOTE_RAY_TEMPDIR!r}):
                kwargs['_temp_dir'] = {constants.SKY_REMOTE_RAY_TEMPDIR!r}
            ray.init(
                address={ray_address!r},
                namespace='__sky__{job_id}__',
                log_to_driver=True,
                **kwargs
            )
            def get_or_fail(futures, pg) -> List[int]:
                \"\"\"Wait for tasks, if any fails, cancel all unready.\"\"\"
                returncodes = [1] * len(futures)
                # Wait for 1 task to be ready.
                ready = []
                # Keep invoking ray.wait if ready is empty. This is because
                # ray.wait with timeout=None will only wait for 10**6 seconds,
                # which will cause tasks running for more than 12 days to return
                # before becoming ready.
                # (Such tasks are common in serving jobs.)
                # Reference: https://github.com/ray-project/ray/blob/ray-2.9.3/python/ray/_private/worker.py#L2845-L2846
                while not ready:
                    ready, unready = ray.wait(futures)
                idx = futures.index(ready[0])
                returncodes[idx] = ray.get(ready[0])
                while unready:
                    if returncodes[idx] != 0:
                        for task in unready:
                            # ray.cancel without force fails to kill tasks.
                            # We use force=True to kill unready tasks.
                            ray.cancel(task, force=True)
                            # Use SIGKILL=128+9 to indicate the task is forcely
                            # killed.
                            idx = futures.index(task)
                            returncodes[idx] = 137
                        break
                    ready, unready = ray.wait(unready)
                    idx = futures.index(ready[0])
                    returncodes[idx] = ray.get(ready[0])
                # Remove the placement group after all tasks are done, so that
                # the next job can be scheduled on the released resources
                # immediately.
                ray_util.remove_placement_group(pg)
                sys.stdout.flush()
                return returncodes

            run_fn = None
            futures = []
            """),
            # FIXME: This is a hack to make sure that the functions can be found
            # by ray.remote. This should be removed once we have a better way to
            # specify dependencies for ray.
            inspect.getsource(log_lib._ProcessingArgs),  # pylint: disable=protected-access
            inspect.getsource(log_lib._handle_io_stream),  # pylint: disable=protected-access
            inspect.getsource(log_lib.process_subprocess_stream),
            inspect.getsource(log_lib.run_with_log),
            inspect.getsource(log_lib.make_task_bash_script),
            inspect.getsource(log_lib.add_ray_env_vars),
            inspect.getsource(log_lib.run_bash_command_with_log),
            'run_bash_command_with_log = ray.remote(run_bash_command_with_log)',
        ]
        # Currently, the codegen program is/can only be submitted to the head
        # node, due to using job_lib for updating job statuses, and using
        # autostop_lib here.
        self._code.append(
            # Use hasattr to handle backward compatibility.
            # TODO(zongheng): remove in ~1-2 minor releases (currently 0.2.x).
            textwrap.dedent("""\
              if hasattr(autostop_lib, 'set_last_active_time_to_now'):
                  autostop_lib.set_last_active_time_to_now()
            """))
        self._code += [
            f'job_lib.set_status({job_id!r}, job_lib.JobStatus.PENDING)',
        ]

    def add_gang_scheduling_placement_group_and_setup(
        self,
        num_nodes: int,
        resources_dict: Dict[str, float],
        stable_cluster_internal_ips: List[str],
        env_vars: Dict[str, str],
        setup_cmd: Optional[str] = None,
        setup_log_path: Optional[str] = None,
    ) -> None:
        """Create the gang scheduling placement group for a Task.

        cluster_ips_sorted is used to ensure that the SKY_NODE_RANK environment
        variable is assigned in a deterministic order whenever a new task is
        added.
        """
        assert self._has_prologue, (
            'Call add_prologue() before '
            'add_gang_scheduling_placement_group_and_setup().')
        self._has_gang_scheduling = True
        self._num_nodes = num_nodes

        bundles = [copy.copy(resources_dict) for _ in range(num_nodes)]
        # Set CPU to avoid ray hanging the resources allocation
        # for remote functions, since the task will request 1 CPU
        # by default.
        task_cpu_demand = resources_dict.pop('CPU')

        if resources_dict:
            assert len(resources_dict) == 1, (
                'There can only be one type of accelerator per instance. '
                f'Found: {resources_dict}.')
            acc_name, acc_count = list(resources_dict.items())[0]
            gpu_dict = {'GPU': acc_count}
            # gpu_dict should be empty when the accelerator is not GPU.
            # TODO(zongheng,zhanghao): an alternative is to start the remote
            # cluster with custom resource 'GPU': <n> even if the accelerator(s)
            # are not GPU. We opt for the current solution for now.
            if accelerator_registry.is_schedulable_non_gpu_accelerator(
                    acc_name):
                gpu_dict = {}
            for bundle in bundles:
                bundle.update({
                    # Set the GPU to avoid ray hanging the resources allocation
                    **gpu_dict,
                })

        self._code += [
            textwrap.dedent(f"""\
                pg = ray_util.placement_group({json.dumps(bundles)}, 'STRICT_SPREAD')
                plural = 's' if {num_nodes} > 1 else ''
                node_str = f'{num_nodes} node{{plural}}'

                message = {_CTRL_C_TIP_MESSAGE!r} + '\\n'
                message += f'INFO: Waiting for task resources on {{node_str}}. This will block if the cluster is full.'
                print(message,
                      flush=True)
                # FIXME: This will print the error message from autoscaler if
                # it is waiting for other task to finish. We should hide the
                # error message.
                ray.get(pg.ready())
                print('INFO: All task resources reserved.',
                      flush=True)
                """)
        ]

        job_id = self.job_id
        if setup_cmd is not None:
            setup_envs = env_vars.copy()
            setup_envs[constants.SKYPILOT_NUM_NODES] = str(num_nodes)
            self._code += [
                textwrap.dedent(f"""\
                setup_cmd = {setup_cmd!r}
                _SETUP_CPUS = 0.0001
                # The setup command will be run as a ray task with num_cpus=_SETUP_CPUS as the
                # requirement; this means Ray will set CUDA_VISIBLE_DEVICES to an empty string.
                # We unset it so that user setup command may properly use this env var.
                setup_cmd = 'unset CUDA_VISIBLE_DEVICES; ' + setup_cmd
                job_lib.set_status({job_id!r}, job_lib.JobStatus.SETTING_UP)

                # The schedule_step should be called after the job status is set to non-PENDING,
                # otherwise, the scheduler will think the current job is not submitted yet, and
                # skip the scheduling step.
                job_lib.scheduler.schedule_step()

                total_num_nodes = len(ray.nodes())
                setup_bundles = [{{"CPU": _SETUP_CPUS}} for _ in range(total_num_nodes)]
                setup_pg = ray.util.placement_group(setup_bundles, strategy='STRICT_SPREAD')
                setup_workers = [run_bash_command_with_log \\
                    .options(
                        name='setup',
                        num_cpus=_SETUP_CPUS,
                        scheduling_strategy=ray.util.scheduling_strategies.PlacementGroupSchedulingStrategy(
                            placement_group=setup_pg,
                            placement_group_bundle_index=i)
                    ) \\
                    .remote(
                        setup_cmd,
                        os.path.expanduser({setup_log_path!r}),
                        env_vars={setup_envs!r},
                        stream_logs=True,
                        with_ray=True,
                    ) for i in range(total_num_nodes)]
                setup_returncodes = get_or_fail(setup_workers, setup_pg)
                if sum(setup_returncodes) != 0:
                    job_lib.set_status({self.job_id!r}, job_lib.JobStatus.FAILED_SETUP)
                    # This waits for all streaming logs to finish.
                    time.sleep(1)
                    print('ERROR: {colorama.Fore.RED}Job {self.job_id}\\'s setup failed with '
                        'return code list:{colorama.Style.RESET_ALL}',
                        setup_returncodes,
                        flush=True)
                    # Need this to set the job status in ray job to be FAILED.
                    sys.exit(1)
                """)
            ]

        self._code.append(f'job_lib.set_job_started({self.job_id!r})')
        if setup_cmd is None:
            # Need to call schedule_step() to make sure the scheduler
            # schedule the next pending job.
            self._code.append('job_lib.scheduler.schedule_step()')

        # Export IP and node rank to the environment variables.
        self._code += [
            textwrap.dedent(f"""\
                @ray.remote
                def check_ip():
                    return ray.util.get_node_ip_address()
                gang_scheduling_id_to_ip = ray.get([
                    check_ip.options(
                            num_cpus={task_cpu_demand},
                            scheduling_strategy=ray.util.scheduling_strategies.PlacementGroupSchedulingStrategy(
                                placement_group=pg,
                                placement_group_bundle_index=i
                            )).remote()
                    for i in range(pg.bundle_count)
                ])
                print('INFO: Reserved IPs:', gang_scheduling_id_to_ip)

                cluster_ips_to_node_id = {{ip: i for i, ip in enumerate({stable_cluster_internal_ips!r})}}
                job_ip_rank_list = sorted(gang_scheduling_id_to_ip, key=cluster_ips_to_node_id.get)
                job_ip_rank_map = {{ip: i for i, ip in enumerate(job_ip_rank_list)}}
                job_ip_list_str = '\\n'.join(job_ip_rank_list)
                """),
        ]

    def register_run_fn(self, run_fn: str, run_fn_name: str) -> None:
        """Register the run function to be run on the remote cluster.

        Args:
            run_fn: The run function to be run on the remote cluster.
        """
        assert self._has_gang_scheduling, (
            'Call add_gang_scheduling_placement_group_and_setup() '
            'before register_run_fn().')
        assert not self._has_register_run_fn, (
            'register_run_fn() called twice?')
        self._has_register_run_fn = True

        self._code += [
            run_fn,
            f'run_fn = {run_fn_name}',
        ]

    def add_ray_task(self,
                     bash_script: Optional[str],
                     task_name: Optional[str],
                     ray_resources_dict: Dict[str, float],
                     log_dir: str,
                     env_vars: Optional[Dict[str, str]] = None,
                     gang_scheduling_id: int = 0) -> None:
        """Generates code for a ray remote task that runs a bash command."""
        assert self._has_gang_scheduling, (
            'Call add_gang_scheduling_placement_group_and_setup() before '
            'add_ray_task().')
        assert (not self._has_register_run_fn or
                bash_script is None), ('bash_script should '
                                       'be None when run_fn is registered.')
        task_cpu_demand = ray_resources_dict.pop('CPU')
        # Build remote_task.options(...)
        #   resources=...
        #   num_gpus=...
        options = []
        options.append(f'num_cpus={task_cpu_demand}')

        num_gpus = 0.0
        if ray_resources_dict:
            assert len(ray_resources_dict) == 1, (
                'There can only be one type of accelerator per instance. '
                f'Found: {ray_resources_dict}.')
            num_gpus = list(ray_resources_dict.values())[0]
            options.append(f'resources={json.dumps(ray_resources_dict)}')

            resources_key = list(ray_resources_dict.keys())[0]
            if not accelerator_registry.is_schedulable_non_gpu_accelerator(
                    resources_key):
                # `num_gpus` should be empty when the accelerator is not GPU.
                # FIXME: use a set of GPU types, instead of 'tpu' in the key.

                # Passing this ensures that the Ray remote task gets
                # CUDA_VISIBLE_DEVICES set correctly.  If not passed, that flag
                # would be force-set to empty by Ray.
                options.append(f'num_gpus={num_gpus}')
        options.append(
            'scheduling_strategy=ray.util.scheduling_strategies.PlacementGroupSchedulingStrategy('  # pylint: disable=line-too-long
            'placement_group=pg, '
            f'placement_group_bundle_index={gang_scheduling_id})')

        sky_env_vars_dict_str = [
            textwrap.dedent(f"""\
            sky_env_vars_dict = {{}}
            sky_env_vars_dict['{constants.SKYPILOT_NODE_IPS}'] = job_ip_list_str
            # Backward compatibility: Environment starting with `SKY_` is
            # deprecated. Remove it in v0.9.0.
            sky_env_vars_dict['SKY_NODE_IPS'] = job_ip_list_str
            sky_env_vars_dict['{constants.SKYPILOT_NUM_NODES}'] = len(job_ip_rank_list)
            """)
        ]

        if env_vars is not None:
            sky_env_vars_dict_str.extend(f'sky_env_vars_dict[{k!r}] = {v!r}'
                                         for k, v in env_vars.items())
        sky_env_vars_dict_str = '\n'.join(sky_env_vars_dict_str)

        options_str = ', '.join(options)
        logger.debug('Added Task with options: '
                     f'{options_str}')
        self._code += [
            sky_env_vars_dict_str,
            textwrap.dedent(f"""\
        script = {bash_script!r}
        if run_fn is not None:
            script = run_fn({gang_scheduling_id}, gang_scheduling_id_to_ip)


        if script is not None:
            sky_env_vars_dict['{constants.SKYPILOT_NUM_GPUS_PER_NODE}'] = {int(math.ceil(num_gpus))!r}
            # Backward compatibility: Environment starting with `SKY_` is
            # deprecated. Remove it in v0.9.0.
            sky_env_vars_dict['SKY_NUM_GPUS_PER_NODE'] = {int(math.ceil(num_gpus))!r}

            ip = gang_scheduling_id_to_ip[{gang_scheduling_id!r}]
            rank = job_ip_rank_map[ip]

            if len(cluster_ips_to_node_id) == 1: # Single-node task on single-node cluter
                name_str = '{task_name},' if {task_name!r} != None else 'task,'
                log_path = os.path.expanduser(os.path.join({log_dir!r}, 'run.log'))
            else: # Single-node or multi-node task on multi-node cluster
                idx_in_cluster = cluster_ips_to_node_id[ip]
                if cluster_ips_to_node_id[ip] == 0:
                    node_name = 'head'
                else:
                    node_name = f'worker{{idx_in_cluster}}'
                name_str = f'{{node_name}}, rank={{rank}},'
                log_path = os.path.expanduser(os.path.join({log_dir!r}, f'{{rank}}-{{node_name}}.log'))
            sky_env_vars_dict['{constants.SKYPILOT_NODE_RANK}'] = rank
            # Backward compatibility: Environment starting with `SKY_` is
            # deprecated. Remove it in v0.9.0.
            sky_env_vars_dict['SKY_NODE_RANK'] = rank

            sky_env_vars_dict['SKYPILOT_INTERNAL_JOB_ID'] = {self.job_id}
            # Backward compatibility: Environment starting with `SKY_` is
            # deprecated. Remove it in v0.9.0.
            sky_env_vars_dict['SKY_INTERNAL_JOB_ID'] = {self.job_id}

            futures.append(run_bash_command_with_log \\
                    .options(name=name_str, {options_str}) \\
                    .remote(
                        script,
                        log_path,
                        env_vars=sky_env_vars_dict,
                        stream_logs=True,
                        with_ray=True,
                    ))""")
        ]

    def add_epilogue(self) -> None:
        """Generates code that waits for all tasks, then exits."""
        assert self._has_prologue, 'Call add_prologue() before add_epilogue().'
        assert not self._has_epilogue, 'add_epilogue() called twice?'
        self._has_epilogue = True

        self._code += [
            textwrap.dedent(f"""\
            returncodes = get_or_fail(futures, pg)
            if sum(returncodes) != 0:
                job_lib.set_status({self.job_id!r}, job_lib.JobStatus.FAILED)
                # Schedule the next pending job immediately to make the job
                # scheduling more efficient.
                job_lib.scheduler.schedule_step()
                # This waits for all streaming logs to finish.
                time.sleep(0.5)
                reason = ''
                # 139 is the return code of SIGSEGV, i.e. Segmentation Fault.
                if any(r == 139 for r in returncodes):
                    reason = '(likely due to Segmentation Fault)'
                print('ERROR: {colorama.Fore.RED}Job {self.job_id} failed with '
                      'return code list:{colorama.Style.RESET_ALL}',
                      returncodes,
                      reason,
                      flush=True)
                # Need this to set the job status in ray job to be FAILED.
                sys.exit(1)
            else:
                job_lib.set_status({self.job_id!r}, job_lib.JobStatus.SUCCEEDED)
                # Schedule the next pending job immediately to make the job
                # scheduling more efficient.
                job_lib.scheduler.schedule_step()
                # This waits for all streaming logs to finish.
                time.sleep(0.5)
            """)
        ]

    def build(self) -> str:
        """Returns the entire generated program."""
        assert self._has_epilogue, 'Call add_epilogue() before build().'
        return '\n'.join(self._code)


class GangSchedulingStatus(enum.Enum):
    """Enum for gang scheduling status."""
    CLUSTER_READY = 0
    GANG_FAILED = 1
    HEAD_FAILED = 2


def _add_to_blocked_resources(blocked_resources: Set['resources_lib.Resources'],
                              resources: 'resources_lib.Resources') -> None:
    # If the resources is already blocked by blocked_resources, we don't need to
    # add it again to avoid duplicated entries.
    for r in blocked_resources:
        if resources.should_be_blocked_by(r):
            return
    blocked_resources.add(resources)


class FailoverCloudErrorHandlerV1:
    """Handles errors during provisioning and updates the blocked_resources.

    Deprecated: Newly added cloud should use the FailoverCloudErrorHandlerV2,
    which is more robust by parsing the errors raised by the cloud's API in a
    more structured way, instead of directly based on the stdout and stderr.
    """

    @staticmethod
    def _handle_errors(stdout: str, stderr: str,
                       is_error_str_known: Callable[[str], bool]) -> List[str]:
        stdout_splits = stdout.split('\n')
        stderr_splits = stderr.split('\n')
        errors = [
            s.strip()
            for s in stdout_splits + stderr_splits
            if is_error_str_known(s.strip())
        ]
        if errors:
            return errors
        if 'rsync: command not found' in stderr:
            with ux_utils.print_exception_no_traceback():
                e = RuntimeError(_RSYNC_NOT_FOUND_MESSAGE)
                setattr(e, 'detailed_reason',
                        f'stdout: {stdout}\nstderr: {stderr}')
                raise e
        detailed_reason = textwrap.dedent(f"""\
        ====== stdout ======
        {stdout}
        ====== stderr ======
        {stderr}
        """)
        logger.info('====== stdout ======')
        print(stdout)
        logger.info('====== stderr ======')
        print(stderr)
        with ux_utils.print_exception_no_traceback():
            e = RuntimeError('Errors occurred during provision; '
                             'check logs above.')
            setattr(e, 'detailed_reason', detailed_reason)
            raise e

    @staticmethod
    def _lambda_handler(blocked_resources: Set['resources_lib.Resources'],
                        launchable_resources: 'resources_lib.Resources',
                        region: 'clouds.Region',
                        zones: Optional[List['clouds.Zone']], stdout: str,
                        stderr: str):
        del zones  # Unused.
        errors = FailoverCloudErrorHandlerV1._handle_errors(
            stdout,
            stderr,
            is_error_str_known=lambda x: 'LambdaCloudError:' in x.strip())
        logger.warning(f'Got error(s) in {region.name}:')
        messages = '\n\t'.join(errors)
        style = colorama.Style
        logger.warning(f'{style.DIM}\t{messages}{style.RESET_ALL}')
        _add_to_blocked_resources(blocked_resources,
                                  launchable_resources.copy(zone=None))

        # Sometimes, LambdaCloudError will list available regions.
        for e in errors:
            if e.find('Regions with capacity available:') != -1:
                for r in service_catalog.regions('lambda'):
                    if e.find(r.name) == -1:
                        _add_to_blocked_resources(
                            blocked_resources,
                            launchable_resources.copy(region=r.name, zone=None))

    @staticmethod
    def _scp_handler(blocked_resources: Set['resources_lib.Resources'],
                     launchable_resources: 'resources_lib.Resources',
                     region: 'clouds.Region',
                     zones: Optional[List['clouds.Zone']], stdout: str,
                     stderr: str):
        del zones  # Unused.
        errors = FailoverCloudErrorHandlerV1._handle_errors(
            stdout,
            stderr,
            is_error_str_known=lambda x: 'SCPError:' in x.strip())

        logger.warning(f'Got error(s) in {region.name}:')
        messages = '\n\t'.join(errors)
        style = colorama.Style
        logger.warning(f'{style.DIM}\t{messages}{style.RESET_ALL}')
        _add_to_blocked_resources(blocked_resources,
                                  launchable_resources.copy(zone=None))

        # Sometimes, SCPError will list available regions.
        for e in errors:
            if e.find('Regions with capacity available:') != -1:
                for r in service_catalog.regions('scp'):
                    if e.find(r.name) == -1:
                        _add_to_blocked_resources(
                            blocked_resources,
                            launchable_resources.copy(region=r.name, zone=None))

    @staticmethod
    def _ibm_handler(blocked_resources: Set['resources_lib.Resources'],
                     launchable_resources: 'resources_lib.Resources',
                     region: 'clouds.Region',
                     zones: Optional[List['clouds.Zone']], stdout: str,
                     stderr: str):

        errors = FailoverCloudErrorHandlerV1._handle_errors(
            stdout, stderr,
            lambda x: 'ERR' in x.strip() or 'PANIC' in x.strip())

        logger.warning(f'Got error(s) on IBM cluster, in {region.name}:')
        messages = '\n\t'.join(errors)
        style = colorama.Style
        logger.warning(f'{style.DIM}\t{messages}{style.RESET_ALL}')

        for zone in zones:  # type: ignore[union-attr]
            _add_to_blocked_resources(blocked_resources,
                                      launchable_resources.copy(zone=zone.name))

    # Apr, 2023 by Hysun(hysun.he@oracle.com): Added support for OCI
    @staticmethod
    def _oci_handler(blocked_resources: Set['resources_lib.Resources'],
                     launchable_resources: 'resources_lib.Resources',
                     region: 'clouds.Region',
                     zones: Optional[List['clouds.Zone']], stdout: str,
                     stderr: str):
        known_service_errors = [
            'NotAuthorizedOrNotFound', 'CannotParseRequest', 'InternalError',
            'LimitExceeded', 'NotAuthenticated'
        ]
        errors = FailoverCloudErrorHandlerV1._handle_errors(
            stdout, stderr, lambda x: 'VcnSubnetNotFound' in x.strip() or
            ('oci.exceptions.ServiceError' in x.strip() and any(
                known_err in x.strip() for known_err in known_service_errors)))
        logger.warning(f'Got error(s) in {region.name}:')
        messages = '\n\t'.join(errors)
        style = colorama.Style
        logger.warning(f'{style.DIM}\t{messages}{style.RESET_ALL}')

        if zones is not None:
            for zone in zones:
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(zone=zone.name))

    @staticmethod
    def update_blocklist_on_error(
            blocked_resources: Set['resources_lib.Resources'],
            launchable_resources: 'resources_lib.Resources',
            region: 'clouds.Region', zones: Optional[List['clouds.Zone']],
            stdout: Optional[str], stderr: Optional[str]) -> bool:
        """Handles cloud-specific errors and updates the block list.

        This parses textual stdout/stderr because we don't directly use the
        underlying clouds' SDKs.  If we did that, we could catch proper
        exceptions instead.

        Returns:
          definitely_no_nodes_launched: bool, True if definitely no nodes
            launched (e.g., due to VPC errors we have never sent the provision
            request), False otherwise.
        """
        assert launchable_resources.region == region.name, (
            launchable_resources, region)
        if stdout is None:
            # Gang scheduling failure (head node is definitely up, but some
            # workers' provisioning failed).  Simply block the zones.
            assert stderr is None, stderr
            if zones is not None:
                for zone in zones:
                    _add_to_blocked_resources(
                        blocked_resources,
                        launchable_resources.copy(zone=zone.name))
            return False  # definitely_no_nodes_launched
        assert stdout is not None and stderr is not None, (stdout, stderr)

        # TODO(zongheng): refactor into Cloud interface?
        cloud = launchable_resources.cloud
        handler = getattr(FailoverCloudErrorHandlerV1,
                          f'_{str(cloud).lower()}_handler')
        if handler is None:
            raise NotImplementedError(
                f'Cloud {cloud} unknown, or has not added '
                'support for parsing and handling provision failures. '
                'Please implement a handler in FailoverCloudErrorHandlerV1 when'
                'ray-autoscaler-based provisioner is used for the cloud.')
        handler(blocked_resources, launchable_resources, region, zones, stdout,
                stderr)

        stdout_splits = stdout.split('\n')
        stderr_splits = stderr.split('\n')
        # Determining whether head node launch *may* have been requested based
        # on outputs is tricky. We are conservative here by choosing an "early
        # enough" output line in the following:
        # https://github.com/ray-project/ray/blob/03b6bc7b5a305877501110ec04710a9c57011479/python/ray/autoscaler/_private/commands.py#L704-L737  # pylint: disable=line-too-long
        # This is okay, because we mainly want to use the return value of this
        # func to skip cleaning up never-launched clusters that encountered VPC
        # errors; their launch should not have printed any such outputs.
        head_node_launch_may_have_been_requested = any(
            'Acquiring an up-to-date head node' in line
            for line in stdout_splits + stderr_splits)
        # If head node request has definitely not been sent (this happens when
        # there are errors during node provider "bootstrapping", e.g.,
        # VPC-not-found errors), then definitely no nodes are launched.
        definitely_no_nodes_launched = (
            not head_node_launch_may_have_been_requested)

        return definitely_no_nodes_launched


class FailoverCloudErrorHandlerV2:
    """Handles errors during provisioning and updates the blocked_resources.

    This is a more robust version of FailoverCloudErrorHandlerV1. V2 parses
    the errors raised by the cloud's API using the exception, instead of the
    stdout and stderr.
    """

    @staticmethod
    def _azure_handler(blocked_resources: Set['resources_lib.Resources'],
                       launchable_resources: 'resources_lib.Resources',
                       region: 'clouds.Region', zones: List['clouds.Zone'],
                       err: Exception):
        del region, zones  # Unused.
        if '(ReadOnlyDisabledSubscription)' in str(err):
            logger.info(
                f'{colorama.Style.DIM}Azure subscription is read-only. '
                'Skip provisioning on Azure. Please check the subscription set '
                'with az account set -s <subscription_id>.'
                f'{colorama.Style.RESET_ALL}')
            _add_to_blocked_resources(
                blocked_resources,
                resources_lib.Resources(cloud=clouds.Azure()))
        else:
            _add_to_blocked_resources(blocked_resources,
                                      launchable_resources.copy(zone=None))

    @staticmethod
    def _gcp_handler(blocked_resources: Set['resources_lib.Resources'],
                     launchable_resources: 'resources_lib.Resources',
                     region: 'clouds.Region', zones: List['clouds.Zone'],
                     err: Exception):
        assert zones and len(zones) == 1, zones
        zone = zones[0]

        if not isinstance(err, provision_common.ProvisionerError):
            logger.warning(f'{colorama.Style.DIM}Got an unparsed error: {err}; '
                           f'blocking resources by its zone {zone.name}'
                           f'{colorama.Style.RESET_ALL}')
            _add_to_blocked_resources(blocked_resources,
                                      launchable_resources.copy(zone=zone.name))
            return
        errors = err.errors

        for e in errors:
            code = e['code']
            message = e['message']

            if code in ('QUOTA_EXCEEDED', 'quotaExceeded'):
                if '\'GPUS_ALL_REGIONS\' exceeded' in message:
                    # Global quota.  All regions in GCP will fail.  Ex:
                    # Quota 'GPUS_ALL_REGIONS' exceeded.  Limit: 1.0
                    # globally.
                    # This skip is only correct if we implement "first
                    # retry the region/zone of an existing cluster with the
                    # same name" correctly.
                    _add_to_blocked_resources(
                        blocked_resources,
                        launchable_resources.copy(region=None, zone=None))
                else:
                    # Per region.  Ex: Quota 'CPUS' exceeded.  Limit: 24.0
                    # in region us-west1.
                    _add_to_blocked_resources(
                        blocked_resources, launchable_resources.copy(zone=None))
            elif code in [
                    'ZONE_RESOURCE_POOL_EXHAUSTED',
                    'ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS',
                    'UNSUPPORTED_OPERATION',
                    'insufficientCapacity',
            ]:  # Per zone.
                # Return codes can be found at https://cloud.google.com/compute/docs/troubleshooting/troubleshooting-vm-creation # pylint: disable=line-too-long
                # However, UNSUPPORTED_OPERATION is observed empirically
                # when VM is preempted during creation.  This seems to be
                # not documented by GCP.
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(zone=zone.name))
            elif code in ['RESOURCE_NOT_READY']:
                # This code is returned when the VM is still STOPPING.
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(zone=zone.name))
            elif code in ['RESOURCE_OPERATION_RATE_EXCEEDED']:
                # This code can happen when the VM is being created with a
                # machine image, and the VM and the machine image are on
                # different zones. We already have the retry when calling the
                # insert API, but if it still fails, we should block the zone
                # to avoid infinite retry.
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(zone=zone.name))
            elif code in [3, 8, 9]:
                # Error code 3 means TPU is preempted during creation.
                # Example:
                # {'code': 3, 'message': 'Cloud TPU received a bad request. update is not supported while in state PREEMPTED [EID: 0x73013519f5b7feb2]'} # pylint: disable=line-too-long
                # Error code 8 means TPU resources is out of
                # capacity. Example:
                # {'code': 8, 'message': 'There is no more capacity in the zone "europe-west4-a"; you can try in another zone where Cloud TPU Nodes are offered (see https://cloud.google.com/tpu/docs/regions) [EID: 0x1bc8f9d790be9142]'} # pylint: disable=line-too-long
                # Error code 9 means TPU resources is insufficient reserved
                # capacity. Example:
                # {'code': 9, 'message': 'Insufficient reserved capacity. Contact customer support to increase your reservation. [EID: 0x2f8bc266e74261a]'} # pylint: disable=line-too-long
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(zone=zone.name))
            elif code == 'RESOURCE_NOT_FOUND':
                # https://github.com/skypilot-org/skypilot/issues/1797
                # In the inner provision loop we have used retries to
                # recover but failed. This indicates this zone is most
                # likely out of capacity. The provision loop will terminate
                # any potentially live VMs before moving onto the next
                # zone.
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(zone=zone.name))
            elif code == 'VPC_NOT_FOUND':
                # User has specified a VPC that does not exist. On GCP, VPC is
                # global. So we skip the entire cloud.
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(region=None, zone=None))
            elif code == 'SUBNET_NOT_FOUND_FOR_VPC':
                if (launchable_resources.accelerators is not None and any(
                        acc.lower().startswith('tpu-v4')
                        for acc in launchable_resources.accelerators.keys()) and
                        region.name == 'us-central2'):
                    # us-central2 is a TPU v4 only region. The subnet for
                    # this region may not exist when the user does not have
                    # the TPU v4 quota. We should skip this region.
                    logger.warning('Please check if you have TPU v4 quotas '
                                   f'in {region.name}.')
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(region=region.name, zone=None))
            elif code == 'type.googleapis.com/google.rpc.QuotaFailure':
                # TPU VM pod specific error.
                if 'in region' in message:
                    # Example:
                    # "Quota 'TPUV2sPreemptiblePodPerProjectPerRegionForTPUAPI'
                    # exhausted. Limit 32 in region europe-west4"
                    _add_to_blocked_resources(
                        blocked_resources,
                        launchable_resources.copy(region=region.name,
                                                  zone=None))
                elif 'in zone' in message:
                    # Example:
                    # "Quota 'TPUV2sPreemptiblePodPerProjectPerZoneForTPUAPI'
                    # exhausted. Limit 32 in zone europe-west4-a"
                    _add_to_blocked_resources(
                        blocked_resources,
                        launchable_resources.copy(zone=zone.name))

            elif 'Requested disk size cannot be smaller than the image size' in message:
                logger.info('Skipping all regions due to disk size issue.')
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(region=None, zone=None))
            elif 'Policy update access denied.' in message or code == 'IAM_PERMISSION_DENIED':
                logger.info(
                    'Skipping all regions due to service account not '
                    'having the required permissions and the user '
                    'account does not have enough permission to '
                    'update it. Please contact your administrator and '
                    'check out: https://skypilot.readthedocs.io/en/latest/cloud-setup/cloud-permissions/gcp.html\n'  # pylint: disable=line-too-long
                    f'Details: {message}')
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(region=None, zone=None))
            elif 'is not found or access is unauthorized' in message:
                # Parse HttpError for unauthorized regions. Example:
                # googleapiclient.errors.HttpError: <HttpError 403 when requesting ... returned "Location us-east1-d is not found or access is unauthorized.". # pylint: disable=line-too-long
                # Details: "Location us-east1-d is not found or access is
                # unauthorized.">
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(zone=zone.name))
            else:
                logger.debug('Got unparsed error blocking resources by zone: '
                             f'{e}.')
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(zone=zone.name))

    @staticmethod
    def _default_handler(blocked_resources: Set['resources_lib.Resources'],
                         launchable_resources: 'resources_lib.Resources',
                         region: 'clouds.Region',
                         zones: Optional[List['clouds.Zone']],
                         error: Exception) -> None:
        """Handles cloud-specific errors and updates the block list."""
        del region  # Unused.
        logger.debug(
            f'Got error(s) in {launchable_resources.cloud}:'
            f'{common_utils.format_exception(error, use_bracket=True)}')
        if zones is None:
            _add_to_blocked_resources(blocked_resources,
                                      launchable_resources.copy(zone=None))
        else:
            for zone in zones:
                _add_to_blocked_resources(
                    blocked_resources,
                    launchable_resources.copy(zone=zone.name))

    @staticmethod
    def update_blocklist_on_error(
            blocked_resources: Set['resources_lib.Resources'],
            launchable_resources: 'resources_lib.Resources',
            region: 'clouds.Region', zones: Optional[List['clouds.Zone']],
            error: Exception) -> None:
        """Handles cloud-specific errors and updates the block list."""
        cloud = launchable_resources.cloud
        handler = getattr(FailoverCloudErrorHandlerV2,
                          f'_{str(cloud).lower()}_handler',
                          FailoverCloudErrorHandlerV2._default_handler)
        handler(blocked_resources, launchable_resources, region, zones, error)


class RetryingVmProvisioner(object):
    """A provisioner that retries different cloud/regions/zones."""

    class ToProvisionConfig:
        """Resources to be provisioned."""

        def __init__(
            self,
            cluster_name: str,
            resources: resources_lib.Resources,
            num_nodes: int,
            prev_cluster_status: Optional[status_lib.ClusterStatus],
            prev_handle: Optional['CloudVmRayResourceHandle'],
            prev_cluster_ever_up: bool,
        ) -> None:
            assert cluster_name is not None, 'cluster_name must be specified.'
            self.cluster_name = cluster_name
            self.resources = resources
            self.num_nodes = num_nodes
            self.prev_cluster_status = prev_cluster_status
            self.prev_handle = prev_handle
            self.prev_cluster_ever_up = prev_cluster_ever_up

    def __init__(self,
                 log_dir: str,
                 dag: 'dag.Dag',
                 optimize_target: 'optimizer.OptimizeTarget',
                 requested_features: Set[clouds.CloudImplementationFeatures],
                 local_wheel_path: pathlib.Path,
                 wheel_hash: str,
                 blocked_resources: Optional[Iterable[
                     resources_lib.Resources]] = None):
        self._blocked_resources: Set[resources_lib.Resources] = set()
        if blocked_resources:
            # blocked_resources is not None and not empty.
            self._blocked_resources.update(blocked_resources)

        self.log_dir = os.path.expanduser(log_dir)
        self._dag = dag
        self._optimize_target = optimize_target
        self._requested_features = requested_features
        self._local_wheel_path = local_wheel_path
        self._wheel_hash = wheel_hash

    def _yield_zones(
            self, to_provision: resources_lib.Resources, num_nodes: int,
            cluster_name: str,
            prev_cluster_status: Optional[status_lib.ClusterStatus],
            prev_cluster_ever_up: bool
    ) -> Iterable[Optional[List[clouds.Zone]]]:
        """Yield zones within the given region to try for provisioning.

        Yields:
            Zones to try for provisioning within the given to_provision.region.
              - None means the cloud does not support zones, but the region does
                offer the requested resources (so the outer loop should issue a
                request to that region).
              - Non-empty list means the cloud supports zones, and the zones
                do offer the requested resources. If a list is yielded, it is
                guaranteed to be non-empty.
              - Nothing yielded means the region does not offer the requested
                resources.
        """
        assert (to_provision.cloud is not None and
                to_provision.region is not None and to_provision.instance_type
                is not None), (to_provision,
                               'cloud, region and instance_type must have been '
                               'set by optimizer')
        cloud = to_provision.cloud
        region = clouds.Region(to_provision.region)
        zones = None

        def _get_previously_launched_zones() -> Optional[List[clouds.Zone]]:
            # When the cluster exists, the to_provision should have been set
            # to the previous cluster's resources.
            zones = [
                clouds.Zone(name=to_provision.zone),
            ] if to_provision.zone is not None else None
            if zones is None:
                # Reuse the zone field in the ray yaml as the
                # prev_resources.zone field may not be set before the previous
                # cluster is launched.
                handle = global_user_state.get_handle_from_cluster_name(
                    cluster_name)
                assert isinstance(handle, CloudVmRayResourceHandle), (
                    'handle should be CloudVmRayResourceHandle (found: '
                    f'{type(handle)}) {cluster_name!r}')
                config = common_utils.read_yaml(handle.cluster_yaml)
                # This is for the case when the zone field is not set in the
                # launched resources in a previous launch (e.g., ctrl-c during
                # launch and multi-node cluster before PR #1700).
                zones_str = config.get('provider', {}).get('availability_zone')
                if zones_str is not None:
                    zones = [
                        clouds.Zone(name=zone) for zone in zones_str.split(',')
                    ]
            return zones

        if prev_cluster_status is not None:
            # If the cluster is previously launched, we should relaunch in the
            # same region and zone.
            zones = _get_previously_launched_zones()

            if prev_cluster_status != status_lib.ClusterStatus.UP:
                logger.info(
                    f'Cluster {cluster_name!r} (status: '
                    f'{prev_cluster_status.value}) was previously launched '
                    f'in {cloud} {region.name}. Relaunching in that region.')
            yield zones

            # If it reaches here: the cluster status in the database gets
            # set to either STOPPED or None, since a launch request was issued
            # but failed, and the provisioning loop (_retry_zones()) stopped the
            # cluster if `cluster_ever_up` is True; or terminated the cluster
            # otherwise.
            if prev_cluster_ever_up:
                message = (f'Failed to launch cluster {cluster_name!r} '
                           f'(previous status: {prev_cluster_status.value}). '
                           'To retry launching the cluster, run: '
                           f'sky start {cluster_name}')
                with ux_utils.print_exception_no_traceback():
                    raise exceptions.ResourcesUnavailableError(message,
                                                               no_failover=True)

            assert (prev_cluster_status == status_lib.ClusterStatus.INIT
                   ), prev_cluster_status
            message = (f'Failed to launch cluster {cluster_name!r} '
                       f'(previous status: {prev_cluster_status.value}) '
                       f'with the original resources: {to_provision}.')
            # We attempted re-launching a previously INIT cluster with the
            # same cloud/region/resources, but failed. Here no_failover=False,
            # so we will retry provisioning it with the current requested
            # resources in the outer loop.
            #
            # This condition can be triggered for previously INIT cluster by
            # (1) launch, after answering prompt immediately ctrl-c;
            # (2) launch again.
            # After (1), the cluster exists with INIT, and may or may not be
            # live.  And if it hits here, it's definitely not alive (because
            # step (2) failed).  Hence it's ok to retry with different
            # cloud/region and with current resources.
            with ux_utils.print_exception_no_traceback():
                raise exceptions.ResourcesUnavailableError(message)

        # If it reaches here, it means the cluster did not exist, as all the
        # cases when the cluster exists have been handled above (either the
        # provision succeeded in the caller and no need to retry, or this
        # function raised an ResourcesUnavailableError).
        for zones in cloud.zones_provision_loop(
                region=to_provision.region,
                num_nodes=num_nodes,
                instance_type=to_provision.instance_type,
                accelerators=to_provision.accelerators,
                use_spot=to_provision.use_spot,
        ):
            if zones is None:
                yield None
            else:
                assert zones, (
                    'Either None or a non-empty list of zones should '
                    'be yielded')
                # Only retry requested region/zones or all if not specified.
                zone_names = [zone.name for zone in zones]
                if not to_provision.valid_on_region_zones(
                        region.name, zone_names):
                    continue
                if to_provision.zone is not None:
                    zones = [clouds.Zone(name=to_provision.zone)]
                yield zones

    def _retry_zones(
        self,
        to_provision: resources_lib.Resources,
        num_nodes: int,
        requested_resources: Set[resources_lib.Resources],
        dryrun: bool,
        stream_logs: bool,
        cluster_name: str,
        cloud_user_identity: Optional[List[str]],
        prev_cluster_status: Optional[status_lib.ClusterStatus],
        prev_handle: Optional['CloudVmRayResourceHandle'],
        prev_cluster_ever_up: bool,
    ) -> Dict[str, Any]:
        """The provision retry loop."""
        style = colorama.Style
        fore = colorama.Fore
        # Get log_path name
        log_path = os.path.join(self.log_dir, 'provision.log')
        log_abs_path = os.path.abspath(log_path)
        if not dryrun:
            os.makedirs(os.path.expanduser(self.log_dir), exist_ok=True)
            os.system(f'touch {log_path}')
        tail_cmd = f'tail -n100 -f {log_path}'
        logger.info('To view detailed progress: '
                    f'{style.BRIGHT}{tail_cmd}{style.RESET_ALL}')

        # Get previous cluster status
        cluster_exists = prev_cluster_status is not None

        assert to_provision.region is not None, (
            to_provision, 'region should have been set by the optimizer.')
        region = clouds.Region(to_provision.region)

        # Optimization - check if user has non-zero quota for
        # the instance type in the target region. If not, fail early
        # instead of trying to provision and failing later.
        try:
            need_provision = to_provision.cloud.check_quota_available(
                to_provision)

        except Exception as e:  # pylint: disable=broad-except
            need_provision = True
            logger.info(f'Error occurred when trying to check quota. '
                        f'Proceeding assuming quotas are available. Error: '
                        f'{common_utils.format_exception(e, use_bracket=True)}')

        if not need_provision:
            # if quota is found to be zero, raise exception and skip to
            # the next region
            if to_provision.use_spot:
                instance_descriptor = 'spot'
            else:
                instance_descriptor = 'on-demand'
            raise exceptions.ResourcesUnavailableError(
                f'{colorama.Fore.YELLOW}Found no quota for '
                f'{to_provision.instance_type} {instance_descriptor} '
                f'instances in region {to_provision.region} '
                f'in {to_provision.cloud}. '
                f'{colorama.Style.RESET_ALL}'
                f'To request quotas, check the instruction: '
                f'https://skypilot.readthedocs.io/en/latest/cloud-setup/quota.html.'  # pylint: disable=line-too-long
            )

        for zones in self._yield_zones(to_provision, num_nodes, cluster_name,
                                       prev_cluster_status,
                                       prev_cluster_ever_up):
            # Filter out zones that are blocked, if any.
            # This optimize the provision loop by skipping zones that are
            # indicated to be unavailable from previous provision attempts.
            # It can happen for the provisioning on GCP, as the
            # yield_region_zones will return zones from a region one by one,
            # but the optimizer that does the filtering will not be involved
            # until the next region.
            if zones is not None:
                remaining_unblocked_zones = copy.deepcopy(zones)
                for zone in zones:
                    for blocked_resources in self._blocked_resources:
                        if to_provision.copy(
                                region=region.name,
                                zone=zone.name).should_be_blocked_by(
                                    blocked_resources):
                            remaining_unblocked_zones.remove(zone)
                            break
                if not remaining_unblocked_zones:
                    # Skip the region if all zones are blocked.
                    continue
                zones = remaining_unblocked_zones

            if zones is None:
                # For clouds that don't have a zone concept or cloud
                # provisioners that do not support zone-based provisioning
                # (e.g., Azure, Lambda).
                zone_str = ''
            else:
                zone_str = ','.join(z.name for z in zones)
                zone_str = f' ({zone_str})'
            try:
                config_dict = backend_utils.write_cluster_config(
                    to_provision,
                    num_nodes,
                    _get_cluster_config_template(to_provision.cloud),
                    cluster_name,
                    self._local_wheel_path,
                    self._wheel_hash,
                    region=region,
                    zones=zones,
                    dryrun=dryrun,
                    keep_launch_fields_in_existing_config=cluster_exists)
            except exceptions.ResourcesUnavailableError as e:
                # Failed due to catalog issue, e.g. image not found, or
                # GPUs are requested in a Kubernetes cluster but the cluster
                # does not have nodes labeled with GPU types.
                logger.info(f'{e}')
                continue
            except exceptions.InvalidCloudConfigs as e:
                # Failed due to invalid user configs in ~/.sky/config.yaml.
                logger.warning(f'{common_utils.format_exception(e)}')
                # We should block the entire cloud if the user config is
                # invalid.
                _add_to_blocked_resources(
                    self._blocked_resources,
                    to_provision.copy(region=None, zone=None))
                raise exceptions.ResourcesUnavailableError(
                    f'Failed to provision on cloud {to_provision.cloud} due to '
                    f'invalid cloud config: {common_utils.format_exception(e)}')
            if dryrun:
                return config_dict
            cluster_config_file = config_dict['ray']

            launched_resources = to_provision.copy(region=region.name)
            if zones and len(zones) == 1:
                launched_resources = launched_resources.copy(zone=zones[0].name)

            prev_cluster_ips, prev_ssh_ports, prev_cluster_info = (None, None,
                                                                   None)
            if prev_handle is not None:
                prev_cluster_ips = prev_handle.stable_internal_external_ips
                prev_ssh_ports = prev_handle.stable_ssh_ports
                prev_cluster_info = prev_handle.cached_cluster_info
            # Record early, so if anything goes wrong, 'sky status' will show
            # the cluster name and users can appropriately 'sky down'.  It also
            # means a second 'sky launch -c <name>' will attempt to reuse.
            handle = CloudVmRayResourceHandle(
                cluster_name=cluster_name,
                # Backward compatibility will be guaranteed by the underlying
                # backend_utils.write_cluster_config, which gets the cluster
                # name on cloud from the ray yaml file, if the previous cluster
                # exists.
                cluster_name_on_cloud=config_dict['cluster_name_on_cloud'],
                cluster_yaml=cluster_config_file,
                launched_nodes=num_nodes,
                # OK for this to be shown in CLI as status == INIT.
                launched_resources=launched_resources,
                # Use the previous cluster's IPs and ports if available to
                # optimize the case where the cluster is restarted, i.e., no
                # need to query IPs and ports from the cloud provider.
                stable_internal_external_ips=prev_cluster_ips,
                stable_ssh_ports=prev_ssh_ports,
                cluster_info=prev_cluster_info,
            )
            usage_lib.messages.usage.update_final_cluster_status(
                status_lib.ClusterStatus.INIT)

            # This sets the status to INIT (even for a normal, UP cluster).
            global_user_state.add_or_update_cluster(
                cluster_name,
                cluster_handle=handle,
                requested_resources=requested_resources,
                ready=False,
            )

            global_user_state.set_owner_identity_for_cluster(
                cluster_name, cloud_user_identity)

            if (to_provision.cloud.PROVISIONER_VERSION ==
                    clouds.ProvisionerVersion.SKYPILOT):
                # TODO (suquark): Gradually move the other clouds to
                #  the new provisioner once they are ready.
                assert to_provision.region == region.name, (to_provision,
                                                            region)
                num_nodes = handle.launched_nodes
                # Some clouds, like RunPod, only support exposing ports during
                # launch. For those clouds, we pass the ports to open in the
                # `bulk_provision` to expose the ports during provisioning.
                # If the `bulk_provision` is to apply on an existing cluster,
                # it should be ignored by the underlying provisioner impl
                # as it will only apply to newly-created instances.
                ports_to_open_on_launch = (
                    list(resources_utils.port_ranges_to_set(to_provision.ports))
                    if to_provision.cloud.OPEN_PORTS_VERSION <=
                    clouds.OpenPortsVersion.LAUNCH_ONLY else None)
                try:
                    provision_record = provisioner.bulk_provision(
                        to_provision.cloud,
                        region,
                        zones,
                        resources_utils.ClusterName(
                            cluster_name, handle.cluster_name_on_cloud),
                        num_nodes=num_nodes,
                        cluster_yaml=handle.cluster_yaml,
                        prev_cluster_ever_up=prev_cluster_ever_up,
                        log_dir=self.log_dir,
                        ports_to_open_on_launch=ports_to_open_on_launch)
                    # NOTE: We will handle the logic of '_ensure_cluster_ray_started' #pylint: disable=line-too-long
                    # in 'provision_utils.post_provision_runtime_setup()' in the
                    # caller.
                    resources_vars = (
                        to_provision.cloud.make_deploy_resources_variables(
                            to_provision,
                            resources_utils.ClusterName(
                                cluster_name, handle.cluster_name_on_cloud),
                            region, zones))
                    config_dict['provision_record'] = provision_record
                    config_dict['resources_vars'] = resources_vars
                    config_dict['handle'] = handle
                    return config_dict
                except provision_common.StopFailoverError:
                    with ux_utils.print_exception_no_traceback():
                        raise
                except Exception as e:  # pylint: disable=broad-except
                    # NOTE: We try to cleanup the cluster even if the previous
                    # cluster does not exist. Also we are fast at
                    # cleaning up clusters now if there is no existing node..
                    CloudVmRayBackend().post_teardown_cleanup(
                        handle, terminate=not prev_cluster_ever_up)
                    # TODO(suquark): other clouds may have different zone
                    #  blocking strategy. See '_update_blocklist_on_error'
                    #  for details.
                    FailoverCloudErrorHandlerV2.update_blocklist_on_error(
                        self._blocked_resources, to_provision, region, zones, e)
                    continue
                # NOTE: The code below in the loop should not be reachable
                # with the new provisioner.

            logging_info = {
                'cluster_name': cluster_name,
                'region_name': region.name,
                'zone_str': zone_str,
            }
            status, stdout, stderr, head_internal_ip, head_external_ip = (
                self._gang_schedule_ray_up(to_provision.cloud,
                                           cluster_config_file, handle,
                                           log_abs_path, stream_logs,
                                           logging_info, to_provision.use_spot))

            if status == GangSchedulingStatus.CLUSTER_READY:
                # We must query the IPs from the cloud provider, when the
                # provisioning is done, to make sure the cluster IPs are
                # up-to-date.
                # The staled IPs may be caused by the node being restarted
                # manually or by the cloud provider.
                # Optimize the case where the cluster's head IPs can be parsed
                # from the output of 'ray up'.
                if handle.launched_nodes == 1:
                    handle.update_cluster_ips(
                        max_attempts=_FETCH_IP_MAX_ATTEMPTS,
                        internal_ips=[head_internal_ip],
                        external_ips=[head_external_ip])
                else:
                    handle.update_cluster_ips(
                        max_attempts=_FETCH_IP_MAX_ATTEMPTS)
                handle.update_ssh_ports(max_attempts=_FETCH_IP_MAX_ATTEMPTS)
                if cluster_exists:
                    # Guard against the case where there's an existing cluster
                    # with ray runtime messed up (e.g., manually killed) by (1)
                    # querying ray status (2) restarting ray if needed.
                    #
                    # The above 'ray up' will not restart it automatically due
                    # to 'ray up # --no-restart' flag.
                    #
                    # NOTE: this is performance sensitive and has been observed
                    # to take 9s. Only do this for existing clusters, not
                    # freshly launched ones (which should have ray runtime
                    # started).
                    self._ensure_cluster_ray_started(handle, log_abs_path)

                config_dict['handle'] = handle
                plural = '' if num_nodes == 1 else 's'
                logger.info(f'{fore.GREEN}Successfully provisioned or found'
                            f' existing VM{plural}.{style.RESET_ALL}')
                return config_dict

            # The cluster is not ready. We must perform error recording and/or
            # cleanup.

            # If cluster was ever up, stop it; otherwise terminate.
            terminate_or_stop = not prev_cluster_ever_up
            definitely_no_nodes_launched = False
            if status == GangSchedulingStatus.HEAD_FAILED:
                # ray up failed for the head node.
                definitely_no_nodes_launched = (
                    FailoverCloudErrorHandlerV1.update_blocklist_on_error(
                        self._blocked_resources, to_provision, region, zones,
                        stdout, stderr))
            else:
                # gang scheduling failed.
                assert status == GangSchedulingStatus.GANG_FAILED, status
                # The stdout/stderr of ray up is not useful here, since
                # head node is successfully provisioned.
                definitely_no_nodes_launched = (
                    FailoverCloudErrorHandlerV1.update_blocklist_on_error(
                        self._blocked_resources,
                        to_provision,
                        region,
                        zones=zones,
                        stdout=None,
                        stderr=None))
                # GANG_FAILED means head is up, workers failed.
                assert definitely_no_nodes_launched is False, (
                    definitely_no_nodes_launched)

                # Only log the errors for GANG_FAILED, since HEAD_FAILED may
                # not have created any resources (it can happen however) and
                # HEAD_FAILED can happen in "normal" failover cases.
                logger.error('*** Failed provisioning the cluster. ***')
                terminate_str = ('Terminating'
                                 if terminate_or_stop else 'Stopping')
                logger.error(f'*** {terminate_str} the failed cluster. ***')

            # If these conditions hold, it *should* be safe to skip the cleanup
            # action. This is a UX optimization.
            #
            # We want to skip mainly for VPC/subnets errors thrown during node
            # provider bootstrapping: if users encountered "No VPC with name
            # 'xxx' is found in <region>.", then going ahead to down the
            # non-existent cluster will itself print out a (caught, harmless)
            # error with the same message.  This was found to be
            # confusing. Thus we skip termination.
            skip_cleanup = not cluster_exists and definitely_no_nodes_launched
            if skip_cleanup:
                continue

            # There may exist partial nodes (e.g., head node) so we must
            # terminate or stop before moving on to other regions.
            #
            # NOTE: even HEAD_FAILED could've left a live head node there,
            # so we must terminate/stop here too. E.g., node is up, and ray
            # autoscaler proceeds to setup commands, which may fail:
            #   ERR updater.py:138 -- New status: update-failed
            CloudVmRayBackend().teardown_no_lock(handle,
                                                 terminate=terminate_or_stop)

        if to_provision.zone is not None:
            message = (
                f'Failed to acquire resources in {to_provision.zone}. '
                'Try changing resource requirements or use another zone.')
        elif to_provision.region is not None:
            # For public clouds, provision.region is always set.
            message = ('Failed to acquire resources in all zones in '
                       f'{to_provision.region}. Try changing resource '
                       'requirements or use another region.')
        else:
            message = (f'Failed to acquire resources in {to_provision.cloud}. '
                       'Try changing resource requirements or use another '
                       'cloud provider.')
        # Do not failover to other locations if the cluster was ever up, since
        # the user can have some data on the cluster.
        raise exceptions.ResourcesUnavailableError(
            message, no_failover=prev_cluster_ever_up)

    # TODO(suquark): Deprecate this method
    # once the `provision_utils` is adopted for all the clouds.
    @timeline.event
    def _gang_schedule_ray_up(
        self, to_provision_cloud: clouds.Cloud, cluster_config_file: str,
        cluster_handle: 'backends.CloudVmRayResourceHandle', log_abs_path: str,
        stream_logs: bool, logging_info: dict, use_spot: bool
    ) -> Tuple[GangSchedulingStatus, str, str, Optional[str], Optional[str]]:
        """Provisions a cluster via 'ray up' and wait until fully provisioned.

        Returns:
            (GangSchedulingStatus; stdout; stderr;
                optional head_internal_ip; optional head_external_ip).
        """
        # FIXME(zhwu,zongheng): ray up on multiple nodes ups the head node then
        # waits for all workers; turn it into real gang scheduling.
        # FIXME: refactor code path to remove use of stream_logs
        del stream_logs

        def ray_up():
            # Runs `ray up <kwargs>` with our monkey-patched launch hash
            # calculation. See the monkey patch file for why.
            #
            # NOTE: --no-restart solves the following bug.  Without it, if 'ray
            # up' (sky launch) twice on a cluster with >1 node, the worker node
            # gets disconnected/killed by ray autoscaler; the whole task will
            # just freeze.  (Doesn't affect 1-node clusters.)  With this flag,
            # ray processes no longer restart and this bug doesn't show.
            # Downside is existing tasks on the cluster will keep running
            # (which may be ok with the semantics of 'sky launch' twice).
            # Tracked in https://github.com/ray-project/ray/issues/20402.
            # Ref: https://github.com/ray-project/ray/blob/releases/2.4.0/python/ray/autoscaler/sdk/sdk.py#L16-L49  # pylint: disable=line-too-long
            script_path = write_ray_up_script_with_patched_launch_hash_fn(
                cluster_config_file, ray_up_kwargs={'no_restart': True})

            # Redirect stdout/err to the file and streaming (if stream_logs).
            # With stdout/err redirected, 'ray up' will have no color and
            # different order from directly running in the console. The
            # `--log-style` and `--log-color` flags do not work. To reproduce,
            # `ray up --log-style pretty --log-color true | tee tmp.out`.
            returncode, stdout, stderr = log_lib.run_with_log(
                [sys.executable, script_path],
                log_abs_path,
                stream_logs=False,
                start_streaming_at='Shared connection to',
                line_processor=log_utils.RayUpLineProcessor(),
                # Reduce BOTO_MAX_RETRIES from 12 to 5 to avoid long hanging
                # time during 'ray up' if insufficient capacity occurs.
                env=dict(
                    os.environ,
                    BOTO_MAX_RETRIES='5',
                    # Use environment variables to disable the ray usage collection
                    # (to avoid overheads and potential issues with the usage)
                    # as sdk does not take the argument for disabling the usage
                    # collection.
                    RAY_USAGE_STATS_ENABLED='0'),
                require_outputs=True,
                # Disable stdin to avoid ray outputs mess up the terminal with
                # misaligned output when multithreading/multiprocessing are used
                # Refer to: https://github.com/ray-project/ray/blob/d462172be7c5779abf37609aed08af112a533e1e/python/ray/autoscaler/_private/subprocess_output_util.py#L264  # pylint: disable=line-too-long
                stdin=subprocess.DEVNULL)
            return returncode, stdout, stderr

        region_name = logging_info['region_name']
        zone_str = logging_info['zone_str']
        style = colorama.Style
        if isinstance(to_provision_cloud, clouds.Kubernetes):
            logger.info(f'{style.BRIGHT}Launching on {to_provision_cloud} '
                        f'{style.RESET_ALL}')
        else:
            logger.info(f'{style.BRIGHT}Launching on {to_provision_cloud} '
                        f'{region_name}{style.RESET_ALL}{zone_str}')
        start = time.time()

        # Edge case: /tmp/ray does not exist, so autoscaler can't create/store
        # cluster lock and cluster state.
        os.makedirs('/tmp/ray', exist_ok=True)

        # Launch the cluster with ray up

        # Retry if the any of the following happens:
        # 1. Failed due to timeout when fetching head node for Azure.
        # 2. Failed due to file mounts, because it is probably has too
        # many ssh connections and can be fixed by retrying.
        # This is required when using custom image for GCP.
        def need_ray_up(
                ray_up_return_value: Optional[Tuple[int, str, str]]) -> bool:

            # Indicates the first ray up.
            if ray_up_return_value is None:
                return True

            returncode, stdout, stderr = ray_up_return_value
            if returncode == 0:
                return False

            if isinstance(to_provision_cloud, clouds.Lambda):
                if 'Your API requests are being rate limited.' in stderr:
                    logger.info(
                        'Retrying due to Lambda API rate limit exceeded.')
                    return True

            if 'rsync: command not found' in stderr:
                logger.info('Skipping retry due to `rsync` not found in '
                            'the specified image.')
                return False

            if ('Processing file mounts' in stdout and
                    'Running setup commands' not in stdout and
                    'Failed to setup head node.' in stderr):
                logger.info(
                    'Retrying runtime setup due to ssh connection issue.')
                return True

            if ('ConnectionResetError: [Errno 54] Connection reset by peer'
                    in stderr):
                logger.info('Retrying due to Connection reset by peer.')
                return True
            return False

        retry_cnt = 0
        ray_up_return_value = None
        # 5 seconds to 180 seconds. We need backoff for e.g., rate limit per
        # minute errors.
        backoff = common_utils.Backoff(initial_backoff=5,
                                       max_backoff_factor=180 // 5)
        while (retry_cnt < _MAX_RAY_UP_RETRY and
               need_ray_up(ray_up_return_value)):
            retry_cnt += 1
            if retry_cnt > 1:
                sleep = backoff.current_backoff()
                logger.info(
                    'Retrying launching in {:.1f} seconds.'.format(sleep))
                time.sleep(sleep)
            # TODO(zhwu): when we retry ray up, it is possible that the ray
            # cluster fail to start because --no-restart flag is used.
            ray_up_return_value = ray_up()

        assert ray_up_return_value is not None
        returncode, stdout, stderr = ray_up_return_value

        logger.debug(f'`ray up` takes {time.time() - start:.1f} seconds with '
                     f'{retry_cnt} retries.')
        if returncode != 0:
            return GangSchedulingStatus.HEAD_FAILED, stdout, stderr, None, None

        # Only 1 node or head node provisioning failure.
        if cluster_handle.launched_nodes == 1 and returncode == 0:
            # Optimization: Try parse head ip from 'ray up' stdout.
            # Last line looks like: 'ssh ... <user>@<public head_ip>\n'
            position = stdout.rfind('@')
            # Use a regex to extract the IP address.
            external_ip_list = re.findall(backend_utils.IP_ADDR_REGEX,
                                          stdout[position + 1:])
            head_internal_ip, head_external_ip = None, None
            if len(external_ip_list) == 1:
                head_external_ip = external_ip_list[0]

            # Optimization: Try parse internal head ip from 'ray start' stdout.
            # The line looks like: 'Local node IP: <internal head_ip>\n'
            position = stdout.rfind('Local node IP')
            line = stdout[position:].partition('\n')[0]
            internal_ip_list = re.findall(backend_utils.IP_ADDR_REGEX,
                                          common_utils.remove_color(line))
            if len(internal_ip_list) == 1:
                head_internal_ip = internal_ip_list[0]

            logger.debug(f'Get head ips from ray up stdout: {head_internal_ip} '
                         f'{head_external_ip}')
            return (GangSchedulingStatus.CLUSTER_READY, stdout, stderr,
                    head_internal_ip, head_external_ip)

        # All code below is handling num_nodes > 1.
        provision_str = ('Successfully provisioned or found existing head '
                         'instance.')
        logger.info(f'{style.BRIGHT}{provision_str} '
                    f'Waiting for workers.{style.RESET_ALL}')

        # FIXME(zongheng): the below requires ray processes are up on head. To
        # repro it failing: launch a 2-node cluster, log into head and ray
        # stop, then launch again.
        cluster_ready = backend_utils.wait_until_ray_cluster_ready(
            cluster_config_file,
            num_nodes=cluster_handle.launched_nodes,
            log_path=log_abs_path,
            nodes_launching_progress_timeout=_NODES_LAUNCHING_PROGRESS_TIMEOUT[
                type(to_provision_cloud)])
        if cluster_ready:
            cluster_status = GangSchedulingStatus.CLUSTER_READY
            # ray up --no-restart again with upscaling_speed=0 after cluster is
            # ready to ensure cluster will not scale up after preemption (spot).
            # Skip for non-spot as this takes extra time to provision (~1min).
            if use_spot:
                ray_config = common_utils.read_yaml(cluster_config_file)
                ray_config['upscaling_speed'] = 0
                common_utils.dump_yaml(cluster_config_file, ray_config)
                start = time.time()
                returncode, stdout, stderr = ray_up()
                logger.debug(
                    f'Upscaling reset takes {time.time() - start} seconds.')
                if returncode != 0:
                    return (GangSchedulingStatus.GANG_FAILED, stdout, stderr,
                            None, None)
        else:
            cluster_status = GangSchedulingStatus.GANG_FAILED

        # Do not need stdout/stderr if gang scheduling failed.
        # gang_succeeded = False, if head OK, but workers failed.
        return cluster_status, '', '', None, None

    def _ensure_cluster_ray_started(self, handle: 'CloudVmRayResourceHandle',
                                    log_abs_path) -> None:
        """Ensures ray processes are up on a just-provisioned cluster."""
        if handle.launched_nodes > 1:
            # FIXME(zongheng): this has NOT been tested with multinode
            # clusters; mainly because this function will not be reached in
            # that case.  See #140 for details.  If it were reached, the
            # following logic might work:
            #   - get all node ips
            #   - for all nodes: ray stop
            #   - ray up --restart-only
            return
        backend = CloudVmRayBackend()

        returncode, output, _ = backend.run_on_head(
            handle,
            instance_setup.RAY_STATUS_WITH_SKY_RAY_PORT_COMMAND,
            require_outputs=True)
        while returncode == 0 and 'No cluster status' in output:
            # Retry until ray status is ready. This is to avoid the case where
            # ray cluster is just started but the ray status is not ready yet.
            logger.info('Waiting for ray cluster to be ready remotely.')
            time.sleep(1)
            returncode, output, _ = backend.run_on_head(
                handle,
                instance_setup.RAY_STATUS_WITH_SKY_RAY_PORT_COMMAND,
                require_outputs=True)
        if returncode == 0:
            return
        backend.run_on_head(handle, f'{constants.SKY_RAY_CMD} stop')

        # Runs `ray up <kwargs>` with our monkey-patched launch hash
        # calculation. See the monkey patch file for why.
        script_path = write_ray_up_script_with_patched_launch_hash_fn(
            handle.cluster_yaml, ray_up_kwargs={'restart_only': True})
        log_lib.run_with_log(
            [sys.executable, script_path],
            log_abs_path,
            stream_logs=False,
            # Use environment variables to disable the ray usage collection
            # (to avoid overheads and potential issues with the usage)
            # as sdk does not take the argument for disabling the usage
            # collection.
            env=dict(os.environ, RAY_USAGE_STATS_ENABLED='0'),
            # Disable stdin to avoid ray outputs mess up the terminal with
            # misaligned output when multithreading/multiprocessing is used.
            # Refer to: https://github.com/ray-project/ray/blob/d462172be7c5779abf37609aed08af112a533e1e/python/ray/autoscaler/_private/subprocess_output_util.py#L264 # pylint: disable=line-too-long
            stdin=subprocess.DEVNULL)

    @timeline.event
    def provision_with_retries(
        self,
        task: task_lib.Task,
        to_provision_config: ToProvisionConfig,
        dryrun: bool,
        stream_logs: bool,
    ) -> Dict[str, Any]:
        """Provision with retries for all launchable resources."""
        cluster_name = to_provision_config.cluster_name
        to_provision = to_provision_config.resources
        num_nodes = to_provision_config.num_nodes
        prev_cluster_status = to_provision_config.prev_cluster_status
        prev_handle = to_provision_config.prev_handle
        prev_cluster_ever_up = to_provision_config.prev_cluster_ever_up
        launchable_retries_disabled = (self._dag is None or
                                       self._optimize_target is None)

        failover_history: List[Exception] = list()

        style = colorama.Style
        fore = colorama.Fore
        # Retrying launchable resources.
        while True:
            if (isinstance(to_provision.cloud, clouds.Azure) and
                    to_provision.accelerators is not None and
                    'A10' in to_provision.accelerators and prev_handle is None):
                logger.warning(f'{style.BRIGHT}{fore.YELLOW}Trying to launch '
                               'an A10 cluster on Azure. This may take ~20 '
                               'minutes due to driver installation.'
                               f'{style.RESET_ALL}')
            try:
                # Recheck cluster name as the 'except:' block below may
                # change the cloud assignment.
                common_utils.check_cluster_name_is_valid(cluster_name)
                if dryrun:
                    cloud_user = None
                else:
                    cloud_user = to_provision.cloud.get_active_user_identity()

                requested_features = self._requested_features.copy()
                # Skip stop feature for Kubernetes and RunPod controllers.
                if (isinstance(to_provision.cloud,
                               (clouds.Kubernetes, clouds.RunPod)) and
                        controller_utils.Controllers.from_name(cluster_name)
                        is not None):
                    assert (clouds.CloudImplementationFeatures.STOP
                            in requested_features), requested_features
                    requested_features.remove(
                        clouds.CloudImplementationFeatures.STOP)

                # Skip if to_provision.cloud does not support requested features
                to_provision.cloud.check_features_are_supported(
                    to_provision, requested_features)

                config_dict = self._retry_zones(
                    to_provision,
                    num_nodes,
                    requested_resources=set(task.resources),
                    dryrun=dryrun,
                    stream_logs=stream_logs,
                    cluster_name=cluster_name,
                    cloud_user_identity=cloud_user,
                    prev_cluster_status=prev_cluster_status,
                    prev_handle=prev_handle,
                    prev_cluster_ever_up=prev_cluster_ever_up)
                if dryrun:
                    return config_dict
            except (exceptions.InvalidClusterNameError,
                    exceptions.NotSupportedError,
                    exceptions.CloudUserIdentityError) as e:
                # InvalidClusterNameError: cluster name is invalid,
                # NotSupportedError: cloud does not support requested features,
                # CloudUserIdentityError: cloud user identity is invalid.
                # The exceptions above should be applicable to the whole
                # cloud, so we do add the cloud to the blocked resources.
                logger.warning(common_utils.format_exception(e))
                _add_to_blocked_resources(
                    self._blocked_resources,
                    resources_lib.Resources(cloud=to_provision.cloud))
                failover_history.append(e)
            except exceptions.ResourcesUnavailableError as e:
                failover_history.append(e)
                if e.no_failover:
                    raise e.with_failover_history(failover_history)
                if launchable_retries_disabled:
                    logger.warning(
                        'DAG and optimize_target needs to be registered first '
                        'to enable cross-cloud retry. '
                        'To fix, call backend.register_info(dag=dag, '
                        'optimize_target=sky.OptimizeTarget.COST)')
                    raise e.with_failover_history(failover_history)

                logger.warning(common_utils.format_exception(e))
            else:
                # Provisioning succeeded.
                break

            if to_provision.zone is None:
                region_or_zone_str = str(to_provision.region)
            else:
                region_or_zone_str = str(to_provision.zone)
            logger.warning(f'\n{style.BRIGHT}Provision failed for {num_nodes}x '
                           f'{to_provision} in {region_or_zone_str}. '
                           f'Trying other locations (if any).{style.RESET_ALL}')
            if prev_cluster_status is None:
                # Add failed resources to the blocklist, only when it
                # is in fallback mode.
                _add_to_blocked_resources(self._blocked_resources, to_provision)
            else:
                # If we reach here, it means that the existing cluster must have
                # a previous status of INIT, because other statuses (UP,
                # STOPPED) will not trigger the failover due to `no_failover`
                # flag; see _yield_zones(). Also, the cluster should have been
                # terminated by _retry_zones().
                assert (prev_cluster_status == status_lib.ClusterStatus.INIT
                       ), prev_cluster_status
                assert global_user_state.get_handle_from_cluster_name(
                    cluster_name) is None, cluster_name
                logger.info('Retrying provisioning with requested resources '
                            f'{task.num_nodes}x {task.resources}')
                # Retry with the current, potentially "smaller" resources:
                # to_provision == the current new resources (e.g., V100:1),
                # which may be "smaller" than the original (V100:8).
                # num_nodes is not part of a Resources so must be updated
                # separately.
                num_nodes = task.num_nodes
                prev_cluster_status = None
                prev_handle = None

            # Set to None so that sky.optimize() will assign a new one
            # (otherwise will skip re-optimizing this task).
            # TODO: set all remaining tasks' best_resources to None.
            task.best_resources = None
            try:
                self._dag = sky.optimize(
                    self._dag,
                    minimize=self._optimize_target,
                    blocked_resources=self._blocked_resources)
            except exceptions.ResourcesUnavailableError as e:
                # Optimizer failed to find a feasible resources for the task,
                # either because the previous failovers have blocked all the
                # possible resources or the requested resources is too
                # restrictive. If we reach here, our failover logic finally
                # ends here.
                raise e.with_failover_history(failover_history)
            to_provision = task.best_resources
            assert task in self._dag.tasks, 'Internal logic error.'
            assert to_provision is not None, task
        return config_dict


class CloudVmRayResourceHandle(backends.backend.ResourceHandle):
    """A pickle-able handle to a cluster created by CloudVmRayBackend.

    The handle object will last for the whole lifecycle of the cluster.

    - (required) Cluster name.
    - (required) Cluster name on cloud (different from the cluster name, as we
        append user hash to avoid conflict b/t multiple users in the same
        organization/account, and truncate the name for length limit). See
        design_docs/cluster_name.md for details.
    - (required) Path to a cluster.yaml file.
    - (optional) A cached head node public IP.  Filled in after a
        successful provision().
    - (optional) A cached stable list of (internal IP, external IP) tuples
        for all nodes in a cluster. Filled in after successful task execution.
    - (optional) Launched num nodes
    - (optional) Launched resources
    - (optional) Docker user name
    - (optional) If TPU(s) are managed, a path to a deletion script.
    """
    # Bump if any fields get added/removed/changed, and add backward
    # compaitibility logic in __setstate__.
    _VERSION = 8

    def __init__(
            self,
            *,
            cluster_name: str,
            cluster_name_on_cloud: str,
            cluster_yaml: str,
            launched_nodes: int,
            launched_resources: resources_lib.Resources,
            stable_internal_external_ips: Optional[List[Tuple[str,
                                                              str]]] = None,
            stable_ssh_ports: Optional[List[int]] = None,
            cluster_info: Optional[provision_common.ClusterInfo] = None,
            # The following 2 fields are deprecated. SkyPilot new provisioner
            # API handles the TPU node creation/deletion.
            # Backward compatibility for TPU nodes created before #2943.
            # TODO (zhwu): Remove this after 0.6.0.
            tpu_create_script: Optional[str] = None,
            tpu_delete_script: Optional[str] = None) -> None:
        self._version = self._VERSION
        self.cluster_name = cluster_name
        self.cluster_name_on_cloud = cluster_name_on_cloud
        self._cluster_yaml = cluster_yaml.replace(os.path.expanduser('~'), '~',
                                                  1)
        # List of (internal_ip, feasible_ip) tuples for all the nodes in the
        # cluster, sorted by the feasible ips. The feasible ips can be either
        # internal or external ips, depending on the use_internal_ips flag.
        self.stable_internal_external_ips = stable_internal_external_ips
        self.stable_ssh_ports = stable_ssh_ports
        self.cached_cluster_info = cluster_info
        self.launched_nodes = launched_nodes
        self.launched_resources = launched_resources
        self.docker_user: Optional[str] = None
        # Deprecated. SkyPilot new provisioner API handles the TPU node
        # creation/deletion.
        # Backward compatibility for TPU nodes created before #2943.
        # TODO (zhwu): Remove this after 0.6.0.
        self.tpu_create_script = tpu_create_script
        self.tpu_delete_script = tpu_delete_script

    def __repr__(self):
        return (f'ResourceHandle('
                f'\n\tcluster_name={self.cluster_name},'
                f'\n\tcluster_name_on_cloud={self.cluster_name_on_cloud},'
                f'\n\thead_ip={self.head_ip},'
                '\n\tstable_internal_external_ips='
                f'{self.stable_internal_external_ips},'
                '\n\tstable_ssh_ports='
                f'{self.stable_ssh_ports},'
                '\n\tcluster_yaml='
                f'{self.cluster_yaml}, '
                f'\n\tlaunched_resources={self.launched_nodes}x '
                f'{self.launched_resources}, '
                f'\n\tdocker_user={self.docker_user},'
                f'\n\tssh_user={self.ssh_user},'
                # TODO (zhwu): Remove this after 0.6.0.
                f'\n\ttpu_create_script={self.tpu_create_script}, '
                f'\n\ttpu_delete_script={self.tpu_delete_script})')

    def get_cluster_name(self):
        return self.cluster_name

    def _use_internal_ips(self):
        """Returns whether to use internal IPs for SSH connections."""
        # Directly load the `use_internal_ips` flag from the cluster yaml
        # instead of `skypilot_config` as the latter can be changed after the
        # cluster is UP.
        return common_utils.read_yaml(self.cluster_yaml).get(
            'provider', {}).get('use_internal_ips', False)

    def _update_cluster_region(self):
        """Update the region in handle.launched_resources.

        This is for backward compatibility to handle the clusters launched
        long before. We should remove this after 0.6.0.
        """
        if self.launched_resources.region is not None:
            return

        config = common_utils.read_yaml(self.cluster_yaml)
        provider = config['provider']
        cloud = self.launched_resources.cloud
        if cloud.is_same_cloud(clouds.Azure()):
            region = provider['location']
        elif cloud.is_same_cloud(clouds.GCP()) or cloud.is_same_cloud(
                clouds.AWS()):
            region = provider['region']

        self.launched_resources = self.launched_resources.copy(region=region)

    def update_ssh_ports(self, max_attempts: int = 1) -> None:
        """Fetches and sets the SSH ports for the cluster nodes.

        Use this method to use any cloud-specific port fetching logic.
        """
        del max_attempts  # Unused.
        if self.cached_cluster_info is not None:
            self.stable_ssh_ports = self.cached_cluster_info.get_ssh_ports()
            return

        head_ssh_port = 22
        self.stable_ssh_ports = (
            [head_ssh_port] + [22] *
            (self.num_ips_per_node * self.launched_nodes - 1))

    def _update_cluster_info(self):
        # When a cluster is on a cloud that does not support the new
        # provisioner, we should skip updating cluster_info.
        if (self.launched_resources.cloud.PROVISIONER_VERSION >=
                clouds.ProvisionerVersion.SKYPILOT):
            provider_name = str(self.launched_resources.cloud).lower()
            config = {}
            if os.path.exists(self.cluster_yaml):
                # It is possible that the cluster yaml is not available when
                # the handle is unpickled for service replicas from the
                # controller with older version.
                config = common_utils.read_yaml(self.cluster_yaml)
            try:
                cluster_info = provision_lib.get_cluster_info(
                    provider_name,
                    region=self.launched_resources.region,
                    cluster_name_on_cloud=self.cluster_name_on_cloud,
                    provider_config=config.get('provider', None))
            except Exception as e:  # pylint: disable=broad-except
                # This could happen when the VM is not fully launched, and a
                # user is trying to terminate it with `sky down`.
                logger.debug('Failed to get cluster info for '
                             f'{self.cluster_name} from the new provisioner '
                             f'with {common_utils.format_exception(e)}.')
                raise exceptions.FetchClusterInfoError(
                    exceptions.FetchClusterInfoError.Reason.HEAD) from e
            if cluster_info.num_instances != self.launched_nodes:
                logger.debug(
                    f'Available nodes in the cluster {self.cluster_name} '
                    'do not match the number of nodes requested ('
                    f'{cluster_info.num_instances} != '
                    f'{self.launched_nodes}).')
                raise exceptions.FetchClusterInfoError(
                    exceptions.FetchClusterInfoError.Reason.HEAD)
            self.cached_cluster_info = cluster_info

    def update_cluster_ips(
            self,
            max_attempts: int = 1,
            internal_ips: Optional[List[Optional[str]]] = None,
            external_ips: Optional[List[Optional[str]]] = None,
            cluster_info: Optional[provision_common.ClusterInfo] = None
    ) -> None:
        """Updates the cluster IPs cached in the handle.

        We cache the cluster IPs in the handle to avoid having to retrieve
        them from the cloud provider every time we need them. This method
        updates the cached IPs.

        Optimizations:
            1) If the external IPs are provided (e.g. from the provision logs),
                we use them instead of retrieving them from the cloud provider.
            2) If the cached external IPs match the provided (fetched) external
                IPs, we don't need to update the internal IPs.
            3) If the internal IPs are provided (e.g. from the provision logs),
                we use them instead of retrieving them from the cloud provider.

        Args:
            max_attempts: The maximum number of attempts to get the head IP.
            internal_ips: The internal IPs to use for the cluster. It is an
                optimization to avoid retrieving the internal IPs from the
                cloud provider. Typically, it can be parsed from the provision
                logs.
            external_ips: The external IPs to use for the cluster. Similar to
                internal_ips, it is an optimization to avoid retrieving the
                external IPs from the cloud provider.

        Raises:
            exceptions.FetchClusterInfoError: if we failed to get the cluster
                infos. e.reason is HEAD or WORKER.
        """
        if cluster_info is not None:
            self.cached_cluster_info = cluster_info
            cluster_feasible_ips = self.cached_cluster_info.get_feasible_ips()
            cluster_internal_ips = self.cached_cluster_info.get_feasible_ips(
                force_internal_ips=True)
        else:
            # For clouds that do not support the SkyPilot Provisioner API.
            # TODO(zhwu): once all the clouds are migrated to SkyPilot
            # Provisioner API, we should remove this else block
            def is_provided_ips_valid(
                    ips: Optional[List[Optional[str]]]) -> bool:
                return (ips is not None and len(ips)
                        == self.num_ips_per_node * self.launched_nodes and
                        all(ip is not None for ip in ips))

            use_internal_ips = self._use_internal_ips()

            # cluster_feasible_ips is the list of IPs of the nodes in the
            # cluster which can be used to connect to the cluster. It is a list
            # of external IPs if the cluster is assigned public IPs, otherwise
            # it is a list of internal IPs.
            if is_provided_ips_valid(external_ips):
                logger.debug(f'Using provided external IPs: {external_ips}')
                cluster_feasible_ips = typing.cast(List[str], external_ips)
            else:
                cluster_feasible_ips = backend_utils.get_node_ips(
                    self.cluster_yaml,
                    self.launched_nodes,
                    head_ip_max_attempts=max_attempts,
                    worker_ip_max_attempts=max_attempts,
                    get_internal_ips=use_internal_ips)

            if self.cached_external_ips == cluster_feasible_ips:
                logger.debug(
                    'Skipping the fetching of internal IPs as the cached '
                    'external IPs matches the newly fetched ones.')
                # Optimization: If the cached external IPs are the same as the
                # retrieved feasible IPs, then we can skip retrieving internal
                # IPs since the cached IPs are up-to-date.
                return

            logger.debug(
                'Cached external IPs do not match with the newly fetched ones: '
                f'cached ({self.cached_external_ips}), new '
                f'({cluster_feasible_ips})')

            if use_internal_ips:
                # Optimization: if we know use_internal_ips is True (currently
                # only exposed for AWS and GCP), then our provisioner is
                # guaranteed to not assign public IPs, thus the first list of
                # IPs returned above are already private IPs. So skip the second
                # query.
                cluster_internal_ips = list(cluster_feasible_ips)
            elif is_provided_ips_valid(internal_ips):
                logger.debug(f'Using provided internal IPs: {internal_ips}')
                cluster_internal_ips = typing.cast(List[str], internal_ips)
            else:
                cluster_internal_ips = backend_utils.get_node_ips(
                    self.cluster_yaml,
                    self.launched_nodes,
                    head_ip_max_attempts=max_attempts,
                    worker_ip_max_attempts=max_attempts,
                    get_internal_ips=True)

        assert len(cluster_feasible_ips) == len(cluster_internal_ips), (
            f'Cluster {self.cluster_name!r}:'
            f'Expected same number of internal IPs {cluster_internal_ips}'
            f' and external IPs {cluster_feasible_ips}.')

        # List of (internal_ip, feasible_ip) tuples for all the nodes in the
        # cluster, sorted by the feasible ips. The feasible ips can be either
        # internal or external ips, depending on the use_internal_ips flag.
        internal_external_ips: List[Tuple[str, str]] = list(
            zip(cluster_internal_ips, cluster_feasible_ips))

        # Ensure head node is the first element, then sort based on the
        # external IPs for stableness. Skip for k8s nodes since pods
        # worker ids are already mapped.
        if (cluster_info is not None and
                cluster_info.provider_name == 'kubernetes'):
            stable_internal_external_ips = internal_external_ips
        else:
            stable_internal_external_ips = [internal_external_ips[0]] + sorted(
                internal_external_ips[1:], key=lambda x: x[1])
        self.stable_internal_external_ips = stable_internal_external_ips

    @functools.lru_cache()
    @timeline.event
    def get_command_runners(self,
                            force_cached: bool = False,
                            avoid_ssh_control: bool = False
                           ) -> List[command_runner.CommandRunner]:
        """Returns a list of command runners for the cluster."""
        ssh_credentials = backend_utils.ssh_credential_from_yaml(
            self.cluster_yaml, self.docker_user, self.ssh_user)
        if avoid_ssh_control:
            ssh_credentials.pop('ssh_control_name', None)
        updated_to_skypilot_provisioner_after_provisioned = (
            self.launched_resources.cloud.PROVISIONER_VERSION >=
            clouds.ProvisionerVersion.SKYPILOT and
            self.cached_external_ips is not None and
            self.cached_cluster_info is None)
        if updated_to_skypilot_provisioner_after_provisioned:
            logger.debug(
                f'{self.launched_resources.cloud} has been updated to the new '
                f'provisioner after cluster {self.cluster_name} was '
                f'provisioned. Cached IPs are used for connecting to the '
                'cluster.')
        if (clouds.ProvisionerVersion.RAY_PROVISIONER_SKYPILOT_TERMINATOR >=
                self.launched_resources.cloud.PROVISIONER_VERSION or
                updated_to_skypilot_provisioner_after_provisioned):
            ip_list = (self.cached_external_ips
                       if force_cached else self.external_ips())
            if ip_list is None:
                return []
            # Potentially refresh the external SSH ports, in case the existing
            # cluster before #2491 was launched without external SSH ports
            # cached.
            port_list = self.external_ssh_ports()
            runners = command_runner.SSHCommandRunner.make_runner_list(
                zip(ip_list, port_list), **ssh_credentials)
            return runners
        if self.cached_cluster_info is None:
            # We have `or self.cached_external_ips is None` here, because
            # when a cluster's cloud is just upgraded to the new provsioner,
            # although it has the cached_external_ips, the cached_cluster_info
            # can be None. We need to update it here, even when force_cached is
            # set to True.
            # TODO: We can remove `self.cached_external_ips is None` after
            # version 0.8.0.
            assert not force_cached or self.cached_external_ips is not None, (
                force_cached, self.cached_external_ips)
            self._update_cluster_info()
        assert self.cached_cluster_info is not None, self
        runners = provision_lib.get_command_runners(
            self.cached_cluster_info.provider_name, self.cached_cluster_info,
            **ssh_credentials)
        return runners

    @property
    def cached_internal_ips(self) -> Optional[List[str]]:
        if self.stable_internal_external_ips is not None:
            return [ips[0] for ips in self.stable_internal_external_ips]
        return None

    def internal_ips(self,
                     max_attempts: int = _FETCH_IP_MAX_ATTEMPTS) -> List[str]:
        internal_ips = self.cached_internal_ips
        if internal_ips is not None:
            return internal_ips
        self.update_cluster_ips(max_attempts=max_attempts)
        internal_ips = self.cached_internal_ips
        assert internal_ips is not None, 'update_cluster_ips failed.'
        return internal_ips

    @property
    def cached_external_ips(self) -> Optional[List[str]]:
        if self.stable_internal_external_ips is not None:
            return [ips[1] for ips in self.stable_internal_external_ips]
        return None

    def external_ips(self,
                     max_attempts: int = _FETCH_IP_MAX_ATTEMPTS) -> List[str]:
        external_ips = self.cached_external_ips
        if external_ips is not None:
            return external_ips
        self.update_cluster_ips(max_attempts=max_attempts)
        external_ips = self.cached_external_ips
        assert external_ips is not None, 'update_cluster_ips failed.'
        return external_ips

    @property
    def cached_external_ssh_ports(self) -> Optional[List[int]]:
        if self.stable_ssh_ports is not None:
            return self.stable_ssh_ports
        return None

    def external_ssh_ports(self,
                           max_attempts: int = _FETCH_IP_MAX_ATTEMPTS
                          ) -> List[int]:
        cached_ssh_ports = self.cached_external_ssh_ports
        if cached_ssh_ports is not None:
            return cached_ssh_ports
        self.update_ssh_ports(max_attempts=max_attempts)
        cached_ssh_ports = self.cached_external_ssh_ports
        assert cached_ssh_ports is not None, 'update_ssh_ports failed.'
        return cached_ssh_ports

    def get_hourly_price(self) -> float:
        hourly_cost = (self.launched_resources.get_cost(3600) *
                       self.launched_nodes)
        return hourly_cost

    def setup_docker_user(self, cluster_config_file: str):
        ip_list = self.external_ips()
        assert ip_list is not None
        docker_user = backend_utils.get_docker_user(ip_list[0],
                                                    cluster_config_file)
        self.docker_user = docker_user

    @property
    def cluster_yaml(self):
        return os.path.expanduser(self._cluster_yaml)

    @property
    def ssh_user(self):
        if self.cached_cluster_info is not None:
            # Overload ssh_user with the user stored in cluster_info, which is
            # useful for kubernetes case, where the ssh_user can depend on the
            # container image used. For those clusters launched with ray
            # autoscaler, we directly use the ssh_user in yaml config.
            return self.cached_cluster_info.ssh_user
        return None

    @property
    def head_ip(self):
        external_ips = self.cached_external_ips
        if external_ips is not None:
            return external_ips[0]
        return None

    @property
    def head_ssh_port(self):
        external_ssh_ports = self.cached_external_ssh_ports
        if external_ssh_ports:
            return external_ssh_ports[0]
        return None

    @property
    def num_ips_per_node(self) -> int:
        """Returns number of IPs per node in the cluster, handling TPU Pod."""
        is_tpu_vm_pod = gcp_utils.is_tpu_vm_pod(self.launched_resources)
        if is_tpu_vm_pod:
            num_ips = gcp_utils.get_num_tpu_devices(self.launched_resources)
        else:
            num_ips = 1
        return num_ips

    def __setstate__(self, state):
        self._version = self._VERSION

        version = state.pop('_version', None)
        if version is None:
            version = -1
            state.pop('cluster_region', None)
        if version < 2:
            state['_cluster_yaml'] = state.pop('cluster_yaml')
        if version < 3:
            head_ip = state.pop('head_ip', None)
            state['stable_internal_external_ips'] = None
        if version < 4:
            # Version 4 adds self.stable_ssh_ports for Kubernetes support
            state['stable_ssh_ports'] = None
        if version < 5:
            state['docker_user'] = None

        if version < 6:
            state['cluster_name_on_cloud'] = state['cluster_name']

        if version < 8:
            self.cached_cluster_info = None

        self.__dict__.update(state)

        # Because the update_cluster_ips and update_ssh_ports
        # functions use the handle, we call it on the current instance
        # after the state is updated.
        if version < 3 and head_ip is not None:
            try:
                self.update_cluster_ips()
            except exceptions.FetchClusterInfoError:
                # This occurs when an old cluster from was autostopped,
                # so the head IP in the database is not updated.
                pass
        if version < 4:
            self.update_ssh_ports()

        self._update_cluster_region()

        if version < 8:
            try:
                self._update_cluster_info()
            except exceptions.FetchClusterInfoError:
                # This occurs when an old cluster from was autostopped,
                # so the head IP in the database is not updated.
                pass


class CloudVmRayBackend(backends.Backend['CloudVmRayResourceHandle']):
    """Backend: runs on cloud virtual machines, managed by Ray.

    Changing this class may also require updates to:
      * Cloud providers' templates under config/
      * Cloud providers' implementations under clouds/
    """

    NAME = 'cloudvmray'

    # Backward compatibility, with the old name of the handle.
    ResourceHandle = CloudVmRayResourceHandle  # pylint: disable=invalid-name

    def __init__(self):
        self.run_timestamp = backend_utils.get_run_timestamp()
        # NOTE: do not expanduser() here, as this '~/...' path is used for
        # remote as well to be expanded on the remote side.
        self.log_dir = os.path.join(constants.SKY_LOGS_DIRECTORY,
                                    self.run_timestamp)
        # Do not make directories to avoid create folder for commands that
        # do not need it (`sky status`, `sky logs` ...)
        # os.makedirs(self.log_dir, exist_ok=True)

        self._dag = None
        self._optimize_target = None
        self._requested_features = set()

        # Command for running the setup script. It is only set when the
        # setup needs to be run outside the self._setup() and as part of
        # a job (--detach-setup).
        self._setup_cmd = None

    # --- Implementation of Backend APIs ---

    def register_info(self, **kwargs) -> None:
        self._dag = kwargs.pop('dag', self._dag)
        self._optimize_target = kwargs.pop(
            'optimize_target',
            self._optimize_target) or optimizer.OptimizeTarget.COST
        self._requested_features = kwargs.pop('requested_features',
                                              self._requested_features)
        assert len(kwargs) == 0, f'Unexpected kwargs: {kwargs}'

    def check_resources_fit_cluster(
        self,
        handle: CloudVmRayResourceHandle,
        task: task_lib.Task,
        check_ports: bool = False,
    ) -> resources_lib.Resources:
        """Check if resources requested by the task fit the cluster.

        The resources requested by the task should be smaller than the existing
        cluster.
        If multiple resources are specified, this checking will pass when
        at least one resource fits the cluster.

        Raises:
            exceptions.ResourcesMismatchError: If the resources in the task
                does not match the existing cluster.
        """

        launched_resources = handle.launched_resources
        cluster_name = handle.cluster_name

        # Usage Collection:
        usage_lib.messages.usage.update_cluster_resources(
            handle.launched_nodes, launched_resources)
        record = global_user_state.get_cluster_from_name(cluster_name)
        if record is not None:
            usage_lib.messages.usage.update_cluster_status(record['status'])

        # Backward compatibility: the old launched_resources without region info
        # was handled by ResourceHandle._update_cluster_region.
        assert launched_resources.region is not None, handle

        mismatch_str = (f'To fix: specify a new cluster name, or down the '
                        f'existing cluster first: sky down {cluster_name}')
        valid_resource = None
        requested_resource_list = []
        for resource in task.resources:
            if (task.num_nodes <= handle.launched_nodes and
                    resource.less_demanding_than(
                        launched_resources,
                        requested_num_nodes=task.num_nodes,
                        check_ports=check_ports)):
                valid_resource = resource
                break
            else:
                requested_resource_list.append(f'{task.num_nodes}x {resource}')

        if valid_resource is None:
            for example_resource in task.resources:
                if (example_resource.region is not None and
                        example_resource.region != launched_resources.region):
                    with ux_utils.print_exception_no_traceback():
                        raise exceptions.ResourcesMismatchError(
                            f'Task requested resources {example_resource} in region '  # pylint: disable=line-too-long
                            f'{example_resource.region!r}'
                            ', but the existing cluster '
                            f'is in region {launched_resources.region!r}.')
                if (example_resource.zone is not None and
                        example_resource.zone != launched_resources.zone):
                    zone_str = (f'is in zone {launched_resources.zone!r}.'
                                if launched_resources.zone is not None else
                                'does not have zone specified.')
                    with ux_utils.print_exception_no_traceback():
                        raise exceptions.ResourcesMismatchError(
                            f'Task requested resources {example_resource} in zone '  # pylint: disable=line-too-long
                            f'{example_resource.zone!r},'
                            'but the existing cluster '
                            f'{zone_str}')
                if (example_resource.requires_fuse and
                        not launched_resources.requires_fuse):
                    # Will not be reached for non-k8s case since the
                    # less_demanding_than only fails fuse requirement when
                    # the cloud is Kubernetes AND the cluster doesn't have fuse.
                    with ux_utils.print_exception_no_traceback():
                        raise exceptions.ResourcesMismatchError(
                            'Task requires FUSE support for mounting object '
                            'stores, but the existing cluster with '
                            f'{launched_resources!r} does not support FUSE '
                            f'mounting. Launch a new cluster to run this task.')
            requested_resource_str = ', '.join(requested_resource_list)
            if isinstance(task.resources, list):
                requested_resource_str = f'[{requested_resource_str}]'
            elif isinstance(task.resources, set):
                requested_resource_str = f'{{{requested_resource_str}}}'
            with ux_utils.print_exception_no_traceback():
                raise exceptions.ResourcesMismatchError(
                    'Requested resources do not match the existing '
                    'cluster.\n'
                    f'  Requested:\t{requested_resource_str}\n'
                    f'  Existing:\t{handle.launched_nodes}x '
                    f'{handle.launched_resources}\n'
                    f'{mismatch_str}')
        return valid_resource

    def _provision(
            self,
            task: task_lib.Task,
            to_provision: Optional[resources_lib.Resources],
            dryrun: bool,
            stream_logs: bool,
            cluster_name: str,
            retry_until_up: bool = False) -> Optional[CloudVmRayResourceHandle]:
        """Provisions using 'ray up'.

        Raises:
            exceptions.ClusterOwnerIdentityMismatchError: if the cluster
                'cluster_name' exists and is owned by another user.
            exceptions.InvalidClusterNameError: if the cluster name is invalid.
            exceptions.ResourcesMismatchError: if the requested resources
                do not match the existing cluster.
            exceptions.ResourcesUnavailableError: if the requested resources
                cannot be satisfied. The failover_history of the exception
                will be set as at least 1 exception from either our pre-checks
                (e.g., cluster name invalid) or a region/zone throwing
                resource unavailability.
            exceptions.CommandError: any ssh command error.
            RuntimeErorr: raised when 'rsync' is not installed.
            # TODO(zhwu): complete the list of exceptions.
        """
        # FIXME: ray up for Azure with different cluster_names will overwrite
        # each other.
        # When rsync is not installed in the user's machine, Ray will
        # silently retry to up the node for _MAX_RAY_UP_RETRY number
        # of times. This is time consuming so we fail early.
        backend_utils.check_rsync_installed()
        # Check if the cluster is owned by the current user. Raise
        # exceptions.ClusterOwnerIdentityMismatchError
        backend_utils.check_owner_identity(cluster_name)
        lock_path = os.path.expanduser(
            backend_utils.CLUSTER_STATUS_LOCK_PATH.format(cluster_name))
        with timeline.FileLockEvent(lock_path):
            # Try to launch the exiting cluster first. If no existing cluster,
            # this function will create a to_provision_config with required
            # resources.
            to_provision_config = self._check_existing_cluster(
                task, to_provision, cluster_name, dryrun)
            assert to_provision_config.resources is not None, (
                'to_provision should not be None', to_provision_config)

            prev_cluster_status = to_provision_config.prev_cluster_status
            usage_lib.messages.usage.update_cluster_resources(
                to_provision_config.num_nodes, to_provision_config.resources)
            usage_lib.messages.usage.update_cluster_status(prev_cluster_status)

            # TODO(suquark): once we have sky on PyPI, we should directly
            # install sky from PyPI.
            # NOTE: can take ~2s.
            with timeline.Event('backend.provision.wheel_build'):
                # TODO(suquark): once we have sky on PyPI, we should directly
                # install sky from PyPI.
                local_wheel_path, wheel_hash = wheel_utils.build_sky_wheel()
                # The most frequent reason for the failure of a provision
                # request is resource unavailability instead of rate
                # limiting; to make users wait shorter, we do not make
                # backoffs exponential.
                backoff = common_utils.Backoff(
                    initial_backoff=_RETRY_UNTIL_UP_INIT_GAP_SECONDS,
                    max_backoff_factor=1)
            attempt_cnt = 1
            while True:
                # For on-demand instances, RetryingVmProvisioner will retry
                # within the given region first, then optionally retry on all
                # other clouds and regions (if backend.register_info()
                # has been called).
                # For spot instances, each provisioning request is made for a
                # single zone and the provisioner will retry on all other
                # clouds, regions, and zones.
                # See optimizer.py#_make_launchables_for_valid_region_zones()
                # for detailed reasons.

                # After this "round" of optimization across clouds, provisioning
                # may still have not succeeded. This while loop will then kick
                # in if retry_until_up is set, which will kick off new "rounds"
                # of optimization infinitely.
                try:
                    retry_provisioner = RetryingVmProvisioner(
                        self.log_dir,
                        self._dag,
                        self._optimize_target,
                        self._requested_features,
                        local_wheel_path,
                        wheel_hash,
                        blocked_resources=task.blocked_resources)
                    config_dict = retry_provisioner.provision_with_retries(
                        task, to_provision_config, dryrun, stream_logs)
                    break
                except exceptions.ResourcesUnavailableError as e:
                    # Do not remove the stopped cluster from the global state
                    # if failed to start.
                    if e.no_failover:
                        error_message = str(e)
                    else:
                        # Clean up the cluster's entry in `sky status`.
                        global_user_state.remove_cluster(cluster_name,
                                                         terminate=True)
                        usage_lib.messages.usage.update_final_cluster_status(
                            None)
                        error_message = (
                            'Failed to provision all possible launchable '
                            'resources.'
                            f' Relax the task\'s resource requirements: '
                            f'{task.num_nodes}x {list(task.resources)[0]}')
                    if retry_until_up:
                        logger.error(error_message)
                        # Sleep and retry.
                        gap_seconds = backoff.current_backoff()
                        plural = 's' if attempt_cnt > 1 else ''
                        logger.info(
                            f'{colorama.Style.BRIGHT}=== Retry until up ==='
                            f'{colorama.Style.RESET_ALL}\n'
                            f'Retrying provisioning after {gap_seconds:.0f}s '
                            '(backoff with random jittering). '
                            f'Already tried {attempt_cnt} attempt{plural}.')
                        attempt_cnt += 1
                        time.sleep(gap_seconds)
                        continue
                    error_message += (
                        '\nTo keep retrying until the cluster is up, use the '
                        '`--retry-until-up` flag.')
                    with ux_utils.print_exception_no_traceback():
                        raise exceptions.ResourcesUnavailableError(
                            error_message,
                            failover_history=e.failover_history) from None
            if dryrun:
                record = global_user_state.get_cluster_from_name(cluster_name)
                return record['handle'] if record is not None else None

            if 'provision_record' in config_dict:
                # New provisioner is used here.
                handle = config_dict['handle']
                provision_record = config_dict['provision_record']
                resources_vars = config_dict['resources_vars']

                # Setup SkyPilot runtime after the cluster is provisioned
                # 1. Wait for SSH to be ready.
                # 2. Mount the cloud credentials, skypilot wheel,
                #    and other necessary files to the VM.
                # 3. Run setup commands to install dependencies.
                # 4. Starting ray cluster and skylet.
                cluster_info = provisioner.post_provision_runtime_setup(
                    repr(handle.launched_resources.cloud),
                    resources_utils.ClusterName(handle.cluster_name,
                                                handle.cluster_name_on_cloud),
                    handle.cluster_yaml,
                    provision_record=provision_record,
                    custom_resource=resources_vars.get('custom_resources'),
                    log_dir=self.log_dir)
                # We use the IPs from the cluster_info to update_cluster_ips,
                # when the provisioning is done, to make sure the cluster IPs
                # are up-to-date.
                # The staled IPs may be caused by the node being restarted
                # manually or by the cloud provider.
                # Optimize the case where the cluster's IPs can be retrieved
                # from cluster_info.
                handle.docker_user = cluster_info.docker_user
                handle.update_cluster_ips(max_attempts=_FETCH_IP_MAX_ATTEMPTS,
                                          cluster_info=cluster_info)
                handle.update_ssh_ports(max_attempts=_FETCH_IP_MAX_ATTEMPTS)

                # Update launched resources.
                handle.launched_resources = handle.launched_resources.copy(
                    region=provision_record.region, zone=provision_record.zone)

                self._update_after_cluster_provisioned(
                    handle, to_provision_config.prev_handle, task,
                    prev_cluster_status, handle.external_ips(),
                    handle.external_ssh_ports(), lock_path)
                return handle

            cluster_config_file = config_dict['ray']
            handle = config_dict['handle']

            ip_list = handle.external_ips()
            ssh_port_list = handle.external_ssh_ports()
            assert ip_list is not None, handle
            assert ssh_port_list is not None, handle

            config = common_utils.read_yaml(cluster_config_file)
            if 'docker' in config:
                handle.setup_docker_user(cluster_config_file)

            # Get actual zone info and save it into handle.
            # NOTE: querying zones is expensive, observed 1node GCP >=4s.
            zone = handle.launched_resources.zone
            if zone is None:
                get_zone_cmd = (
                    handle.launched_resources.cloud.get_zone_shell_cmd())
                # zone is None for Azure
                if get_zone_cmd is not None:
                    runners = handle.get_command_runners()

                    def _get_zone(runner):
                        retry_count = 0
                        backoff = common_utils.Backoff(initial_backoff=1,
                                                       max_backoff_factor=3)
                        while True:
                            returncode, stdout, stderr = runner.run(
                                get_zone_cmd,
                                require_outputs=True,
                                stream_logs=False)
                            if returncode == 0:
                                break
                            retry_count += 1
                            if retry_count <= _MAX_GET_ZONE_RETRY:
                                time.sleep(backoff.current_backoff())
                                continue
                        subprocess_utils.handle_returncode(
                            returncode,
                            get_zone_cmd,
                            f'Failed to get zone for {cluster_name!r}',
                            stderr=stderr,
                            stream_logs=stream_logs)
                        return stdout.strip()

                    zones = subprocess_utils.run_in_parallel(_get_zone, runners)
                    if len(set(zones)) == 1:
                        # zone will be checked during Resources cls
                        # initialization.
                        handle.launched_resources = (
                            handle.launched_resources.copy(zone=zones[0]))
                    # If the number of zones > 1, nodes in the cluster are
                    # launched in different zones (legacy clusters before
                    # #1700), leave the zone field of handle.launched_resources
                    # to None.

            # For backward compatibility and robustness of skylet, it is checked
            # and restarted if necessary.
            logger.debug('Checking if skylet is running on the head node.')
            with rich_utils.safe_status(
                    '[bold cyan]Preparing SkyPilot runtime'):
                # We need to source bashrc for skylet to make sure the autostop
                # event can access the path to the cloud CLIs.
                self.run_on_head(handle,
                                 instance_setup.MAYBE_SKYLET_RESTART_CMD,
                                 source_bashrc=True)

            self._update_after_cluster_provisioned(
                handle, to_provision_config.prev_handle, task,
                prev_cluster_status, ip_list, ssh_port_list, lock_path)
            return handle

    def _open_ports(self, handle: CloudVmRayResourceHandle) -> None:
        cloud = handle.launched_resources.cloud
        logger.debug(
            f'Opening ports {handle.launched_resources.ports} for {cloud}')
        config = common_utils.read_yaml(handle.cluster_yaml)
        provider_config = config['provider']
        provision_lib.open_ports(repr(cloud), handle.cluster_name_on_cloud,
                                 handle.launched_resources.ports,
                                 provider_config)

    def _update_after_cluster_provisioned(
            self, handle: CloudVmRayResourceHandle,
            prev_handle: Optional[CloudVmRayResourceHandle],
            task: task_lib.Task,
            prev_cluster_status: Optional[status_lib.ClusterStatus],
            ip_list: List[str], ssh_port_list: List[int],
            lock_path: str) -> None:
        usage_lib.messages.usage.update_cluster_resources(
            handle.launched_nodes, handle.launched_resources)
        usage_lib.messages.usage.update_final_cluster_status(
            status_lib.ClusterStatus.UP)

        # Update job queue to avoid stale jobs (when restarted), before
        # setting the cluster to be ready.
        if prev_cluster_status == status_lib.ClusterStatus.INIT:
            # update_status will query the ray job status for all INIT /
            # PENDING / RUNNING jobs for the real status, since we do not
            # know the actual previous status of the cluster.
            cmd = job_lib.JobLibCodeGen.update_status()
            logger.debug('Update job queue on remote cluster.')
            with rich_utils.safe_status(
                    '[bold cyan]Preparing SkyPilot runtime'):
                returncode, _, stderr = self.run_on_head(handle,
                                                         cmd,
                                                         require_outputs=True)
            subprocess_utils.handle_returncode(returncode, cmd,
                                               'Failed to update job status.',
                                               stderr)
        if prev_cluster_status == status_lib.ClusterStatus.STOPPED:
            # Safely set all the previous jobs to FAILED since the cluster
            # is restarted
            # An edge case here due to racing:
            # 1. A job finishes RUNNING, but right before it update itself
            # to SUCCEEDED, the cluster is STOPPED by `sky stop`.
            # 2. On next `sky start`, it gets reset to FAILED.
            cmd = job_lib.JobLibCodeGen.fail_all_jobs_in_progress()
            returncode, stdout, stderr = self.run_on_head(handle,
                                                          cmd,
                                                          require_outputs=True)
            subprocess_utils.handle_returncode(
                returncode, cmd,
                'Failed to set previously in-progress jobs to FAILED',
                stdout + stderr)

        prev_ports = None
        if prev_handle is not None:
            prev_ports = prev_handle.launched_resources.ports
        current_ports = handle.launched_resources.ports
        open_new_ports = bool(
            resources_utils.port_ranges_to_set(current_ports) -
            resources_utils.port_ranges_to_set(prev_ports))
        if open_new_ports:
            cloud = handle.launched_resources.cloud
            if not (cloud.OPEN_PORTS_VERSION <=
                    clouds.OpenPortsVersion.LAUNCH_ONLY):
                with rich_utils.safe_status(
                        '[bold cyan]Launching - Opening new ports'):
                    self._open_ports(handle)

        with timeline.Event('backend.provision.post_process'):
            global_user_state.add_or_update_cluster(
                handle.cluster_name,
                handle,
                set(task.resources),
                ready=True,
            )
            usage_lib.messages.usage.update_final_cluster_status(
                status_lib.ClusterStatus.UP)
            auth_config = backend_utils.ssh_credential_from_yaml(
                handle.cluster_yaml,
                ssh_user=handle.ssh_user,
                docker_user=handle.docker_user)
            backend_utils.SSHConfigHelper.add_cluster(handle.cluster_name,
                                                      ip_list, auth_config,
                                                      ssh_port_list,
                                                      handle.docker_user,
                                                      handle.ssh_user)

            common_utils.remove_file_if_exists(lock_path)

    def _sync_workdir(self, handle: CloudVmRayResourceHandle,
                      workdir: Path) -> None:
        # Even though provision() takes care of it, there may be cases where
        # this function is called in isolation, without calling provision(),
        # e.g., in CLI.  So we should rerun rsync_up.
        fore = colorama.Fore
        style = colorama.Style
        ip_list = handle.external_ips()
        assert ip_list is not None, 'external_ips is not cached in handle'
        full_workdir = os.path.abspath(os.path.expanduser(workdir))

        # These asserts have been validated at Task construction time.
        assert os.path.exists(full_workdir), f'{full_workdir} does not exist'
        if os.path.islink(full_workdir):
            logger.warning(
                f'{fore.YELLOW}Workdir {workdir!r} is a symlink. '
                f'Symlink contents are not uploaded.{style.RESET_ALL}')
        else:
            assert os.path.isdir(
                full_workdir), f'{full_workdir} should be a directory.'

        # Raise warning if directory is too large
        dir_size = backend_utils.path_size_megabytes(full_workdir)
        if dir_size >= _PATH_SIZE_MEGABYTES_WARN_THRESHOLD:
            logger.warning(
                f'{fore.YELLOW}The size of workdir {workdir!r} '
                f'is {dir_size} MB. Try to keep workdir small or use '
                '.gitignore to exclude large files, as large sizes will slow '
                f'down rsync.{style.RESET_ALL}')

        log_path = os.path.join(self.log_dir, 'workdir_sync.log')

        # TODO(zhwu): refactor this with backend_utils.parallel_cmd_with_rsync
        runners = handle.get_command_runners()

        def _sync_workdir_node(runner: command_runner.CommandRunner) -> None:
            runner.rsync(
                source=workdir,
                target=SKY_REMOTE_WORKDIR,
                up=True,
                log_path=log_path,
                stream_logs=False,
            )

        num_nodes = handle.launched_nodes
        plural = 's' if num_nodes > 1 else ''
        logger.info(
            f'{fore.CYAN}Syncing workdir (to {num_nodes} node{plural}): '
            f'{style.BRIGHT}{workdir}{style.RESET_ALL}'
            f' -> '
            f'{style.BRIGHT}{SKY_REMOTE_WORKDIR}{style.RESET_ALL}')
        os.makedirs(os.path.expanduser(self.log_dir), exist_ok=True)
        os.system(f'touch {log_path}')
        tail_cmd = f'tail -n100 -f {log_path}'
        logger.info('To view detailed progress: '
                    f'{style.BRIGHT}{tail_cmd}{style.RESET_ALL}')
        with rich_utils.safe_status('[bold cyan]Syncing[/]'):
            subprocess_utils.run_in_parallel(_sync_workdir_node, runners)

    def _sync_file_mounts(
        self,
        handle: CloudVmRayResourceHandle,
        all_file_mounts: Optional[Dict[Path, Path]],
        storage_mounts: Optional[Dict[Path, storage_lib.Storage]],
    ) -> None:
        """Mounts all user files to the remote nodes."""
        controller_utils.replace_skypilot_config_path_in_file_mounts(
            handle.launched_resources.cloud, all_file_mounts)
        self._execute_file_mounts(handle, all_file_mounts)
        self._execute_storage_mounts(handle, storage_mounts)
        self._set_storage_mounts_metadata(handle.cluster_name, storage_mounts)

    def _setup(self, handle: CloudVmRayResourceHandle, task: task_lib.Task,
               detach_setup: bool) -> None:
        start = time.time()
        style = colorama.Style
        fore = colorama.Fore

        if task.setup is None:
            return
        setup = task.setup
        # Sync the setup script up and run it.
        internal_ips = handle.internal_ips()
        remote_setup_file_name = f'/tmp/sky_setup_{self.run_timestamp}'
        # Need this `-i` option to make sure `source ~/.bashrc` work
        setup_cmd = f'/bin/bash -i {remote_setup_file_name} 2>&1'
        runners = handle.get_command_runners(avoid_ssh_control=True)

        def _setup_node(node_id: int) -> None:
            setup_envs = task.envs.copy()
            setup_envs.update(self._skypilot_predefined_env_vars(handle))
            setup_envs['SKYPILOT_SETUP_NODE_IPS'] = '\n'.join(internal_ips)
            setup_envs['SKYPILOT_SETUP_NODE_RANK'] = str(node_id)
            runner = runners[node_id]
            setup_script = log_lib.make_task_bash_script(setup,
                                                         env_vars=setup_envs)
            encoded_script = shlex.quote(setup_script)

            def _dump_setup_script(setup_script: str) -> None:
                with tempfile.NamedTemporaryFile('w', prefix='sky_setup_') as f:
                    f.write(setup_script)
                    f.flush()
                    setup_sh_path = f.name
                    runner.rsync(source=setup_sh_path,
                                 target=remote_setup_file_name,
                                 up=True,
                                 stream_logs=False)

            if detach_setup or _is_command_length_over_limit(encoded_script):
                _dump_setup_script(setup_script)
                create_script_code = 'true'
            else:
                create_script_code = (f'{{ echo {encoded_script} > '
                                      f'{remote_setup_file_name}; }}')

            if detach_setup:
                return

            setup_log_path = os.path.join(self.log_dir,
                                          f'setup-{runner.node_id}.log')

            def _run_setup(setup_cmd: str) -> int:
                returncode = runner.run(
                    setup_cmd,
                    log_path=setup_log_path,
                    process_stream=False,
                    # We do not source bashrc for setup, since bashrc is sourced
                    # in the script already.
                    # Skip an empty line and two lines due to the /bin/bash -i
                    # and source ~/.bashrc in the setup_cmd.
                    #   bash: cannot set terminal process group (7398): Inappropriate ioctl for device # pylint: disable=line-too-long
                    #   bash: no job control in this shell
                    skip_lines=3)
                return returncode

            returncode = _run_setup(f'{create_script_code} && {setup_cmd}',)
            if returncode == 255:
                is_message_too_long = False
                with open(setup_log_path, 'r', encoding='utf-8') as f:
                    if 'too long' in f.read():
                        is_message_too_long = True

                if is_message_too_long:
                    # If the setup script is too long, we retry it with dumping
                    # the script to a file and running it with SSH. We use a
                    # general length limit check before but it could be
                    # inaccurate on some systems.
                    logger.debug(
                        'Failed to run setup command inline due to '
                        'command length limit. Dumping setup script to '
                        'file and running it with SSH.')
                    _dump_setup_script(setup_script)
                    returncode = _run_setup(setup_cmd)

            def error_message() -> str:
                # Use the function to avoid tailing the file in success case
                try:
                    last_10_lines = subprocess.run(
                        ['tail', '-n10',
                         os.path.expanduser(setup_log_path)],
                        stdout=subprocess.PIPE,
                        check=True).stdout.decode('utf-8')
                except subprocess.CalledProcessError:
                    last_10_lines = None

                err_msg = (f'Failed to setup with return code {returncode}. '
                           f'Check the details in log: {setup_log_path}')
                if last_10_lines:
                    err_msg += (f'\n\n{colorama.Fore.RED}'
                                '****** START Last lines of setup output ******'
                                f'{colorama.Style.RESET_ALL}\n'
                                f'{last_10_lines}'
                                f'{colorama.Fore.RED}'
                                '******* END Last lines of setup output *******'
                                f'{colorama.Style.RESET_ALL}')
                return err_msg

            subprocess_utils.handle_returncode(returncode=returncode,
                                               command=setup_cmd,
                                               error_msg=error_message)

        num_nodes = len(runners)
        plural = 's' if num_nodes > 1 else ''
        if not detach_setup:
            logger.info(f'{fore.CYAN}Running setup on {num_nodes} node{plural}.'
                        f'{style.RESET_ALL}')
        # TODO(zhwu): run_in_parallel uses multi-thread to run the commands,
        # which can cause the program waiting for all the threads to finish,
        # even if some of them raise exceptions. We should replace it with
        # multi-process.
        subprocess_utils.run_in_parallel(_setup_node, range(num_nodes))

        if detach_setup:
            # Only set this when setup needs to be run outside the self._setup()
            # as part of a job (--detach-setup).
            self._setup_cmd = setup_cmd
            return
        logger.info(f'{fore.GREEN}Setup completed.{style.RESET_ALL}')
        end = time.time()
        logger.debug(f'Setup took {end - start} seconds.')

    def _exec_code_on_head(
        self,
        handle: CloudVmRayResourceHandle,
        codegen: str,
        job_id: int,
        detach_run: bool = False,
        managed_job_dag: Optional['dag.Dag'] = None,
    ) -> None:
        """Executes generated code on the head node."""
        style = colorama.Style
        fore = colorama.Fore

        script_path = os.path.join(SKY_REMOTE_APP_DIR, f'sky_job_{job_id}')
        remote_log_dir = self.log_dir
        remote_log_path = os.path.join(remote_log_dir, 'run.log')

        cd = f'cd {SKY_REMOTE_WORKDIR}'

        mkdir_code = (f'{cd} && mkdir -p {remote_log_dir} && '
                      f'touch {remote_log_path}')
        encoded_script = shlex.quote(codegen)
        create_script_code = (f'{{ echo {encoded_script} > {script_path}; }}')
        job_submit_cmd = (
            f'RAY_DASHBOARD_PORT=$({constants.SKY_PYTHON_CMD} -c "from sky.skylet import job_lib; print(job_lib.get_job_submission_port())" 2> /dev/null || echo 8265);'  # pylint: disable=line-too-long
            f'{cd} && {constants.SKY_RAY_CMD} job submit '
            '--address=http://127.0.0.1:$RAY_DASHBOARD_PORT '
            f'--submission-id {job_id}-$(whoami) --no-wait '
            # Redirect stderr to /dev/null to avoid distracting error from ray.
            f'"{constants.SKY_PYTHON_CMD} -u {script_path} > {remote_log_path} '
            '2> /dev/null"')

        code = job_lib.JobLibCodeGen.queue_job(job_id, job_submit_cmd)
        job_submit_cmd = ' && '.join([mkdir_code, create_script_code, code])

        def _dump_code_to_file(codegen: str) -> None:
            runners = handle.get_command_runners()
            head_runner = runners[0]
            with tempfile.NamedTemporaryFile('w', prefix='sky_app_') as fp:
                fp.write(codegen)
                fp.flush()
                script_path = os.path.join(SKY_REMOTE_APP_DIR,
                                           f'sky_job_{job_id}')
                # We choose to sync code + exec, because the alternative of 'ray
                # submit' may not work as it may use system python (python2) to
                # execute the script. Happens for AWS.
                head_runner.rsync(source=fp.name,
                                  target=script_path,
                                  up=True,
                                  stream_logs=False)

        if _is_command_length_over_limit(job_submit_cmd):
            _dump_code_to_file(codegen)
            job_submit_cmd = f'{mkdir_code} && {code}'

        if managed_job_dag is not None:
            # Add the managed job to job queue database.
            managed_job_codegen = managed_jobs.ManagedJobCodeGen()
            managed_job_code = managed_job_codegen.set_pending(
                job_id, managed_job_dag)
            # Set the managed job to PENDING state to make sure that this
            # managed job appears in the `sky jobs queue`, when there are
            # already 2x vCPU controller processes running on the controller VM,
            # e.g., 16 controller processes running on a controller with 8
            # vCPUs.
            # The managed job should be set to PENDING state *after* the
            # controller process job has been queued, as our skylet on spot
            # controller will set the managed job in FAILED state if the
            # controller process job does not exist.
            # We cannot set the managed job to PENDING state in the codegen for
            # the controller process job, as it will stay in the job pending
            # table and not be executed until there is an empty slot.
            job_submit_cmd = job_submit_cmd + ' && ' + managed_job_code

        returncode, stdout, stderr = self.run_on_head(handle,
                                                      job_submit_cmd,
                                                      stream_logs=False,
                                                      require_outputs=True)
        if returncode == 255 and 'too long' in stdout + stderr:
            # If the generated script is too long, we retry it with dumping
            # the script to a file and running it with SSH. We use a general
            # length limit check before but it could be inaccurate on some
            # systems.
            logger.debug('Failed to submit job due to command length limit. '
                         'Dumping job to file and running it with SSH.')
            _dump_code_to_file(codegen)
            job_submit_cmd = f'{mkdir_code} && {code}'
            returncode, stdout, stderr = self.run_on_head(handle,
                                                          job_submit_cmd,
                                                          stream_logs=False,
                                                          require_outputs=True)

        # Happens when someone calls `sky exec` but remote is outdated
        # necessitating calling `sky launch`.
        backend_utils.check_stale_runtime_on_remote(returncode, stdout,
                                                    handle.cluster_name)
        subprocess_utils.handle_returncode(returncode,
                                           job_submit_cmd,
                                           f'Failed to submit job {job_id}.',
                                           stderr=stdout + stderr)

        logger.info('Job submitted with Job ID: '
                    f'{style.BRIGHT}{job_id}{style.RESET_ALL}')

        try:
            if not detach_run:
                if (handle.cluster_name in controller_utils.Controllers.
                        JOBS_CONTROLLER.value.candidate_cluster_names):
                    self.tail_managed_job_logs(handle, job_id)
                else:
                    # Sky logs. Not using subprocess.run since it will make the
                    # ssh keep connected after ctrl-c.
                    self.tail_logs(handle, job_id)
        finally:
            name = handle.cluster_name
            controller = controller_utils.Controllers.from_name(name)
            if controller == controller_utils.Controllers.JOBS_CONTROLLER:
                logger.info(
                    f'{fore.CYAN}Managed Job ID: '
                    f'{style.BRIGHT}{job_id}{style.RESET_ALL}'
                    '\nTo cancel the job:\t\t'
                    f'{backend_utils.BOLD}sky jobs cancel {job_id}'
                    f'{backend_utils.RESET_BOLD}'
                    '\nTo stream job logs:\t\t'
                    f'{backend_utils.BOLD}sky jobs logs {job_id}'
                    f'{backend_utils.RESET_BOLD}'
                    f'\nTo stream controller logs:\t'
                    f'{backend_utils.BOLD}sky jobs logs --controller {job_id}'
                    f'{backend_utils.RESET_BOLD}'
                    '\nTo view all managed jobs:\t'
                    f'{backend_utils.BOLD}sky jobs queue'
                    f'{backend_utils.RESET_BOLD}'
                    '\nTo view managed job dashboard:\t'
                    f'{backend_utils.BOLD}sky jobs dashboard'
                    f'{backend_utils.RESET_BOLD}')
            elif controller is None:
                logger.info(f'{fore.CYAN}Job ID: '
                            f'{style.BRIGHT}{job_id}{style.RESET_ALL}'
                            '\nTo cancel the job:\t'
                            f'{backend_utils.BOLD}sky cancel {name} {job_id}'
                            f'{backend_utils.RESET_BOLD}'
                            '\nTo stream job logs:\t'
                            f'{backend_utils.BOLD}sky logs {name} {job_id}'
                            f'{backend_utils.RESET_BOLD}'
                            '\nTo view the job queue:\t'
                            f'{backend_utils.BOLD}sky queue {name}'
                            f'{backend_utils.RESET_BOLD}')

    def _add_job(self, handle: CloudVmRayResourceHandle,
                 job_name: Optional[str], resources_str: str) -> int:
        username = getpass.getuser()
        code = job_lib.JobLibCodeGen.add_job(job_name, username,
                                             self.run_timestamp, resources_str)
        returncode, job_id_str, stderr = self.run_on_head(handle,
                                                          code,
                                                          stream_logs=False,
                                                          require_outputs=True,
                                                          separate_stderr=True)
        # TODO(zhwu): this sometimes will unexpectedly fail, we can add
        # retry for this, after we figure out the reason.
        subprocess_utils.handle_returncode(returncode, code,
                                           'Failed to fetch job id.', stderr)
        try:
            job_id_match = _JOB_ID_PATTERN.search(job_id_str)
            if job_id_match is not None:
                job_id = int(job_id_match.group(1))
            else:
                # For backward compatibility.
                job_id = int(job_id_str)
        except ValueError as e:
            logger.error(stderr)
            raise ValueError(f'Failed to parse job id: {job_id_str}; '
                             f'Returncode: {returncode}') from e
        return job_id

    def _execute(
        self,
        handle: CloudVmRayResourceHandle,
        task: task_lib.Task,
        detach_run: bool,
        dryrun: bool = False,
    ) -> Optional[int]:
        """Executes the task on the cluster.

        Returns:
            Job id if the task is submitted to the cluster, None otherwise.
        """
        if task.run is None:
            logger.info('Run commands not specified or empty.')
            return None
        # Check the task resources vs the cluster resources. Since `sky exec`
        # will not run the provision and _check_existing_cluster
        # We need to check ports here since sky.exec shouldn't change resources
        valid_resource = self.check_resources_fit_cluster(handle,
                                                          task,
                                                          check_ports=True)
        task_copy = copy.copy(task)
        # Handle multiple resources exec case.
        task_copy.set_resources(valid_resource)
        if len(task.resources) > 1:
            logger.info('Multiple resources are specified '
                        f'for the task, using: {valid_resource}')
        task_copy.best_resources = None
        resources_str = backend_utils.get_task_resources_str(task_copy)

        if dryrun:
            logger.info(f'Dryrun complete. Would have run:\n{task}')
            return None

        job_id = self._add_job(handle, task_copy.name, resources_str)

        num_actual_nodes = task.num_nodes * handle.num_ips_per_node
        # Case: task_lib.Task(run, num_nodes=N) or TPU VM Pods
        if num_actual_nodes > 1:
            self._execute_task_n_nodes(handle, task_copy, job_id, detach_run)
        else:
            # Case: task_lib.Task(run, num_nodes=1)
            self._execute_task_one_node(handle, task_copy, job_id, detach_run)

        return job_id

    def _post_execute(self, handle: CloudVmRayResourceHandle,
                      down: bool) -> None:
        fore = colorama.Fore
        style = colorama.Style
        name = handle.cluster_name
        controller = controller_utils.Controllers.from_name(name)
        if controller is not None or down:
            return
        stop_str = ('\nTo stop the cluster:'
                    f'\t{backend_utils.BOLD}sky stop {name}'
                    f'{backend_utils.RESET_BOLD}')
        logger.info(f'\n{fore.CYAN}Cluster name: '
                    f'{style.BRIGHT}{name}{style.RESET_ALL}'
                    '\nTo log into the head VM:\t'
                    f'{backend_utils.BOLD}ssh {name}'
                    f'{backend_utils.RESET_BOLD}'
                    '\nTo submit a job:'
                    f'\t\t{backend_utils.BOLD}sky exec {name} yaml_file'
                    f'{backend_utils.RESET_BOLD}'
                    f'{stop_str}'
                    '\nTo teardown the cluster:'
                    f'\t{backend_utils.BOLD}sky down {name}'
                    f'{backend_utils.RESET_BOLD}')
        if (gcp_utils.is_tpu(handle.launched_resources) and
                not gcp_utils.is_tpu_vm(handle.launched_resources)):
            logger.info('Tip: `sky down` will delete launched TPU(s) too.')

    def _teardown_ephemeral_storage(self, task: task_lib.Task) -> None:
        storage_mounts = task.storage_mounts
        if storage_mounts is not None:
            for _, storage in storage_mounts.items():
                if not storage.persistent:
                    storage.delete()

    def _teardown(self,
                  handle: CloudVmRayResourceHandle,
                  terminate: bool,
                  purge: bool = False):
        """Tear down or stop the cluster.

        Args:
            handle: The handle to the cluster.
            terminate: Terminate or stop the cluster.
            purge: Purge the cluster record from the cluster table, even if
                the teardown fails.
        Raises:
            exceptions.ClusterOwnerIdentityMismatchError: If the cluster is
                owned by another user.
            exceptions.CloudUserIdentityError: if we fail to get the current
                user identity.
            RuntimeError: If the cluster fails to be terminated/stopped.
        """
        cluster_name = handle.cluster_name
        # Check if the cluster is owned by the current user. Raise
        # exceptions.ClusterOwnerIdentityMismatchError
        yellow = colorama.Fore.YELLOW
        reset = colorama.Style.RESET_ALL
        is_identity_mismatch_and_purge = False
        try:
            backend_utils.check_owner_identity(cluster_name)
        except exceptions.ClusterOwnerIdentityMismatchError as e:
            if purge:
                logger.error(e)
                verbed = 'terminated' if terminate else 'stopped'
                logger.warning(
                    f'{yellow}Purge (-p/--purge) is set, ignoring the '
                    f'identity mismatch error and removing '
                    f'the cluster record from cluster table.{reset}\n{yellow}It'
                    ' is the user\'s responsibility to ensure that this '
                    f'cluster is actually {verbed} on the cloud.{reset}')
                is_identity_mismatch_and_purge = True
            else:
                raise

        lock_path = os.path.expanduser(
            backend_utils.CLUSTER_STATUS_LOCK_PATH.format(cluster_name))

        try:
            # TODO(mraheja): remove pylint disabling when filelock
            # version updated
            # pylint: disable=abstract-class-instantiated
            with filelock.FileLock(
                    lock_path,
                    backend_utils.CLUSTER_STATUS_LOCK_TIMEOUT_SECONDS):
                self.teardown_no_lock(
                    handle,
                    terminate,
                    purge,
                    # When --purge is set and we already see an ID mismatch
                    # error, we skip the refresh codepath. This is because
                    # refresh checks current user identity can throw
                    # ClusterOwnerIdentityMismatchError. The argument/flag
                    # `purge` should bypass such ID mismatch errors.
                    refresh_cluster_status=not is_identity_mismatch_and_purge)
            if terminate:
                common_utils.remove_file_if_exists(lock_path)
        except filelock.Timeout as e:
            raise RuntimeError(
                f'Cluster {cluster_name!r} is locked by {lock_path}. '
                'Check to see if it is still being launched') from e

    # --- CloudVMRayBackend Specific APIs ---

    def get_job_status(
        self,
        handle: CloudVmRayResourceHandle,
        job_ids: Optional[List[int]] = None,
        stream_logs: bool = True
    ) -> Dict[Optional[int], Optional[job_lib.JobStatus]]:
        code = job_lib.JobLibCodeGen.get_job_status(job_ids)
        returncode, stdout, stderr = self.run_on_head(handle,
                                                      code,
                                                      stream_logs=stream_logs,
                                                      require_outputs=True,
                                                      separate_stderr=True)
        subprocess_utils.handle_returncode(returncode, code,
                                           'Failed to get job status.', stderr)
        statuses = job_lib.load_statuses_payload(stdout)
        return statuses

    def cancel_jobs(self,
                    handle: CloudVmRayResourceHandle,
                    jobs: Optional[List[int]],
                    cancel_all: bool = False) -> None:
        """Cancels jobs.

        CloudVMRayBackend specific method.

        Args:
            handle: The cluster handle.
            jobs: Job IDs to cancel. (See `cancel_all` for special semantics.)
            cancel_all: Whether to cancel all jobs. If True, asserts `jobs` is
                set to None. If False and `jobs` is None, cancel the latest
                running job.
        """
        if cancel_all:
            assert jobs is None, (
                'If cancel_all=True, usage is to set jobs=None')
        code = job_lib.JobLibCodeGen.cancel_jobs(jobs, cancel_all)

        # All error messages should have been redirected to stdout.
        returncode, stdout, _ = self.run_on_head(handle,
                                                 code,
                                                 stream_logs=False,
                                                 require_outputs=True)
        subprocess_utils.handle_returncode(
            returncode, code,
            f'Failed to cancel jobs on cluster {handle.cluster_name}.', stdout)

        cancelled_ids = common_utils.decode_payload(stdout)
        if cancelled_ids:
            logger.info(
                f'Cancelled job ID(s): {", ".join(map(str, cancelled_ids))}')
        else:
            logger.info(
                'No jobs cancelled. They may already be in terminal states.')

    def sync_down_logs(
            self,
            handle: CloudVmRayResourceHandle,
            job_ids: Optional[List[str]],
            local_dir: str = constants.SKY_LOGS_DIRECTORY) -> Dict[str, str]:
        """Sync down logs for the given job_ids.

        Returns:
            A dictionary mapping job_id to log path.
        """
        code = job_lib.JobLibCodeGen.get_run_timestamp_with_globbing(job_ids)
        returncode, run_timestamps, stderr = self.run_on_head(
            handle,
            code,
            stream_logs=False,
            require_outputs=True,
            separate_stderr=True)
        subprocess_utils.handle_returncode(returncode, code,
                                           'Failed to sync logs.', stderr)
        run_timestamps = common_utils.decode_payload(run_timestamps)
        if not run_timestamps:
            logger.info(f'{colorama.Fore.YELLOW}'
                        'No matching log directories found'
                        f'{colorama.Style.RESET_ALL}')
            return {}

        job_ids = list(run_timestamps.keys())
        run_timestamps = list(run_timestamps.values())
        remote_log_dirs = [
            os.path.join(constants.SKY_LOGS_DIRECTORY, run_timestamp)
            for run_timestamp in run_timestamps
        ]
        local_log_dirs = [
            os.path.expanduser(os.path.join(local_dir, run_timestamp))
            for run_timestamp in run_timestamps
        ]

        style = colorama.Style
        fore = colorama.Fore
        for job_id, log_dir in zip(job_ids, local_log_dirs):
            logger.info(f'{fore.CYAN}Job {job_id} logs: {log_dir}'
                        f'{style.RESET_ALL}')

        runners = handle.get_command_runners()

        def _rsync_down(args) -> None:
            """Rsync down logs from remote nodes.

            Args:
                args: A tuple of (runner, local_log_dir, remote_log_dir)
            """
            (runner, local_log_dir, remote_log_dir) = args
            try:
                os.makedirs(local_log_dir, exist_ok=True)
                runner.rsync(
                    # Require a `/` at the end to make sure the parent dir
                    # are not created locally. We do not add additional '*' as
                    # kubernetes's rsync does not work with an ending '*'.
                    source=f'{remote_log_dir}/',
                    target=local_log_dir,
                    up=False,
                    stream_logs=False,
                )
            except exceptions.CommandError as e:
                if e.returncode == exceptions.RSYNC_FILE_NOT_FOUND_CODE:
                    # Raised by rsync_down. Remote log dir may not exist, since
                    # the job can be run on some part of the nodes.
                    logger.debug(f'{runner.node_id} does not have the tasks/*.')
                else:
                    raise

        parallel_args = [[runner, *item]
                         for item in zip(local_log_dirs, remote_log_dirs)
                         for runner in runners]
        subprocess_utils.run_in_parallel(_rsync_down, parallel_args)
        return dict(zip(job_ids, local_log_dirs))

    def tail_logs(self,
                  handle: CloudVmRayResourceHandle,
                  job_id: Optional[int],
                  managed_job_id: Optional[int] = None,
                  follow: bool = True) -> int:
        """Tail the logs of a job.

        Args:
            handle: The handle to the cluster.
            job_id: The job ID to tail the logs of.
            managed_job_id: The managed job ID for display purpose only.
            follow: Whether to follow the logs.
        """
        code = job_lib.JobLibCodeGen.tail_logs(job_id,
                                               managed_job_id=managed_job_id,
                                               follow=follow)
        if job_id is None and managed_job_id is None:
            logger.info(
                'Job ID not provided. Streaming the logs of the latest job.')

        # With the stdin=subprocess.DEVNULL, the ctrl-c will not directly
        # kill the process, so we need to handle it manually here.
        if threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGINT, backend_utils.interrupt_handler)
            signal.signal(signal.SIGTSTP, backend_utils.stop_handler)
        try:
            returncode = self.run_on_head(
                handle,
                code,
                stream_logs=True,
                process_stream=False,
                # Allocate a pseudo-terminal to disable output buffering.
                # Otherwise, there may be 5 minutes delay in logging.
                ssh_mode=command_runner.SshMode.INTERACTIVE,
                # Disable stdin to avoid ray outputs mess up the terminal with
                # misaligned output in multithreading/multiprocessing.
                # Refer to: https://github.com/ray-project/ray/blob/d462172be7c5779abf37609aed08af112a533e1e/python/ray/autoscaler/_private/subprocess_output_util.py#L264 # pylint: disable=line-too-long
                stdin=subprocess.DEVNULL,
            )
        except SystemExit as e:
            returncode = e.code
        return returncode

    def tail_managed_job_logs(self,
                              handle: CloudVmRayResourceHandle,
                              job_id: Optional[int] = None,
                              job_name: Optional[str] = None,
                              controller: bool = False,
                              follow: bool = True) -> None:
        # if job_name is not None, job_id should be None
        assert job_name is None or job_id is None, (job_name, job_id)
        code = managed_jobs.ManagedJobCodeGen.stream_logs(
            job_name, job_id, follow, controller)

        # With the stdin=subprocess.DEVNULL, the ctrl-c will not directly
        # kill the process, so we need to handle it manually here.
        if threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGINT, backend_utils.interrupt_handler)
            signal.signal(signal.SIGTSTP, backend_utils.stop_handler)

        # Refer to the notes in tail_logs.
        self.run_on_head(
            handle,
            code,
            stream_logs=True,
            process_stream=False,
            ssh_mode=command_runner.SshMode.INTERACTIVE,
            stdin=subprocess.DEVNULL,
        )

    def tail_serve_logs(self, handle: CloudVmRayResourceHandle,
                        service_name: str, target: serve_lib.ServiceComponent,
                        replica_id: Optional[int], follow: bool) -> None:
        """Tail the logs of a service.

        Args:
            handle: The handle to the sky serve controller.
            service_name: The name of the service.
            target: The component to tail the logs of. Could be controller,
                load balancer, or replica.
            replica_id: The replica ID to tail the logs of. Only used when
                target is replica.
            follow: Whether to follow the logs.
        """
        if target != serve_lib.ServiceComponent.REPLICA:
            code = serve_lib.ServeCodeGen.stream_serve_process_logs(
                service_name,
                stream_controller=(
                    target == serve_lib.ServiceComponent.CONTROLLER),
                follow=follow)
        else:
            assert replica_id is not None, service_name
            code = serve_lib.ServeCodeGen.stream_replica_logs(
                service_name, replica_id, follow)

        signal.signal(signal.SIGINT, backend_utils.interrupt_handler)
        signal.signal(signal.SIGTSTP, backend_utils.stop_handler)

        self.run_on_head(
            handle,
            code,
            stream_logs=True,
            process_stream=False,
            ssh_mode=command_runner.SshMode.INTERACTIVE,
            stdin=subprocess.DEVNULL,
        )

    def teardown_no_lock(self,
                         handle: CloudVmRayResourceHandle,
                         terminate: bool,
                         purge: bool = False,
                         post_teardown_cleanup: bool = True,
                         refresh_cluster_status: bool = True) -> None:
        """Teardown the cluster without acquiring the cluster status lock.

        NOTE: This method should not be called without holding the cluster
        status lock already.

        refresh_cluster_status is only used internally in the status refresh
        process, and should not be set to False in other cases.

        Raises:
            RuntimeError: If the cluster fails to be terminated/stopped.
        """
        if refresh_cluster_status:
            prev_cluster_status, _ = (
                backend_utils.refresh_cluster_status_handle(
                    handle.cluster_name, acquire_per_cluster_status_lock=False))
        else:
            record = global_user_state.get_cluster_from_name(
                handle.cluster_name)
            prev_cluster_status = record[
                'status'] if record is not None else None
        if prev_cluster_status is None:
            # When the cluster is not in the cluster table, we guarantee that
            # all related resources / cache / config are cleaned up, i.e. it
            # is safe to skip and return True.
            ux_utils.console_newline()
            logger.warning(
                f'Cluster {handle.cluster_name!r} is already terminated. '
                'Skipped.')
            return
        log_path = os.path.join(os.path.expanduser(self.log_dir),
                                'teardown.log')
        log_abs_path = os.path.abspath(log_path)
        cloud = handle.launched_resources.cloud
        config = common_utils.read_yaml(handle.cluster_yaml)
        cluster_name = handle.cluster_name
        cluster_name_on_cloud = handle.cluster_name_on_cloud

        # Avoid possibly unbound warnings. Code below must overwrite these vars:
        returncode = 0
        stdout = ''
        stderr = ''

        if (cloud.PROVISIONER_VERSION >=
                clouds.ProvisionerVersion.RAY_PROVISIONER_SKYPILOT_TERMINATOR):
            logger.debug(f'Provisioner version: {cloud.PROVISIONER_VERSION} '
                         'using new provisioner for teardown.')
            # Stop the ray autoscaler first to avoid the head node trying to
            # re-launch the worker nodes, during the termination of the
            # cluster.
            try:
                # We do not check the return code, since Ray returns
                # non-zero return code when calling Ray stop,
                # even when the command was executed successfully.
                self.run_on_head(handle,
                                 f'{constants.SKY_RAY_CMD} stop --force')
            except exceptions.FetchClusterInfoError:
                # This error is expected if the previous cluster IP is
                # failed to be found,
                # i.e., the cluster is already stopped/terminated.
                if prev_cluster_status == status_lib.ClusterStatus.UP:
                    logger.warning(
                        'Failed to take down Ray autoscaler on the head node. '
                        'It might be because the cluster\'s head node has '
                        'already been terminated. It is fine to skip this.')

            try:
                provisioner.teardown_cluster(repr(cloud),
                                             resources_utils.ClusterName(
                                                 cluster_name,
                                                 cluster_name_on_cloud),
                                             terminate=terminate,
                                             provider_config=config['provider'])
            except Exception as e:  # pylint: disable=broad-except
                if purge:
                    logger.warning(
                        _TEARDOWN_PURGE_WARNING.format(
                            reason='stopping/terminating cluster nodes',
                            details=common_utils.format_exception(
                                e, use_bracket=True)))
                else:
                    raise

            if post_teardown_cleanup:
                self.post_teardown_cleanup(handle, terminate, purge)
            return

        if (isinstance(cloud, clouds.IBM) and terminate and
                prev_cluster_status == status_lib.ClusterStatus.STOPPED):
            # pylint: disable= W0622 W0703 C0415
            from sky.adaptors import ibm
            from sky.skylet.providers.ibm.vpc_provider import IBMVPCProvider

            config_provider = common_utils.read_yaml(
                handle.cluster_yaml)['provider']
            region = config_provider['region']
            search_client = ibm.search_client()
            vpc_found = False
            # pylint: disable=unsubscriptable-object
            vpcs_filtered_by_tags_and_region = search_client.search(
                query=(f'type:vpc AND tags:{cluster_name_on_cloud} '
                       f'AND region:{region}'),
                fields=['tags', 'region', 'type'],
                limit=1000).get_result()['items']
            vpc_id = None
            try:
                # pylint: disable=line-too-long
                vpc_id = vpcs_filtered_by_tags_and_region[0]['crn'].rsplit(
                    ':', 1)[-1]
                vpc_found = True
            except Exception:
                logger.critical('failed to locate vpc for ibm cloud')
                returncode = -1

            if vpc_found:
                # pylint: disable=line-too-long E1136
                # Delete VPC and it's associated resources
                vpc_provider = IBMVPCProvider(
                    config_provider['resource_group_id'], region,
                    cluster_name_on_cloud)
                vpc_provider.delete_vpc(vpc_id, region)
                # successfully removed cluster as no exception was raised
                returncode = 0

        elif terminate and isinstance(cloud, clouds.SCP):
            # pylint: disable=import-outside-toplevel
            from sky.skylet.providers.scp import node_provider
            config['provider']['cache_stopped_nodes'] = not terminate
            provider = node_provider.SCPNodeProvider(config['provider'],
                                                     cluster_name_on_cloud)
            try:
                if not os.path.exists(provider.metadata.path):
                    raise node_provider.SCPError(
                        'SKYPILOT_ERROR_NO_NODES_LAUNCHED: '
                        'Metadata file does not exist.')

                with open(provider.metadata.path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    node_id = next(iter(metadata.values())).get(
                        'creation', {}).get('virtualServerId', None)
                    provider.terminate_node(node_id)
                returncode = 0
            except node_provider.SCPError as e:
                returncode = 1
                stdout = ''
                stderr = str(e)

        # Apr, 2023 by Hysun(hysun.he@oracle.com): Added support for OCI
        # May, 2023 by Hysun: Allow terminate INIT cluster which may have
        # some instances provisioning in background but not completed.
        elif (isinstance(cloud, clouds.OCI) and terminate and
              prev_cluster_status in (status_lib.ClusterStatus.STOPPED,
                                      status_lib.ClusterStatus.INIT)):
            region = config['provider']['region']

            # pylint: disable=import-outside-toplevel
            from ray.autoscaler.tags import TAG_RAY_CLUSTER_NAME

            from sky.skylet.providers.oci.query_helper import oci_query_helper

            # 0: All terminated successfully, failed count otherwise
            returncode = oci_query_helper.terminate_instances_by_tags(
                {TAG_RAY_CLUSTER_NAME: cluster_name_on_cloud}, region)

            # To avoid undefined local variables error.
            stdout = stderr = ''
        else:
            config['provider']['cache_stopped_nodes'] = not terminate
            with tempfile.NamedTemporaryFile('w',
                                             prefix='sky_',
                                             delete=False,
                                             suffix='.yml') as f:
                common_utils.dump_yaml(f.name, config)
                f.flush()

                teardown_verb = 'Terminating' if terminate else 'Stopping'
                with rich_utils.safe_status(f'[bold cyan]{teardown_verb} '
                                            f'[green]{cluster_name}'):
                    # FIXME(zongheng): support retries. This call can fail for
                    # example due to GCP returning list requests per limit
                    # exceeded.
                    returncode, stdout, stderr = log_lib.run_with_log(
                        ['ray', 'down', '-y', f.name],
                        log_abs_path,
                        stream_logs=False,
                        require_outputs=True,
                        # Disable stdin to avoid ray outputs mess up the
                        # terminal with misaligned output when multithreading/
                        # multiprocessing are used.
                        # Refer to: https://github.com/ray-project/ray/blob/d462172be7c5779abf37609aed08af112a533e1e/python/ray/autoscaler/_private/subprocess_output_util.py#L264 # pylint: disable=line-too-long
                        stdin=subprocess.DEVNULL)
        if returncode != 0:
            if purge:
                logger.warning(
                    _TEARDOWN_PURGE_WARNING.format(
                        reason='stopping/terminating cluster nodes',
                        details=stderr))
            # 'TPU must be specified.': This error returns when we call "gcloud
            #   delete" with an empty VM list where no instance exists. Safe to
            #   ignore it and do cleanup locally. TODO(wei-lin): refactor error
            #   handling mechanism.
            #
            # 'SKYPILOT_ERROR_NO_NODES_LAUNCHED': this indicates nodes are
            #   never launched and the errors are related to pre-launch
            #   configurations (such as VPC not found). So it's safe & good UX
            #   to not print a failure message.
            elif ('TPU must be specified.' not in stderr and
                  'SKYPILOT_ERROR_NO_NODES_LAUNCHED: ' not in stderr):
                raise RuntimeError(
                    _TEARDOWN_FAILURE_MESSAGE.format(
                        extra_reason='',
                        cluster_name=common_utils.cluster_name_in_hint(
                            cluster_name, cluster_name_on_cloud),
                        stdout=stdout,
                        stderr=stderr))

        # No need to clean up if the cluster is already terminated
        # (i.e., prev_status is None), as the cleanup has already been done
        # if the cluster is removed from the status table.
        if post_teardown_cleanup:
            self.post_teardown_cleanup(handle, terminate, purge)

    def post_teardown_cleanup(self,
                              handle: CloudVmRayResourceHandle,
                              terminate: bool,
                              purge: bool = False) -> None:
        """Cleanup local configs/caches and delete TPUs after teardown.

        This method will handle the following cleanup steps:
        * Deleting the TPUs;
        * Removing ssh configs for the cluster;
        * Updating the local state of the cluster;
        * Removing the terminated cluster's scripts and ray yaml files.

        Raises:
            RuntimeError: If it fails to delete the TPU.
        """
        log_path = os.path.join(os.path.expanduser(self.log_dir),
                                'teardown.log')
        log_abs_path = os.path.abspath(log_path)
        cluster_name_on_cloud = handle.cluster_name_on_cloud

        # Backward compatibility for TPU nodes created before #2943. Any TPU
        # node launched before that PR have the delete script generated (and do
        # not have the tpu_node config set in its cluster yaml), so we have to
        # call the deletion script to clean up the TPU node.
        # For TPU nodes launched after the PR, deletion is done in SkyPilot's
        # new GCP provisioner API.
        # TODO (zhwu): Remove this after 0.6.0.
        if (handle.tpu_delete_script is not None and
                os.path.exists(handle.tpu_delete_script)):
            # Only call the deletion script if the cluster config does not
            # contain TPU node config. Otherwise, the deletion should
            # already be handled by the new provisioner.
            config = common_utils.read_yaml(handle.cluster_yaml)
            tpu_node_config = config['provider'].get('tpu_node')
            if tpu_node_config is None:
                with rich_utils.safe_status('[bold cyan]Terminating TPU...'):
                    tpu_rc, tpu_stdout, tpu_stderr = log_lib.run_with_log(
                        ['bash', handle.tpu_delete_script],
                        log_abs_path,
                        stream_logs=False,
                        require_outputs=True)
                if tpu_rc != 0:
                    if _TPU_NOT_FOUND_ERROR in tpu_stderr:
                        logger.info('TPU not found. '
                                    'It should have been deleted already.')
                    elif purge:
                        logger.warning(
                            _TEARDOWN_PURGE_WARNING.format(
                                reason='stopping/terminating TPU',
                                details=tpu_stderr))
                    else:
                        raise RuntimeError(
                            _TEARDOWN_FAILURE_MESSAGE.format(
                                extra_reason='It is caused by TPU failure.',
                                cluster_name=common_utils.cluster_name_in_hint(
                                    handle.cluster_name, cluster_name_on_cloud),
                                stdout=tpu_stdout,
                                stderr=tpu_stderr))

        if (terminate and handle.launched_resources.is_image_managed is True):
            # Delete the image when terminating a "cloned" cluster, i.e.,
            # whose image is created by SkyPilot (--clone-disk-from)
            logger.debug(f'Deleting image {handle.launched_resources.image_id}')
            cluster_resources = handle.launched_resources
            cluster_cloud = cluster_resources.cloud
            image_dict = cluster_resources.image_id
            assert cluster_cloud is not None, cluster_resources
            assert image_dict is not None and len(image_dict) == 1
            image_id = list(image_dict.values())[0]
            try:
                cluster_cloud.delete_image(image_id,
                                           handle.launched_resources.region)
            except exceptions.CommandError as e:
                logger.warning(
                    f'Failed to delete cloned image {image_id}. Please '
                    'remove it manually to avoid image leakage. Details: '
                    f'{common_utils.format_exception(e, use_bracket=True)}')
        if terminate:
            cloud = handle.launched_resources.cloud
            config = common_utils.read_yaml(handle.cluster_yaml)
            try:
                cloud.check_features_are_supported(
                    handle.launched_resources,
                    {clouds.CloudImplementationFeatures.OPEN_PORTS})
                provision_lib.cleanup_ports(repr(cloud), cluster_name_on_cloud,
                                            handle.launched_resources.ports,
                                            config['provider'])
            except exceptions.NotSupportedError:
                pass
            except exceptions.PortDoesNotExistError:
                logger.debug('Ports do not exist. Skipping cleanup.')
            except Exception as e:  # pylint: disable=broad-except
                if purge:
                    logger.warning(
                        f'Failed to cleanup ports. Skipping since purge is '
                        f'set. Details: '
                        f'{common_utils.format_exception(e, use_bracket=True)}')
                else:
                    raise

        # The cluster file must exist because the cluster_yaml will only
        # be removed after the cluster entry in the database is removed.
        config = common_utils.read_yaml(handle.cluster_yaml)
        auth_config = config['auth']
        backend_utils.SSHConfigHelper.remove_cluster(handle.cluster_name,
                                                     handle.head_ip,
                                                     auth_config,
                                                     handle.docker_user)

        global_user_state.remove_cluster(handle.cluster_name,
                                         terminate=terminate)

        if terminate:
            # This function could be directly called from status refresh,
            # where we need to cleanup the cluster profile.
            metadata_utils.remove_cluster_metadata(handle.cluster_name)
            # Clean up TPU creation/deletion scripts
            # Backward compatibility for TPU nodes created before #2943.
            # TODO (zhwu): Remove this after 0.6.0.
            if handle.tpu_delete_script is not None:
                assert handle.tpu_create_script is not None
                common_utils.remove_file_if_exists(handle.tpu_create_script)
                common_utils.remove_file_if_exists(handle.tpu_delete_script)

            # Clean up generated config
            # No try-except is needed since Ray will fail to teardown the
            # cluster if the cluster_yaml is missing.
            common_utils.remove_file_if_exists(handle.cluster_yaml)

    def set_autostop(self,
                     handle: CloudVmRayResourceHandle,
                     idle_minutes_to_autostop: Optional[int],
                     down: bool = False,
                     stream_logs: bool = True) -> None:
        # The core.autostop() function should have already checked that the
        # cloud and resources support requested autostop.
        if idle_minutes_to_autostop is not None:
            # Skip auto-stop for Kubernetes and RunPod clusters.
            if (isinstance(handle.launched_resources.cloud,
                           (clouds.Kubernetes, clouds.RunPod)) and not down and
                    idle_minutes_to_autostop >= 0):
                # We should hit this code path only for the controllers on
                # Kubernetes and RunPod clusters.
                assert (controller_utils.Controllers.from_name(
                    handle.cluster_name) is not None), handle.cluster_name
                logger.info('Auto-stop is not supported for Kubernetes '
                            'and RunPod clusters. Skipping.')
                return

            # Check if we're stopping spot
            assert (handle.launched_resources is not None and
                    handle.launched_resources.cloud is not None), handle
            code = autostop_lib.AutostopCodeGen.set_autostop(
                idle_minutes_to_autostop, self.NAME, down)
            returncode, _, stderr = self.run_on_head(handle,
                                                     code,
                                                     require_outputs=True,
                                                     stream_logs=stream_logs)
            subprocess_utils.handle_returncode(returncode,
                                               code,
                                               'Failed to set autostop',
                                               stderr=stderr,
                                               stream_logs=stream_logs)
            global_user_state.set_cluster_autostop_value(
                handle.cluster_name, idle_minutes_to_autostop, down)

    def is_definitely_autostopping(self,
                                   handle: CloudVmRayResourceHandle,
                                   stream_logs: bool = True) -> bool:
        """Check if the cluster is autostopping.

        Returns:
            True if the cluster is definitely autostopping. It is possible
            that the cluster is still autostopping when False is returned,
            due to errors like transient network issues.
        """
        if handle.head_ip is None:
            # The head node of the cluster is not UP or in an abnormal state.
            # We cannot check if the cluster is autostopping.
            return False
        code = autostop_lib.AutostopCodeGen.is_autostopping()
        returncode, stdout, stderr = self.run_on_head(handle,
                                                      code,
                                                      require_outputs=True,
                                                      stream_logs=stream_logs)

        if returncode == 0:
            return common_utils.decode_payload(stdout)
        logger.debug('Failed to check if cluster is autostopping with '
                     f'{returncode}: {stdout+stderr}\n'
                     f'Command: {code}')
        return False

    # TODO(zhwu): Refactor this to a CommandRunner class, so different backends
    # can support its own command runner.
    @timeline.event
    def run_on_head(
        self,
        handle: CloudVmRayResourceHandle,
        cmd: str,
        *,
        port_forward: Optional[List[int]] = None,
        log_path: str = '/dev/null',
        stream_logs: bool = False,
        ssh_mode: command_runner.SshMode = command_runner.SshMode.
        NON_INTERACTIVE,
        under_remote_workdir: bool = False,
        require_outputs: bool = False,
        separate_stderr: bool = False,
        process_stream: bool = True,
        source_bashrc: bool = False,
        **kwargs,
    ) -> Union[int, Tuple[int, str, str]]:
        """Runs 'cmd' on the cluster's head node.

        It will try to fetch the head node IP if it is not cached.

        Args:
            handle: The ResourceHandle to the cluster.
            cmd: The command to run.

            Advanced options:

            port_forward: A list of ports to forward.
            log_path: The path to the log file.
            stream_logs: Whether to stream the logs to stdout/stderr.
            ssh_mode: The mode to use for ssh.
                See command_runner.SSHCommandRunner.SSHMode for more details.
            under_remote_workdir: Whether to run the command under the remote
                workdir ~/sky_workdir.
            require_outputs: Whether to return the stdout and stderr of the
                command.
            separate_stderr: Whether to separate stderr from stdout.
            process_stream: Whether to post-process the stdout/stderr of the
                command, such as replacing or skipping lines on the fly. If
                enabled, lines are printed only when '\r' or '\n' is found.
            source_bashrc: Whether to source bashrc when running on the command
                on the VM. If it is a user-related commands, it would always be
                good to source bashrc to make sure the env vars are set.

        Returns:
            returncode
            or
            A tuple of (returncode, stdout, stderr).

        Raises:
            exceptions.FetchClusterInfoError: If the cluster info cannot be
                fetched.
        """
        # This will try to fetch the head node IP if it is not cached.

        runners = handle.get_command_runners()
        head_runner = runners[0]
        if under_remote_workdir:
            cmd = f'cd {SKY_REMOTE_WORKDIR} && {cmd}'

        return head_runner.run(
            cmd,
            port_forward=port_forward,
            log_path=log_path,
            process_stream=process_stream,
            stream_logs=stream_logs,
            ssh_mode=ssh_mode,
            require_outputs=require_outputs,
            separate_stderr=separate_stderr,
            source_bashrc=source_bashrc,
            **kwargs,
        )

    # --- Utilities ---

    @timeline.event
    def _check_existing_cluster(
            self,
            task: task_lib.Task,
            to_provision: Optional[resources_lib.Resources],
            cluster_name: str,
            dryrun: bool = False) -> RetryingVmProvisioner.ToProvisionConfig:
        """Checks if the cluster exists and returns the provision config.

        Raises:
            exceptions.ResourcesMismatchError: If the resources in the task
                does not match the existing cluster.
            exceptions.InvalidClusterNameError: If the cluster name is invalid.
            # TODO(zhwu): complete the list of exceptions.
        """
        record = global_user_state.get_cluster_from_name(cluster_name)
        if record is None:
            handle_before_refresh = None
            status_before_refresh = None
        else:
            handle_before_refresh = record['handle']
            status_before_refresh = record['status']

        prev_cluster_status, handle = (status_before_refresh,
                                       handle_before_refresh)

        if not dryrun:
            # We force refresh any cluster (1) with INIT status, or (2) has
            # autostop set. This is to determine the actual state of such a
            # cluster and to make the hint that uses prev_cluster_status more
            # accurate.
            record = backend_utils.refresh_cluster_record(
                cluster_name,
                force_refresh_statuses={status_lib.ClusterStatus.INIT},
                acquire_per_cluster_status_lock=False,
            )
            if record is not None:
                prev_cluster_status = record['status']
                handle = record['handle']
            else:
                prev_cluster_status = None
                handle = None
        # We should check the cluster_ever_up after refresh, because if the
        # cluster is terminated (through console or auto-dwon), the record will
        # become None and the cluster_ever_up should be considered as False.
        cluster_ever_up = record is not None and record['cluster_ever_up']
        logger.debug(f'cluster_ever_up: {cluster_ever_up}')
        logger.debug(f'record: {record}')

        if prev_cluster_status is not None:
            assert handle is not None
            # Cluster already exists.
            self.check_resources_fit_cluster(handle, task)
            # Use the existing cluster.
            assert handle.launched_resources is not None, (cluster_name, handle)
            # Assume resources share the same ports.
            for resource in task.resources:
                assert resource.ports == list(task.resources)[0].ports
            requested_ports_set = resources_utils.port_ranges_to_set(
                list(task.resources)[0].ports)
            current_ports_set = resources_utils.port_ranges_to_set(
                handle.launched_resources.ports)
            all_ports = resources_utils.port_set_to_ranges(current_ports_set |
                                                           requested_ports_set)
            to_provision = handle.launched_resources
            if (to_provision.cloud.OPEN_PORTS_VERSION <=
                    clouds.OpenPortsVersion.LAUNCH_ONLY):
                if not requested_ports_set <= current_ports_set:
                    current_cloud = to_provision.cloud
                    with ux_utils.print_exception_no_traceback():
                        raise exceptions.NotSupportedError(
                            'Failed to open new ports on an existing cluster '
                            f'with the current cloud {current_cloud} as it only'
                            ' supports opening ports on launch of the cluster. '
                            'Please terminate the existing cluster and launch '
                            'a new cluster with the desired ports open.')
            if all_ports:
                to_provision = to_provision.copy(ports=all_ports)
            return RetryingVmProvisioner.ToProvisionConfig(
                cluster_name,
                to_provision,
                handle.launched_nodes,
                prev_cluster_status=prev_cluster_status,
                prev_handle=handle,
                prev_cluster_ever_up=cluster_ever_up)
        usage_lib.messages.usage.set_new_cluster()
        # Use the task_cloud, because the cloud in `to_provision` can be changed
        # later during the retry.
        common_utils.check_cluster_name_is_valid(cluster_name)

        if to_provision is None:
            # The cluster is recently terminated either by autostop or manually
            # terminated on the cloud. We should use the previously terminated
            # resources to provision the cluster.
            #
            # FIXME(zongheng): this assert can be hit by using two terminals.
            # First, create a 'dbg' cluster. Then:
            #   Terminal 1: sky down dbg -y
            #   Terminal 2: sky launch -c dbg -- echo
            # Run it in order. Terminal 2 will show this error after terminal 1
            # succeeds in downing the cluster and releasing the lock.
            assert isinstance(
                handle_before_refresh, CloudVmRayResourceHandle), (
                    f'Trying to launch cluster {cluster_name!r} recently '
                    'terminated on the cloud, but the handle is not a '
                    f'CloudVmRayResourceHandle ({handle_before_refresh}).')
            status_before_refresh_str = None
            if status_before_refresh is not None:
                status_before_refresh_str = status_before_refresh.value

            logger.info(
                f'The cluster {cluster_name!r} (status: '
                f'{status_before_refresh_str}) was not found on the cloud: it '
                'may be autodowned, manually terminated, or its launch never '
                'succeeded. Provisioning a new cluster by using the same '
                'resources as its original launch.')
            to_provision = handle_before_refresh.launched_resources
            self.check_resources_fit_cluster(handle_before_refresh, task)

        logger.info(
            f'{colorama.Fore.CYAN}Creating a new cluster: {cluster_name!r} '
            f'[{task.num_nodes}x {to_provision}].'
            f'{colorama.Style.RESET_ALL}\n'
            'Tip: to reuse an existing cluster, '
            'specify --cluster (-c). '
            'Run `sky status` to see existing clusters.')
        return RetryingVmProvisioner.ToProvisionConfig(
            cluster_name,
            to_provision,
            task.num_nodes,
            prev_cluster_status=None,
            prev_handle=None,
            prev_cluster_ever_up=False)

    def _execute_file_mounts(self, handle: CloudVmRayResourceHandle,
                             file_mounts: Optional[Dict[Path, Path]]):
        """Executes file mounts.

        Rsyncing local files and copying from remote stores.
        """
        # File mounts handling for remote paths possibly without write access:
        #  (1) in 'file_mounts' sections, add <prefix> to these target paths.
        #  (2) then, create symlinks from '/.../file' to '<prefix>/.../file'.
        if file_mounts is None or not file_mounts:
            return
        symlink_commands = []
        fore = colorama.Fore
        style = colorama.Style
        logger.info(f'{fore.CYAN}Processing file mounts.{style.RESET_ALL}')
        start = time.time()
        runners = handle.get_command_runners()
        log_path = os.path.join(self.log_dir, 'file_mounts.log')

        # Check the files and warn
        for dst, src in file_mounts.items():
            if not data_utils.is_cloud_store_url(src):
                full_src = os.path.abspath(os.path.expanduser(src))
                # Checked during Task.set_file_mounts().
                assert os.path.exists(full_src), f'{full_src} does not exist.'
                src_size = backend_utils.path_size_megabytes(full_src)
                if src_size >= _PATH_SIZE_MEGABYTES_WARN_THRESHOLD:
                    logger.warning(
                        f'{fore.YELLOW}The size of file mount src {src!r} '
                        f'is {src_size} MB. Try to keep src small or use '
                        '.gitignore to exclude large files, as large sizes '
                        f'will slow down rsync. {style.RESET_ALL}')
                if os.path.islink(full_src):
                    logger.warning(
                        f'{fore.YELLOW}Source path {src!r} is a symlink. '
                        f'Symlink contents are not uploaded.{style.RESET_ALL}')

        os.makedirs(os.path.expanduser(self.log_dir), exist_ok=True)
        os.system(f'touch {log_path}')
        tail_cmd = f'tail -n100 -f {log_path}'
        logger.info('To view detailed progress: '
                    f'{style.BRIGHT}{tail_cmd}{style.RESET_ALL}')

        for dst, src in file_mounts.items():
            # TODO: room for improvement.  Here there are many moving parts
            # (download gsutil on remote, run gsutil on remote).  Consider
            # alternatives (smart_open, each provider's own sdk), a
            # data-transfer container etc.
            if not os.path.isabs(dst) and not dst.startswith('~/'):
                dst = f'{SKY_REMOTE_WORKDIR}/{dst}'
            # Sync 'src' to 'wrapped_dst', a safe-to-write "wrapped" path.
            wrapped_dst = dst
            if not dst.startswith('~/') and not dst.startswith('/tmp/'):
                # Handles the remote paths possibly without write access.
                # (1) add <prefix> to these target paths.
                wrapped_dst = backend_utils.FileMountHelper.wrap_file_mount(dst)
                cmd = backend_utils.FileMountHelper.make_safe_symlink_command(
                    source=dst, target=wrapped_dst)
                symlink_commands.append(cmd)

            if not data_utils.is_cloud_store_url(src):
                full_src = os.path.abspath(os.path.expanduser(src))

                if os.path.isfile(full_src):
                    mkdir_for_wrapped_dst = (
                        f'mkdir -p {os.path.dirname(wrapped_dst)}')
                else:
                    mkdir_for_wrapped_dst = f'mkdir -p {wrapped_dst}'

                # TODO(mluo): Fix method so that mkdir and rsync run together
                backend_utils.parallel_data_transfer_to_nodes(
                    runners,
                    source=src,
                    target=wrapped_dst,
                    cmd=mkdir_for_wrapped_dst,
                    run_rsync=True,
                    action_message='Syncing',
                    log_path=log_path,
                    stream_logs=False,
                )
                continue

            storage = cloud_stores.get_storage_from_path(src)
            if storage.is_directory(src):
                sync_cmd = (storage.make_sync_dir_command(
                    source=src, destination=wrapped_dst))
                # It is a directory so make sure it exists.
                mkdir_for_wrapped_dst = f'mkdir -p {wrapped_dst}'
            else:
                sync_cmd = (storage.make_sync_file_command(
                    source=src, destination=wrapped_dst))
                # It is a file so make sure *its parent dir* exists.
                mkdir_for_wrapped_dst = (
                    f'mkdir -p {os.path.dirname(wrapped_dst)}')

            download_target_commands = [
                # Ensure sync can write to wrapped_dst (e.g., '/data/').
                mkdir_for_wrapped_dst,
                # Both the wrapped and the symlink dir exist; sync.
                sync_cmd,
            ]
            command = ' && '.join(download_target_commands)
            # dst is only used for message printing.
            backend_utils.parallel_data_transfer_to_nodes(
                runners,
                source=src,
                target=dst,
                cmd=command,
                run_rsync=False,
                action_message='Syncing',
                log_path=log_path,
                stream_logs=False,
                # Need to source bashrc, as the cloud specific CLI or SDK may
                # require PATH in bashrc.
                source_bashrc=True,
            )
        # (2) Run the commands to create symlinks on all the nodes.
        symlink_command = ' && '.join(symlink_commands)
        if symlink_command:
            # ALIAS_SUDO_TO_EMPTY_FOR_ROOT_CMD sets sudo to empty string for
            # root. We need this as we do not source bashrc for the command for
            # better performance, and our sudo handling is only in bashrc.
            symlink_command = (
                f'{command_runner.ALIAS_SUDO_TO_EMPTY_FOR_ROOT_CMD} && '
                f'{symlink_command}')

            def _symlink_node(runner: command_runner.CommandRunner):
                returncode = runner.run(symlink_command, log_path=log_path)
                subprocess_utils.handle_returncode(
                    returncode, symlink_command,
                    'Failed to create symlinks. The target destination '
                    f'may already exist. Log: {log_path}')

            subprocess_utils.run_in_parallel(_symlink_node, runners)
        end = time.time()
        logger.debug(f'File mount sync took {end - start} seconds.')

    def _execute_storage_mounts(
            self, handle: CloudVmRayResourceHandle,
            storage_mounts: Optional[Dict[Path, storage_lib.Storage]]):
        """Executes storage mounts: installing mounting tools and mounting."""
        # Handle cases where `storage_mounts` is None. This occurs when users
        # initiate a 'sky start' command from a Skypilot version that predates
        # the introduction of the `storage_mounts_metadata` feature.
        if not storage_mounts:
            return

        # Process only mount mode objects here. COPY mode objects have been
        # converted to regular copy file mounts and thus have been handled
        # in the '_execute_file_mounts' method.
        storage_mounts = {
            path: storage_mount
            for path, storage_mount in storage_mounts.items()
            if storage_mount.mode == storage_lib.StorageMode.MOUNT
        }

        # Handle cases when there aren't any Storages with MOUNT mode.
        if not storage_mounts:
            return

        fore = colorama.Fore
        style = colorama.Style
        plural = 's' if len(storage_mounts) > 1 else ''
        logger.info(f'{fore.CYAN}Processing {len(storage_mounts)} '
                    f'storage mount{plural}.{style.RESET_ALL}')
        start = time.time()
        runners = handle.get_command_runners()
        log_path = os.path.join(self.log_dir, 'storage_mounts.log')

        for dst, storage_obj in storage_mounts.items():
            if not os.path.isabs(dst) and not dst.startswith('~/'):
                dst = f'{SKY_REMOTE_WORKDIR}/{dst}'
            # Raised when the bucket is externall removed before re-mounting
            # with sky start.
            if not storage_obj.stores:
                with ux_utils.print_exception_no_traceback():
                    raise exceptions.StorageExternalDeletionError(
                        f'The bucket, {storage_obj.name!r}, could not be '
                        f'mounted on cluster {handle.cluster_name!r}. Please '
                        'verify that the bucket exists. The cluster started '
                        'successfully without mounting the bucket.')
            # Get the first store and use it to mount
            store = list(storage_obj.stores.values())[0]
            mount_cmd = store.mount_command(dst)
            src_print = (storage_obj.source
                         if storage_obj.source else storage_obj.name)
            if isinstance(src_print, list):
                src_print = ', '.join(src_print)
            try:
                backend_utils.parallel_data_transfer_to_nodes(
                    runners,
                    source=src_print,
                    target=dst,
                    cmd=mount_cmd,
                    run_rsync=False,
                    action_message='Mounting',
                    log_path=log_path,
                    # Need to source bashrc, as the cloud specific CLI or SDK
                    # may require PATH in bashrc.
                    source_bashrc=True,
                )
            except exceptions.CommandError as e:
                if e.returncode == exceptions.MOUNT_PATH_NON_EMPTY_CODE:
                    mount_path = (f'{colorama.Fore.RED}'
                                  f'{colorama.Style.BRIGHT}{dst}'
                                  f'{colorama.Style.RESET_ALL}')
                    error_msg = (f'Mount path {mount_path} is non-empty.'
                                 f' {mount_path} may be a standard unix '
                                 f'path or may contain files from a previous'
                                 f' task. To fix, change the mount path'
                                 f' to an empty or non-existent path.')
                    raise RuntimeError(error_msg) from None
                else:
                    # Strip the command (a big heredoc) from the exception
                    raise exceptions.CommandError(
                        e.returncode,
                        command='to mount',
                        error_msg=e.error_msg,
                        detailed_reason=e.detailed_reason) from None

        end = time.time()
        logger.debug(f'Storage mount sync took {end - start} seconds.')

    def _set_storage_mounts_metadata(
            self, cluster_name: str,
            storage_mounts: Optional[Dict[Path, storage_lib.Storage]]) -> None:
        """Sets 'storage_mounts' object in cluster's storage_mounts_metadata.

        After converting Storage objects in 'storage_mounts' to metadata,
        it stores {PATH: StorageMetadata} into the table.
        """
        if not storage_mounts:
            return
        storage_mounts_metadata = {}
        for dst, storage_obj in storage_mounts.items():
            storage_mounts_metadata[dst] = storage_obj.handle
        lock_path = (
            backend_utils.CLUSTER_FILE_MOUNTS_LOCK_PATH.format(cluster_name))
        lock_timeout = backend_utils.CLUSTER_FILE_MOUNTS_LOCK_TIMEOUT_SECONDS
        try:
            with filelock.FileLock(lock_path, lock_timeout):
                global_user_state.set_cluster_storage_mounts_metadata(
                    cluster_name, storage_mounts_metadata)
        except filelock.Timeout as e:
            raise RuntimeError(
                f'Failed to store metadata for cluster {cluster_name!r} due to '
                'a timeout when trying to access local database. Please '
                f'try again or manually remove the lock at {lock_path}. '
                f'{common_utils.format_exception(e)}') from None

    def get_storage_mounts_metadata(
            self,
            cluster_name: str) -> Optional[Dict[Path, storage_lib.Storage]]:
        """Gets 'storage_mounts' object from cluster's storage_mounts_metadata.

        After retrieving storage_mounts_metadata, it converts back the
        StorageMetadata to Storage object and restores 'storage_mounts.'
        """
        lock_path = (
            backend_utils.CLUSTER_FILE_MOUNTS_LOCK_PATH.format(cluster_name))
        lock_timeout = backend_utils.CLUSTER_FILE_MOUNTS_LOCK_TIMEOUT_SECONDS
        try:
            with filelock.FileLock(lock_path, lock_timeout):
                storage_mounts_metadata = (
                    global_user_state.get_cluster_storage_mounts_metadata(
                        cluster_name))
        except filelock.Timeout as e:
            raise RuntimeError(
                f'Failed to retrieve metadata for cluster {cluster_name!r} '
                'due to a timeout when trying to access local database. '
                f'Please try again or manually remove the lock at {lock_path}.'
                f' {common_utils.format_exception(e)}') from None

        if storage_mounts_metadata is None:
            return None
        storage_mounts = {}
        for dst, storage_metadata in storage_mounts_metadata.items():
            # Setting 'sync_on_reconstruction' to False prevents from Storage
            # object creation to sync local source syncing to the bucket. Local
            # source specified in Storage object is synced to the bucket only
            # when it is created with 'sky launch'.
            storage_mounts[dst] = storage_lib.Storage.from_metadata(
                storage_metadata, sync_on_reconstruction=False)
        return storage_mounts

    def _skypilot_predefined_env_vars(
            self, handle: CloudVmRayResourceHandle) -> Dict[str, str]:
        """Returns the SkyPilot predefined environment variables.

        TODO(zhwu): Check if a single variable for all the cluster info is more
        desirable or separate variables for each piece of info.
        NOTE: In order to avoid complication in a potential future separation
        of the info into multiple env vars, we should not treat this json format
        as a sink for all the cluster info.
        """
        return {
            'SKYPILOT_CLUSTER_INFO': json.dumps({
                'cluster_name': handle.cluster_name,
                'cloud': str(handle.launched_resources.cloud),
                'region': handle.launched_resources.region,
                'zone': handle.launched_resources.zone,
            })
        }

    def _get_task_env_vars(self, task: task_lib.Task, job_id: int,
                           handle: CloudVmRayResourceHandle) -> Dict[str, str]:
        """Returns the environment variables for the task."""
        env_vars = task.envs.copy()
        # If it is a managed job, the TASK_ID_ENV_VAR will have been already set
        # by the controller.
        if constants.TASK_ID_ENV_VAR not in env_vars:
            env_vars[
                constants.TASK_ID_ENV_VAR] = common_utils.get_global_job_id(
                    self.run_timestamp,
                    cluster_name=handle.cluster_name,
                    job_id=str(job_id))
        env_vars.update(self._skypilot_predefined_env_vars(handle))
        return env_vars

    def _execute_task_one_node(self, handle: CloudVmRayResourceHandle,
                               task: task_lib.Task, job_id: int,
                               detach_run: bool) -> None:
        # Launch the command as a Ray task.
        log_dir = os.path.join(self.log_dir, 'tasks')

        resources_dict = backend_utils.get_task_demands_dict(task)
        internal_ips = handle.internal_ips()
        assert internal_ips is not None, 'internal_ips is not cached in handle'

        task_env_vars = self._get_task_env_vars(task, job_id, handle)

        codegen = RayCodeGen()
        codegen.add_prologue(job_id)
        codegen.add_gang_scheduling_placement_group_and_setup(
            1,
            resources_dict,
            stable_cluster_internal_ips=internal_ips,
            env_vars=task_env_vars,
            setup_cmd=self._setup_cmd,
            setup_log_path=os.path.join(log_dir, 'setup.log'),
        )

        if callable(task.run):
            run_fn_code = textwrap.dedent(inspect.getsource(task.run))
            run_fn_name = task.run.__name__
            codegen.register_run_fn(run_fn_code, run_fn_name)

        command_for_node = task.run if isinstance(task.run, str) else None
        codegen.add_ray_task(
            bash_script=command_for_node,
            env_vars=task_env_vars,
            task_name=task.name,
            ray_resources_dict=backend_utils.get_task_demands_dict(task),
            log_dir=log_dir)

        codegen.add_epilogue()

        self._exec_code_on_head(handle,
                                codegen.build(),
                                job_id,
                                detach_run=detach_run,
                                managed_job_dag=task.managed_job_dag)

    def _execute_task_n_nodes(self, handle: CloudVmRayResourceHandle,
                              task: task_lib.Task, job_id: int,
                              detach_run: bool) -> None:
        # Strategy:
        #   ray.init(...)
        #   for node:
        #     submit _run_cmd(cmd) with resource {node_i: 1}
        log_dir_base = self.log_dir
        log_dir = os.path.join(log_dir_base, 'tasks')
        resources_dict = backend_utils.get_task_demands_dict(task)
        internal_ips = handle.internal_ips()
        assert internal_ips is not None, 'internal_ips is not cached in handle'

        # If TPU VM Pods is used, #num_nodes should be num_nodes * num_node_ips
        num_actual_nodes = task.num_nodes * handle.num_ips_per_node
        task_env_vars = self._get_task_env_vars(task, job_id, handle)

        codegen = RayCodeGen()
        codegen.add_prologue(job_id)
        codegen.add_gang_scheduling_placement_group_and_setup(
            num_actual_nodes,
            resources_dict,
            stable_cluster_internal_ips=internal_ips,
            env_vars=task_env_vars,
            setup_cmd=self._setup_cmd,
            setup_log_path=os.path.join(log_dir, 'setup.log'),
        )

        if callable(task.run):
            run_fn_code = textwrap.dedent(inspect.getsource(task.run))
            run_fn_name = task.run.__name__
            codegen.register_run_fn(run_fn_code, run_fn_name)

        # TODO(zhwu): The resources limitation for multi-node ray.tune and
        # horovod should be considered.
        for i in range(num_actual_nodes):
            command_for_node = task.run if isinstance(task.run, str) else None

            # Ray's per-node resources, to constrain scheduling each command to
            # the corresponding node, represented by private IPs.
            codegen.add_ray_task(
                bash_script=command_for_node,
                env_vars=task_env_vars,
                task_name=task.name,
                ray_resources_dict=backend_utils.get_task_demands_dict(task),
                log_dir=log_dir,
                gang_scheduling_id=i)

        codegen.add_epilogue()
        # TODO(zhanghao): Add help info for downloading logs.
        self._exec_code_on_head(handle,
                                codegen.build(),
                                job_id,
                                detach_run=detach_run,
                                managed_job_dag=task.managed_job_dag)
