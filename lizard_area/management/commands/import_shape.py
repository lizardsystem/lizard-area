# -*- coding: utf-8 -*-
# Copyright 2011 Nelen & Schuurmans
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from lizard_area.geoobject import import_shapefile_communique

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = "<username> <filename>"
    help = "Import shapefile."

    def handle(self, *args, **options):
        user = User.objects.get(username=args[0])
        filename = args[1]
        logger.info('User: %s' % user)
        logger.info('Filename: %s' % filename)
        import_shapefile_communique(filename, user)
