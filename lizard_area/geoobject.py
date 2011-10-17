# -*- coding: utf-8 -*-
# Copyright 2011 Nelen & Schuurmans
"""
GeoObject helpers
"""
import logging

from django.template.defaultfilters import slugify
from django.contrib.gis.geos import GEOSGeometry
from osgeo import ogr

from lizard_area.models import Area
from lizard_area.models import GeoObjectGroup

logger = logging.getLogger(__name__)


def import_shapefile_area(shapefile_filename, user, data_administrator):
    """
    Load shapefile with communique and put it in Communique(GeoObject)
    and GeoObjectGroup

    From: import_geoobject_shapefile in rainapp
    """
    # shapefile_filename = resource_filename('lizard_rainapp',
    #                                        'shape/gemeenten2009.shp')

    # original_srs = ogr.osr.SpatialReference()
    # original_srs.ImportFromProj4(coordinates.RD)
    # target_srs = ogr.osr.SpatialReference()
    # target_srs.ImportFromEPSG(4326)
    # coordinate_transformation = ogr.osr.CoordinateTransformation(
    #     original_srs, target_srs)

    drv = ogr.GetDriverByName('ESRI Shapefile')
    source = drv.Open(shapefile_filename)
    layer = source.GetLayer()

    logger.info("Importing new geoobjects from %s...", shapefile_filename)
    number_of_features = 0

    # Create group with geo objects.
    geo_object_group = GeoObjectGroup(
        name=shapefile_filename[:128],
        slug=slugify(shapefile_filename[:128]),
        created_by=user)
    geo_object_group.save()

    # Add all geo objects to group.
    for feature in layer:
        geom = feature.GetGeometryRef()
        # Optional extra things to do with the shape
        # geom.Transform(coordinate_transformation)
        # geom.FlattenTo2D()
        # import pdb;pdb.set_trace()

        # KRW Waterlichamen merge
        # kwargs = {
        #     'ident': feature.GetField(feature.GetFieldIndex('OWAIDENT')),
        #     'geometry': GEOSGeometry(geom.ExportToWkt(), srid=4326),
        #     'geo_object_group': geo_object_group,

        #     # Communique
        #     'name': '%s ' % feature.GetField(feature.GetFieldIndex('OWANAAM')),

        #     # Area
        #     'data_administrator': data_administrator,
        #     'area_class': Area.AREA_CLASS_KRW_WATERLICHAAM,
        # }
        # Afvoergebieden
        kwargs = {
            'ident': feature.GetField(feature.GetFieldIndex('GAFIDENT')),
            'geometry': GEOSGeometry(geom.ExportToWkt(), srid=4326),
            'geo_object_group': geo_object_group,

            # Communique
            'name': '%s ' % feature.GetField(feature.GetFieldIndex('GAFNAAM')),
            'code': feature.GetField(feature.GetFieldIndex('GAFCODE')),
            # Area
            'data_administrator': data_administrator,
            'area_class': Area.AREA_CLASS_AAN_AFVOERGEBIED,
        }
        geo_object = Area(**kwargs)
        geo_object.save()
        number_of_features += 1

    logger.info("Added %s with %s geo objects.",
            shapefile_filename, number_of_features)

