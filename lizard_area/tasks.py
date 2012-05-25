import logging
from celery.task import task
from lizard_task.task import task_logging
from lizard_area.runner import run_sync_area


@task()
@task_logging
def synchronize_geoobjects(username=None,
                           dataset=None,
                           areatype=None,
                           taskname=None,
                           loglevel=20):
    """
    Import aanafvoergebieden.
    """
    logger = logging.getLogger(taskname)

    options = {'username': username,
               'dataset': dataset,
               'areatype': areatype}
    run_sync_area(options, logger=logger)
