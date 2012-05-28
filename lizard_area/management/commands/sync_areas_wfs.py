#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from optparse import make_option

from django.core.management.base import BaseCommand
from lizard_area.runner import run_sync_area


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
        run_sync_area(options)
