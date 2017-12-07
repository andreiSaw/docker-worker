import socket
import time
import traceback

import json
from disneylandClient import Job
from lockfile import LockFile

from . import harbor
from . import logic
from . import util
from dockerworker.config import config
from dockerworker.log import logger, capture_exception


def do_docker_job(job, stub):
    logger.debug("Got descriptor: {}".format(job.input))
    try:
        job.status = Job.RUNNING
        stub.ModifyJob(job)

        process(job)

        job.status = Job.COMPLETED
        stub.ModifyJob(job)

        logger.debug("Finished")
    except BaseException as e:
        capture_exception()
        if job.status != Job.COMPLETED:
            job.status = Job.FAILED

        debug_info = {
            "hostname": socket.gethostname(),
            "exception": str(e),
            "traceback": traceback.format_exc()
        }

        job.metadata = json.dumps(debug_info)
        stub.ModifyJob(job)

        logger.error(str(e))
        logger.error(traceback.format_exc())
        raise e


def process(job):
    util.descriptor_correct(job)

    job_dir, in_dir, out_dir = logic.create_workdir(job)

    mounted_ids = []
    container_id = None
    try:
        logic.get_input_files(job, in_dir)

        with LockFile(config.LOCK_FILE):
            mounted_ids, container_id = logic.create_containers(job, in_dir, out_dir)

        while harbor.is_running(container_id):
            logger.debug("Container is running. Sleeping for {} sec.".format(config.CONTAINER_CHECK_INTERVAL))
            time.sleep(config.CONTAINER_CHECK_INTERVAL)

        logic.write_std_output(container_id, out_dir)
        logic.handle_output(job, out_dir)
        logger.debug("Setting job.status='completed'")
        job.status = Job.COMPLETED
    except Exception as e:
        capture_exception()
        traceback.print_exc()
        raise e
    finally:
        logic.cleanup_dir(job_dir)

        cnt_to_remove = mounted_ids
        if container_id:
            cnt_to_remove += [container_id]

        logic.cleanup_containers(cnt_to_remove)
