#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from optparse import make_option

from django.core.management.base import BaseCommand
from lizard_security.models import DataSet
from lizard_area.models import AREA_TYPES
from lizard_area.sync_areas import run_sync

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Synchronise area's with external WFS.
    """

    help = ("Example: bin/django sync_areas_wfs --username=buildout "\
                "--areatype=peilgebied --dataset=HHNK")

    option_list = BaseCommand.option_list + (
        make_option('--username',
                    help='Username.',
                    type='str',
                    default=None),
        make_option('--areatype',
                    help='Type of area as in admin by Areawfsconfiguration.',
                    type='str',
                    default=None),
        make_option('--dataset',
                    help='Name of data_set from lizard_security.',
                    type='str',
                    default=None))

    def handle(self, *args, **options):
        if options['username'] is None:
            logger.error('Option "--username" is required,"\ use --help.')
            return

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

        run_sync(options['username'],
                 options['areatype'],
                 datasets[0])
        logger.info('Synchronization is finished.')
