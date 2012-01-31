from celery.task import task
from django.core import management


@task()
def synchronize_geoobjects(username=None,
                           dataset=None,
                           areatype=None):
    """
    Import aanafvoergebieden.
    """
    options = {'username': username,
               'dataset': dataset,
               'areatype': areatype}
    management.call_command('sync_areas_wfs', **options)
