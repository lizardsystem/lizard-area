#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from lizard_security.models import DataSet
from lizard_area.models import AREA_TYPES
from lizard_area.models import Area, AreaLink
from lizard_area.sync_areas import Synchronizer

import logging
default_logger = logging.getLogger(__name__)


def run_sync_area(options, logger=None):
    """
    Synchronise 'aanafvoergieden with WFS.
    """
    synchronizer = Synchronizer(logger)

    if logger is None:
        logger = default_logger

    datasets = DataSet.objects.filter(name=options['dataset'])
    if datasets.exists() == False:

        datasets = DataSet.objects.all()
        names_str = ""
        for dataset in datasets:
            names_str = "%s\n%s" % (names_str, dataset.name)
        logger.error(
            'Option "--dataset" is reguired, choices:\n%s\n',
            names_str)
        return

    areatype_ok = False
    for item in AREA_TYPES:
        if options['areatype'] in item:
            areatype_ok = True
    if areatype_ok == False:
        logger.error(
            'Option "--areatype" is reguired, choices:\n%s\n',
            "\n".join(['%s' % v[1] for v in AREA_TYPES]))
        return

    synchronizer.run_sync(options['username'],
                          options['areatype'],
                          datasets[0])

    logger.info('create empty links')
    counter = 0

    for area in Area.objects.filter(area_class = Area.AREA_CLASS_KRW_WATERLICHAAM, arealink_a__isnull=True):
        area_link = AreaLink(area_a=area)
        area_link.save()
        counter += 1

    logger.info('Finished creating empty area links for KRW areas (%i links created).'%counter)
