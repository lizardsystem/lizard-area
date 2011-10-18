# -*- coding: utf-8 -*-
# Copyright 2011 Nelen & Schuurmans
import logging

from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from lizard_area.models import DataAdministrator

from lizard_area.geoobject import import_shapefile_area

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = "<username> <data-administrator> <filename>"
    help = "Import shapefile."

    @transaction.commit_on_success
    def handle(self, *args, **options):
        user = User.objects.get(username=args[0])
        data_administrator = DataAdministrator.objects.get(name=args[1])
        filename = args[2]
        logger.info('User: %s' % user)
        logger.info('Data administrator: %s' % data_administrator)
        logger.info('Filename: %s' % filename)
        import_shapefile_area(filename, user, data_administrator)
