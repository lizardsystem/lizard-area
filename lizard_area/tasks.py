from celery.task import task
from django.core import management
from lizard_task.handler import get_handler
import logging


@task()
def synchronize_geoobjects(username=None,
                           dataset=None,
                           areatype=None,
                           taskname=None):
    """
    Import aanafvoergebieden.
    """
    handler = get_handler(username=username, taskname=taskname)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(20)

    options = {'username': username,
               'dataset': dataset,
               'areatype': areatype}
    management.call_command('sync_areas_wfs', **options)

    logger.removeHandler(handler)
