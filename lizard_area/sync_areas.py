"""
Adapter for areas
"""

import httplib
import logging
import json
from decimal import Decimal

from datetime import datetime
from datetime import date

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
    """Save synchronistaion history.

    Arguments:

    sync_hist -- instance of SynchronizationHistory
    kwargs - dict contains a field name end value
    """
    for k, v in kwargs.items():
        setattr(sync_hist, k, v)
    sync_hist.save()


def geo_object_group(username):
    """Return an instance of GeoObjectGroup.

    Argument:

    username -- user logging name as string"""
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
                'gpgnaam': 'name',
                'iws_dtmwijzmeta': 'dt_latestchanged_krw',
                'gpgoppvl': 'surface',
                'gpgsoort': 'areasort',
                'gpgsoort': 'areasort_krw',
                'krwwatertype': 'watertype_krw'}
    elif area_type.lower() == 'aanafvoergebied':
        return {'gafident': 'ident',
                'gafnaam': 'name',
                'iws_dtmwijzmeta': 'dt_latestchanged_krw',
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
    """Checks or content contains a GeoJSON elements.

    Arguments:

    content -- dict contains data from wfs
    """

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
    """Returns ident of passed area object.
    The ident field has different names depends on area_type.

    Arguments

    properties -- dict contains area data recived from wfs
    area_type -- area type as string for example 'peilgebied'
    """
    if area_type == 'aanafvoergebied':
        return properties['gafident']
    if area_type == 'peilgebied':
        return properties['gpgident']
    return None


def update_area(area_object, properties, geometry,
                area_type, username):
    """Updates a passed area object. Returns
    amount of activated and updated objects.

    Arguments:

    area_object -- instance object to update
    properties -- dict contains area data
    geometry -- dict contains geometry data
    data_set -- instance object of lizard_security.DataSet
    area_type -- area type as string for example 'peilgebied'
    username -- user logging name as string
    """
    updated = False
    activated = False
    mapping = fields_mapping(area_type)
    for k, v in mapping.items():
        if k not in properties.keys():
            logger.warning("Wrong fields mapping '%s' NOT in response." % k)
            continue
        value_krw = properties.get(k)
        value_vss = getattr(area_object, v)
        if isinstance(value_vss, unicode) and isinstance(value_krw, int):
            value_krw = unicode(value_krw)
        if isinstance(value_vss, unicode) and isinstance(value_krw, Decimal):
            value_krw = unicode(value_krw)
        if isinstance(value_vss, date) and isinstance(value_krw, unicode):
            value_vss = unicode(value_vss)
        if value_vss != value_krw:
            setattr(area_object, v, value_krw)
            updated = True

    mp = geometry2mp(geometry)
    if getattr(area_object, 'geometry') != mp:
        setattr(area_object, 'geometry', mp)
        updated = True

    group = geo_object_group(username)
    if getattr(area_object, 'geo_object_group') != group:
        setattr(area_object, 'geo_object_group', group)
        updated = True

    if getattr(area_object, 'is_active') == False:
        setattr(area_object, 'is_active', True)
        updated = True
        activated = True

    if getattr(area_object, 'area_type') != area_type:
        setattr(area_object, 'area_type', area_type)
        updated = True

    return updated, activated


def set_extra_values(area_object, created, updated):
    """Sets extra values into passed area_object.

    Arguments:

    area_object -- instance object of lizard_area.Area
    created - boolean indicates a new object
    updated - boolean indicates a existing object
    """
    now = datetime.today()
    setattr(area_object, 'dt_latestsynchronized', now)
    if created:
        setattr(area_object, 'dt_created', now)
    if updated:
        setattr(area_object, 'dt_latestchanged', now)


def invalidate(content, area_type, data_set):
    """Deactivate areas those available in vss
    but not in content.
    Returns amount of deactivated areas.

    Arguments:

    content -- list of dict contains loaded krw data
    area_type -- area type as string for example 'peilgebied'
    data_set -- instance object of lizard_security.DataSet
    """
    vss_areas = Area.objects.filter(area_type=area_type,
                                    data_set=data_set,
                                    is_active=True)
    amount_deactivated = 0
    if vss_areas.exists() == False:
        return amount_deactivated

    for area in vss_areas:
        is_active = False
        for feature in content:
            properties = feature['properties']
            ident_krw = get_ident(properties, area_type)
            if area.ident == ident_krw:
                is_active = True
                break

        if is_active == False:
            area.is_active = is_active
            area.save()
            amount_deactivated = amount_deactivated + 1
    return amount_deactivated


def get_or_create_area(geo_object_group, geometry, ident, data_set):
    """Returns area object. This function to catch MultipleObjectsReturned
    error. The error can raise because Ident is not unique field in db.
    In case of error the function returns None."""
    created = False
    area_object = None
    try:
        area_object = Area.objects.get(ident=ident, data_set=data_set)
        return area_object, created
    except Area.DoesNotExist as ex:
        area_object = Area(ident=ident,
                           geo_object_group=geo_object_group,
                           geometry=geometry,
                           data_set=data_set,
                           area_class=Area.AREA_CLASS_AAN_AFVOERGEBIED)
        created = True
        return area_object, created
    except Area.MultipleObjectsReturned as ex:
        logger.error(".".join(map(str, ex.args)))
    except Exception as ex:
        logger.error(".".join(map(str, ex.args)))
    return area_object, created


def create_update_areas(content, username, area_type, data_set, sync_hist):
    """Creates or updates areas.
    During the execution logs into SynchronizationHistory.

    Arguments:

    content -- dict of geojson format within loaded krw data
    username -- user logging name as string
    area_type -- area type as string for example 'peilgebied'
    data_set -- instance object of lizard_security.DataSet
    sync_hist -- object instance of lizard_area.SynchronizationHistory

    """
    amount_updated = 0
    amount_created = 0
    amount_activated = 0
    amount_synchronized = 0
    amount_deactivated = 0

    for feature in content['features']:
        properties = feature['properties']
        geometry = feature['geometry']

        geometry_mp = geometry2mp(geometry)
        ident = get_ident(properties, area_type)
        logger.debug("Synchronise %s ident=%s." % (area_type, ident))
        area_object, created = get_or_create_area(
            geo_object_group(username),
            geometry_mp,
            ident,
            data_set)
        if area_object is None:
            continue
        updated, activated = update_area(area_object, properties,
                                         geometry, area_type, username)
        set_extra_values(area_object, created, updated)
        if created:
            amount_created = amount_created + 1
        elif updated:
            amount_updated = amount_updated + 1

        if activated:
            amount_activated = amount_activated + 1
        if created or updated:
            try:
                area_object.save()
                if created:
                    kwargs = {'amount_created': amount_created}
                elif updated:
                    kwargs = {'amount_updated': amount_updated}
                if kwargs is not None:
                    log_synchistory(sync_hist, **kwargs)
            except Exception as ex:
                logger.error(".".join(map(str, ex.args)))
                logger.error('Object ident="%s" is not saved' % ident)

    amount_deactivated = invalidate(content['features'], area_type, data_set)
    amount_synchronized = len(content['features'])
    log_synchistory(sync_hist, **{'amount_created': amount_created,
                                  'amount_updated': amount_updated,
                                  'amount_activated': amount_activated,
                                  'amount_synchronized': amount_synchronized,
                                  'amount_deactivated': amount_deactivated})


def get_content(response):
    """Return decoded JSON object or string.

    Argument:
    response -- responce object of HTTP request
    """
    try:
        content = json.loads(response.read())
        return content, True
    except ValueError:
        return response.read(), False


def sync_areas(username, params_str, area_type, data_set, sync_hist):
    """Create a http request, loads the data as json,
    checks or recived data geojson elements, synchronizes the data.
    During the execution logs into SynchronizationHistory.

    Arguments:

    username -- user logging name as string
    params_str -- request parameter as url string
    area_type -- area type as string for example 'peilgebied'
    data_set -- instance object of lizard_security.DataSet
    sync_hist -- object instance of lizard_area.SynchronizationHistory
    """
    host = "maps.waterschapservices.nl"
    url = "/wsh/ows?%s" % params_str
    kwargs = {"url": url, "host": host, "message": "Connecting.."}
    log_synchistory(sync_hist, **kwargs)
    connection = httplib.HTTPConnection(host)
    connection.request("GET", url)
    response = connection.getresponse()
    success = False
    if response.status == 200:
        message = "Connected, starting load data."
        log_synchistory(sync_hist, **{'message': message})
        content, is_json = get_content(response)
        if is_json and check_content(content):
            message = "Data loaded, synchronization in progress."
            log_synchistory(sync_hist, **{'message': message})
            logger.debug(message)
            create_update_areas(content, username,
                                area_type, data_set, sync_hist)
            success = True
        else:
            message = "Content is not a GeoJSON format or empty."
            log_synchistory(sync_hist, **{'message': message})
            logger.error(message)
    elif response.status == 404:
        message = "Page Not Found host='%s' url='%s'" % (host, url)
        log_synchistory(sync_hist, **{'message': message})
        logger.error(message)
    else:
        message = "Connection error status='%s' reason='%s'" % (
            response.status, response.reason)
        log_synchistory(sync_hist, **{'message': message})
        logger.error(message)
    connection.close()
    return success


def default_request_parameters():
    """Containts request parameters. Expected that this parameter
    will not be changed."""
    parameters = {
        'service': 'WFS',
        'version': '1.0.0',
        'request': 'GetFeature',
        'outputFormat': 'json',
        'srsName': 'EPSG:4326'}
    return parameters


def run_sync(username, area_type, data_set):
    """Retrieves the request configuration,
    creates a request string and starts syncronization.
    During the execution logs into SynchronizationHistory.

    Arguments:

    username -- user logging name as string
    area_type -- area type as string for example 'peilgebied'
    data_set -- instance object of lizard_security.DataSet
    """
    configurations = AreaWFSConfiguration.objects.filter(area_type=area_type,
                                                         data_set=data_set)

    message = "Syncronization is started. Retrieving configuration...."
    success = True
    sync_hist = SynchronizationHistory(
        dt_start=datetime.today(),
        username=username,
        message=message,
        data_set=data_set)
    sync_hist.save()
    if configurations.exists():
        for config in configurations:
            request_parameters = {
                'typeName': config.typeName,
                'cql_filter': config.cql_filter,
                'maxFeatures': config.maxFeatures}
            request_parameters.update(default_request_parameters())
            params_str = '&'.join(
                ['%s=%s' % (k, v) for k, v in request_parameters.items()])
            success = sync_areas(username, str(params_str), area_type,
                                 data_set, sync_hist)
    else:
        message = "There are no any configuration for %s of %s" % (
            area_type, data_set.name)
        log_synchistory(sync_hist, **{'message': message})
        logger.info(message)
    if success:
        message = "Synchronization is finished."
    else:
        message = "Synchronization is finished with erors: %s" % (
            sync_hist.message)
    log_synchistory(sync_hist, **{'dt_finish': datetime.today(),
                                  'message': message})
