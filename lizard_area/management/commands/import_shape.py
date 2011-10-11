# -*- coding: utf-8 -*-
# Copyright 2011 Nelen & Schuurmans
import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ""
    help = "Import shapefile."

    def handle(self, *args, **options):
        pass
