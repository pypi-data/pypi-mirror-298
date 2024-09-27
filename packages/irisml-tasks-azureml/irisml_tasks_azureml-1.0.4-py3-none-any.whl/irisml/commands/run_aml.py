import argparse
import logging
import os
import pathlib
from irisml.azureml import AMLJobManager, Job, JobEnvironment
from irisml.core.commands.common import configure_logger

logger = logging.getLogger(__name__)


def main():
    class KeyValuePairAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            assert len(values) == 1
            k, v = values[0].split('=', 1)
            d = getattr(namespace, self.dest)
            d[k] = v

    configure_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument('job_filepath', type=pathlib.Path)
    parser.add_argument('--env', '-e', nargs=1, default={}, action=KeyValuePairAction)
    parser.add_argument('--no_cache', action='store_true')
    parser.add_argument('--no_cache_read', action='store_true')
    parser.add_argument('--include_local_tasks', '-l', nargs='?', const=pathlib.Path(), default=None, type=pathlib.Path)
    parser.add_argument('--custom_packages', '-p', nargs='+', default=[])
    parser.add_argument('--requirement', '-r', type=pathlib.Path)
    parser.add_argument('--extra_index_url')
    parser.add_argument('--no_wait', action='store_true')
    parser.add_argument('--compute_target', default=os.getenv('IRISML_AML_COMPUTE_TARGET'))
    parser.add_argument('--subscription_id', default=os.getenv('IRISML_AML_SUBSCRIPTION_ID'))
    parser.add_argument('--resourcegroup', default=os.getenv('IRISML_AML_RESOURCEGROUP_NAME'))
    parser.add_argument('--workspace', default=os.getenv('IRISML_AML_WORKSPACE_NAME'))
    parser.add_argument('--experiment', default=os.getenv('IRISML_AML_EXPERIMENT_NAME', 'irisml'))
    parser.add_argument('--job_name')
    parser.add_argument('--base_docker_image')
    parser.add_argument('--base_docker_image_registry')
    parser.add_argument('--no_docker_build_date_label', action='store_true')
    parser.add_argument('--use_sp_on_remote', '--sp', action='store_true', help="Use Service Principal id and secret on the AML job.")
    parser.add_argument('--very_verbose', '-vv', action='store_true')

    args = parser.parse_args()

    if not args.workspace:
        parser.error("Workspace name is required. Please set IRISML_AML_WORKSPACE_NAME or use --workspace option.")
    if not args.resourcegroup:
        parser.error("Resource group name is required. Please set IRISML_AML_RESOURCEGROUP_NAME or use --resourcegroup option.")
    if not args.subscription_id:
        parser.error("Subscription ID is required. Please set IRISML_AML_SUBSCRIPTION_ID or use --subscription_id option.")
    if not args.compute_target:
        parser.error("Compute target is required. Please set IRISML_AML_COMPUTE_TARGET or use --compute_target option.")

    envs = args.env
    cache_url = os.getenv('IRISML_CACHE_URL') if not args.no_cache else None
    if cache_url and args.include_local_tasks:
        logger.warning("Cache is disabled since local task implementations are used.")
        cache_url = None

    job = Job(args.job_filepath, envs, very_verbose=args.very_verbose, aml_job_name=args.job_name)
    if args.include_local_tasks:
        job.add_custom_tasks(args.include_local_tasks)

    custom_packages = args.custom_packages
    if args.requirement:
        custom_packages = custom_packages + args.requirement.read_text().splitlines()
    env = JobEnvironment(args.base_docker_image, args.base_docker_image_registry, custom_packages, args.extra_index_url, not args.no_docker_build_date_label)
    print(env)

    job_manager = AMLJobManager(args.subscription_id, args.resourcegroup, args.workspace, args.experiment, args.compute_target, use_sp_on_remote=args.use_sp_on_remote,
                                cache_url=cache_url, no_cache_read=args.no_cache_read)
    run = job_manager.submit(job, env)
    print(run)

    if not args.no_wait:
        run.stream()


if __name__ == '__main__':
    main()
