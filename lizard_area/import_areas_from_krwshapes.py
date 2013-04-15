"""
Adapter for areas
"""

import logging

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal import CoordTransform
from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User
from lizard_map.coordinates import RD
from lizard_map.coordinates import WGS84

from lizard_area.models import Area

from lizard_security.models import DataSet

from lizard_geo.models import GeoObjectGroup

from lizard_measure.models import WaterBody

from django.template.defaultfilters import slugify


FIELDS_MAPPING = {
    'ident': 'OWMIDENT',
    'name': 'OWMNAAM',
    'areasort_krw': 'OWMTYPE'
}


WATERBEHEERDER_DATASET = {
    'NL15': 'Delfland',
    'NL02': 'Fryslan',
    'NL04': 'Grootsalland',
    'NL33': 'Hunzeenaas',
    'NL34': 'Noorderzijlvest',
    'NL57': 'Peelenmaasvallei'
}


logger = logging.getLogger(__name__)


def geo_object_group():
    """Return an instance of GeoObjectGroup."""
    group_name = 'IMPORT_KRW_SHAPE_DEMO'
    group_slug = slugify(group_name)
    geo_object_group_user = User.objects.filter(is_superuser=True)[0]
    geo_object_group, created = GeoObjectGroup.objects.get_or_create(
	name=group_name,
	slug=group_slug,
	defaults={'created_by': geo_object_group_user})
    if created:
	geo_object_group.source_log = group_name
	geo_object_group.save()
    return geo_object_group


def retrieve_dataset(feat):
    """Retrieve dataset object corresponds with
    with first 4 chars in owmident field of shape(dbf) file."""
    ident = feat.get(FIELDS_MAPPING['ident'])
    code = ident[:4]
    if code not in WATERBEHEERDER_DATASET.keys():
        return None

    dataset_name = WATERBEHEERDER_DATASET.get(code)
    datasets = DataSet.objects.filter(name=dataset_name)
    
    if not datasets.exists():
        return None

    return datasets[0]


def create_areas(layer):
    """Create area for each item in layer."""
    ct = CoordTransform(SpatialReference(RD), SpatialReference(WGS84))
    for feat in layer:
        dataset = retrieve_dataset(feat)
        if dataset is None:
            continue
        logger.debug(dataset.name)

        feat_geometry = feat.geom
        feat_geometry.transform(ct)

        geom = GEOSGeometry(feat_geometry.wkb)
	if Area.objects.filter(ident=feat.get(FIELDS_MAPPING['ident'])).exists():
            continue
        area = Area(geometry=geom,
                    geo_object_group=geo_object_group(),
                    ident=feat.get(FIELDS_MAPPING['ident']),
                    name=feat.get(FIELDS_MAPPING['name']),
                    areasort_krw=feat.get(FIELDS_MAPPING['areasort_krw']),
		    area_class=Area.AREA_CLASS_KRW_WATERLICHAAM,
		    is_active=True,
                    data_set=dataset)
        area.save()

	# create waterbody
	WaterBody(area=area).save()
	
        logger.debug('Object {0} saved'.format(feat.get(FIELDS_MAPPING['ident'])))
                    
                        
        
def import_areas(krw_shape_file):
    """Import areas from kwr shape file."""
    ds = DataSource(krw_shape_file)
    if ds is None: 
       logger.error("Dataset is None, check the passed file {0}".format(krw_shape_file))
       return
    if ds.layer_count <= 0:
        logger.warn("Dataset contains any layer, check the passed file {0}".format(krw_shape_file))
        return

    for layer in ds:
        create_areas(layer)
        
    del ds

    
    


