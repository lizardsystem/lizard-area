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


def import_shapefile_area(shapefile_filename, srid, user, data_administrator, file_type):
    """
    Load shapefile with communique and put it in Communique(GeoObject)
    and GeoObjectGroup

    From: import_geoobject_shapefile in rainapp
    """
    # shapefile_filename = resource_filename('lizard_rainapp',
    #                                        'shape/gemeenten2009.shp')

    original_srs = ogr.osr.SpatialReference()
    original_srs.ImportFromEPSG(int(srid))
    target_srs = ogr.osr.SpatialReference()
    target_srs.ImportFromEPSG(4326)
    coordinate_transformation = ogr.osr.CoordinateTransformation(
         original_srs, target_srs)

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

    done = {}  # Check for duplicates

    # Add all geo objects to group.
    for feature in layer:
        geom = feature.GetGeometryRef()
        # Optional extra things to do with the shape
        geom.Transform(coordinate_transformation)
        geom.FlattenTo2D()
        # import pdb;pdb.set_trace()

        # # KRW Waterlichamen merge
        # kwargs = {
        #     'ident': feature.GetField(feature.GetFieldIndex('OWAIDENT')),
        #     'geometry': GEOSGeometry(geom.ExportToWkt(), srid=4326),
        #     'geo_object_group': geo_object_group,

        #     # Communique
        #     'name': '%s' % feature.GetField(feature.GetFieldIndex('OWANAAM')),

        #     # Area
        #     'data_administrator': data_administrator,
        #     'area_class': Area.AREA_CLASS_KRW_WATERLICHAAM,
        # }

        # # Afvoergebieden, 2 varianten
        # # area_code, _ = AreaCode.objects.get_or_create(
        # #     name=feature.GetField(feature.GetFieldIndex('GAFCODE')))
        # kwargs = {
        #     'ident': feature.GetField(feature.GetFieldIndex('GAFIDENT')),
        #     'geometry': GEOSGeometry(geom.ExportToWkt(), srid=4326),
        #     'geo_object_group': geo_object_group,

        #     # Communique
        #     'name': unicode(
        #         feature.GetField(feature.GetFieldIndex('GAFNAAM')),
        #         errors='ignore'),
        #     #'code': area_code,
        #     # Area
        #     'data_administrator': data_administrator,
        #     'area_class': Area.AREA_CLASS_AAN_AFVOERGEBIED,
        # }

        # Deel afvoergebieden: watervlakken_mbp_sap
        # area_code, _ = AreaCode.objects.get_or_create(
        #     name=feature.GetField(feature.GetFieldIndex('GAFCODE')))
        parent = Area.objects.get(name=unicode(
                feature.GetField(feature.GetFieldIndex('GAFNAAM')),
                errors='ignore'))
        # Only field that is unique.
        name = 'Deelgebied %s' % feature.GetField(
            feature.GetFieldIndex('FID_GBKNwa'))
        ident = 'LSDR-%s' % feature.GetField(
            feature.GetFieldIndex('FID_GBKNwa')),  # Else it is not unique
        kwargs = {
            'ident': ident,
            'geometry': GEOSGeometry(geom.ExportToWkt(), srid=4326),
            'geo_object_group': geo_object_group,

            # Communique
            'name': name,
            #'code': area_code,
            # Area
            'data_administrator': data_administrator,
            'area_class': Area.AREA_CLASS_DEEL_AAN_AFVOERGEBIED,
            'parent': parent,
        }

        if ident not in done:
            geo_object = Area(**kwargs)
            geo_object.save()
            done[ident] = None
        else:
            logger.warning(
                'Ignored: Ident %s is already imported in this session' %
                ident)
        number_of_features += 1

    logger.info("Added %s with %s geo objects.",
            shapefile_filename, number_of_features)

