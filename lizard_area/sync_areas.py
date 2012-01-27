"""
Adapter for areas
"""

import httplib
import logging
import json
import datetime

from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Polygon
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from lizard_area.models import Area
from lizard_area.models import AreaWFSConfiguration
from lizard_area.models import SynchronizationHistory

from lizard_geo.models import GeoObjectGroup

logger = logging.getLogger(__name__)


def log_synchistory(sync_hist, **kwargs):
    """Save synchronistaion history."""
    for k, v in kwargs.items():
        setattr(sync_hist, k, v)
    sync_hist.save()


def geo_object_group(username):
    user_obj = User.objects.get(username=username)
    group_name = 'LAYERS'
    group_slug = slugify(group_name)
    geo_object_group, created = GeoObjectGroup.objects.get_or_create(
        name=group_name, slug=group_slug, created_by=user_obj)
    if created:
        geo_object_group.source_log = 'LAYERS'
        geo_object_group.save()
    return geo_object_group


def fields_mapping(area_type):
    """Maps GV fields with Area where
    key is GV field, value is Area field.

    Arguments:
    area_type - 'peilgebied' or 'aanafvoergebied'.
    """
    if area_type.lower() == 'peilgebied':
        return {'gpgident': 'ident',
                'gpgname': 'name',
                'iws_dtmwijzmeta': 'dt_latestchanged',
                'gpgoppvl': 'surface',
                'gpgsoort': 'areasort',
                'gpgsoort': 'areasort_krw',
                'krwwatertype': 'watertype_krw' }
    elif area_type.lower() == 'aanafvoergebied':
        return {'gafident': 'ident',
                'gafname': 'name',
                'iws_dtmwijzmeta': 'dt_latestchanged',
                'gafoppvl': 'surface',
                'gafsoort': 'areasort',
                'gafsoort': 'areasort_krw',
                'krwwatertype': 'watertype_krw'}
    else:
        return {}


def geometry2mp(geo_dict):
    """Convert dict to MultiPolygon object.

    Arguments:
    geo_dict -- python dict with in 'Multipoligon' as type
    and nested list of points as 'coordinates'
    """
    coord = geo_dict.get('coordinates', None)
    geo_type = geo_dict.get('type', None)
    if coord is None or geo_type is None:
        logger.error("Expected 'type' and 'coordinates' "\
                         "keys to convert dict to MultiPolygon "\
                         "object, given %s" % geo_dict.keys())
        return None

    if geo_type.lower() == 'multipolygon':
        polygons = []
        for item in coord[0]:
            polygons.append(Polygon(item))

        if len(polygons) > 0:
            return MultiPolygon(polygons)
        else:
            logger.debug("Amount of polygons is '%d'." % len(polygons))
    return None


def check_content(content):
    """Checks or content is GeoJSON."""
    expected_keys = [u'crs', u'type', u'features', u'bbox']
    features_key = u'features'
    if isinstance(content, dict) == False:
        return False

    for key in expected_keys:
        if key not in content.keys():
            return False

    features = content[features_key]
    if len(features) <= 0:
        return False

    expected_propertie_keys = [u'geometry',
                               u'properties',
                               u'type',
                               u'id',
                               u'geometry_name']
    for feature in features:
        if isinstance(feature, dict) == False:
            return False
        for key in expected_propertie_keys:
            if key not in feature.keys():
                return False
        if isinstance(feature['geometry'], dict) == False:
            return False
    return True


def get_ident(properties, area_type):
    if area_type == 'aanafvoergebied':
        return properties['gafident']
    if area_type == 'peilgebied':
        return properties['gpgident']
    return None


def update_area(area_object, properties, geometry, data_set, area_type, username):
    """ """
    updated = False
    mapping = fields_mapping(area_type)
    for k, v in mapping.items():
        if k not in properties.keys():
            logger.warning("Wrong fields mapping '%s' NOT in response." % k)
            continue
        value = properties.get(k)
        print ("value to set %s." % value)
        print ("value available %s." % getattr(area_object, v))
        if getattr(area_object, v) != value:
            print "set %s." % v
            setattr(area_object, v, value)
            updated = True

    mp = geometry2mp(geometry)
    if getattr(area_object, 'geometry') != mp:
        setattr(area_object, 'data_set', data_set)
        updated = True

    if getattr(area_object, 'data_set') != data_set:
        setattr(area_object, 'data_set', data_set)
        updated = True

    group = geo_object_group(username)
    if getattr(area_object, 'geo_object_group') != group:
        setattr(area_object, 'geo_object_group', group)
        updated = True

    if getattr(area_object, 'is_active') == False:
        setattr(area_object, 'is_active', True)
        updated = True

    if getattr(area_object, 'area_type') != area_type:
        setattr(area_object, 'area_type', area_type)
        updated = True

    return updated


