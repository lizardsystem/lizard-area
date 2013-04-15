#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import os

from django.core.management.base import BaseCommand
from django.conf import settings
from lizard_area.import_areas_from_krwshapes import import_areas


class Command(BaseCommand):
    """
    Synchronise area's with external WFS.
    """

    help = ("Example: bin/django import_areas_from_krwshape")

    def handle(self, *args, **options):
        shapes_path = os.path.join(settings.BUILDOUT_DIR,
                                   'import_krw_portaal/overige/KRWWaterlichamen')
        import_areas(shapes_path)