def set_extra_values(area_object, created, updated):
    """Sets extra values into passed area_object."""
    now = datetime.today()
    setattr(area_object, 'dt_latestsynchronized', now)
    if created:
        setattr(area_object, 'dt_created', now)
    if updated:
        setattr(area_object, 'dt_latestchanged', now)


def invalidate(content, area_type, data_set):
    """Deactivate areas."""
    vss_areas = Area.objects.filter(area_type=area_type,
                                    data_set=data_set)
    for feature in content['features']:
        properties = feature['properties']


def create_update_areas(content, username, area_type, data_set, sync_hist):
    """ """
    amount_updated = 0
    amount_created = 0
    for feature in content['features']:
        properties = feature['properties']
        geometry = feature['geometry']

        ident = get_ident(properties, area_type)
        area_object, created = Area.objects.get_or_create(
            geo_object_group=geo_object_group(username),
            geometry=geometry2mp(geometry),
            ident=ident)
        updated = update_area(area_object, properties,
                              geometry, data_set,
                              area_type, username)
        set_extra_values(area_object, created, updated)

        amount_updated = amount_updated + 1 if updated
        if created or updated:
            try:
                area_object.save()
                if created:
                    amount_created = amount_created + 1
                    kwargs = {'amount_created': amount_created}
                else if updated:
                    amount_updated = amount_apdated + 1
                    kwargs = {'amount_updated': amount_updated}
                log_synchistory(sync_hist,**{'message': message})
            except Error as ex:
                logger.error('Object ident="%s" is not saved' % ident)


def sync_areas(username, params_str, area_type, data_set, sync_hist):
    host = "maps.waterschapservices.nl"
    url = "/wsh/ows?%s" % params_str
    print("import data from host='%s' \n url='%s'" % (host, url))
    kwargs = {"url": url, "host": host, "message": "Connecting..")
    log_synchistory(sync_hist,**kwargs)
    connection = httplib.HTTPConnection(host)
    connection.request("GET", url)
    response = connection.getresponse()
    print "Response is %s", response.status
    if response.status == 200:
        message = "Connected, starting load data."
        log_synchistory(sync_hist,**{'message': message})
        content = json.loads(response.read())
        if check_content(content):
            message = "Data loaded, synchronization in progress."
            log_synchistory(sync_hist,**{'message': message})
            logger.debug(message)
            create_update_areas(content, username, area_type, data_set, sync_hist)
        else:
            message = "Content is not a GeoJSON format or empty."
            log_synchistory(sync_hist,**{'message': message})
            logger.error(message)
    elif response.status == 404:
        message = "Page Not Found host='%s' url='%s'" % (host, url)
        log_synchistory(sync_hist,**{'message': message})
        logger.error(message)
    else:
        message = "Connection error status='%s' reason='%s'" % (response.status,
                                                                response.reason)
        log_synchistory(sync_hist,**{'message': message})
        logger.error(message)
    connection.close()


def default_request_parameters():
    parameters = {
        'service': 'WFS',
        'version': '1.0.0',
        'request': 'GetFeature',
        'outputFormat': 'json',
        'srsName': 'EPSG:4326'}
    return parameters


def run_sync(username, area_type, data_set):
    configurations = AreaWFSConfiguration.objects.filter(area_type=area_type,
                                                         data_set=data_set)

    message = "Syncronization is started. Retrieving configuration...."
    sync_hist = SynchronizationHistory(
        dt_start=datetime.today(),
        username=username,
        message=message)
    sync_hist.save()
    if configurations.exists():
        for config in configurations:
            request_parameters = {
                'typeName': config.typeName,
                'cql_filter': config.cql_filter,
                'maxFeatures': config.maxFeatures}
            request_parameters.update(default_request_parameters())
            params_str = '&'.join(['%s=%s' % (k, v) for k, v in request_parameters.items()])
            print params_str
            print type(params_str)
            sync_areas(username, str(params_str), area_type, data_set, sync_hist)
    else:
        message = "There are no any configuration for %s of %s" % (
        log_synchistory(sync_hist, **{'message': message})
        logger.info(message)
    log_synchistory(sync_hist, **{'dt_finish': datetime.today()})
