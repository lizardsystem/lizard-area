"""
Adapter for areas
"""

import httplib
import logging
import json
import base64
from decimal import Decimal

from datetime import datetime
from datetime import date

from django.contrib.auth.models import User
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Polygon
from django.template.defaultfilters import slugify

from lizard_area.models import Area
from lizard_area.models import AreaWFSConfiguration
from lizard_area.models import SynchronizationHistory

from lizard_geo.models import GeoObjectGroup

from lizard_measure.models import KRWWatertype
from lizard_measure.models import WaterBody


FIELDS_MAPPING_PEILGEBIED = {
    'gpgident': 'ident',
    'gpgnaam': 'name',
    'iws_dtmwijzmeta': 'dt_latestchanged_krw',
    'gpgoppvl': 'surface',
    'gpgsoort': 'areasort',
    'gpgsoort_krw': 'areasort_krw'
}


FIELDS_MAPPING_AANAFVOERGEBIED = {
    'gafident': 'ident',
    'gafnaam': 'name',
    'iws_dtmwijzmeta': 'dt_latestchanged_krw',
    'gafoppvl': 'surface',
    'gafsoort': 'areasort',
    'gafsoort_krw': 'areasort_krw'
}


FIELDS_MAPPING_EXCEPTION = {
    'fsoort_krw': 'gafsoort_krw',
    'wwatertype': 'krwwatertype',
    'angafident': 'onderdeelvangafident',
    'angpgident': 'onderdeelvangpgident',
    'tailniveau': 'detailniveau'
}

default_logger = logging.getLogger(__name__)


class Synchronizer(object):
    """Synchronize 'aanafvoergebieden' with 'geovoorzieningen',
    build a parent-child relation for synchronized objecten,
    create waterbodies."""

    def __init__(self, logger=None):
        self.logger = logger
        if self.logger is None:
            self.logger = default_logger

    def log_synchistory(self, sync_hist, **kwargs):
        """Save synchronistaion history.

        Arguments:

        sync_hist -- instance of SynchronizationHistory
        kwargs - dict contains a field name end value
        """
        for k, v in kwargs.items():
            setattr(sync_hist, k, v)
        self.logger.info(
            ' | '.join(["%s=%s" % (k, v) for k, v  in kwargs.items()]))
        sync_hist.save()

    def geo_object_group(self):
        """Return an instance of GeoObjectGroup."""
        group_name = 'LAYERS'
        group_slug = slugify(group_name)
        geo_object_group_user = User.objects.filter(is_superuser=True)[0]
        geo_object_group, created = GeoObjectGroup.objects.get_or_create(
            name=group_name,
            slug=group_slug,
            defaults={'created_by': geo_object_group_user},
        )
        if created:
            geo_object_group.source_log = 'LAYERS'
            geo_object_group.save()
        return geo_object_group

    def fields_mapping(self, area_type):
        """Maps GV fields with Area where
        key is GV field, value is Area field.

        Arguments:
        area_type - 'peilgebied' or 'aanafvoergebied'.
        """
        if area_type.lower() == 'peilgebied':
            return FIELDS_MAPPING_PEILGEBIED
        elif area_type.lower() == 'aanafvoergebied':
            return FIELDS_MAPPING_AANAFVOERGEBIED
        else:
            return {}

    def geometry2mp(self, geo_dict):
        """Convert dict to MultiPolygon object.

        Arguments:
        geo_dict -- python dict with in 'Multipoligon' as type
        and nested list of points as 'coordinates'
        """
        coord = geo_dict.get('coordinates', None)
        geo_type = geo_dict.get('type', None)
        if coord is None or geo_type is None:
            self.logger.error("Expected 'type' and 'coordinates' "\
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
                self.logger.debug(
                    "Amount of polygons is '%d'." % len(polygons))
        return None

    def check_content(self, content):
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

    def get_ident(self, properties, area_type):
        """Returns ident of passed area object.
        The ident field has different names depends on area_type.

        Arguments

        properties -- dict contains area data from wfs
        area_type -- area type as string for example 'peilgebied'
        """
        if area_type == 'aanafvoergebied':
            return properties.get('gafident')
        if area_type == 'peilgebied':
            return properties.get('gpgident')
        return None

    def get_parent_area(self, properties):
        """Return parent object of passed area object."""
        gafident_parent = properties.get('onderdeelvangafident', None)
        gpgident_parent = properties.get('onderdeelvangpgident', None)
        parent_areas1 = Area.objects.filter(ident=gafident_parent)
        parent_areas2 = Area.objects.filter(ident=gpgident_parent)

        if parent_areas1.exists():
            return parent_areas1[0]
        elif parent_areas2.exists():
            return parent_areas2[0]
        else:
            return None

    def get_krw_watertype(self, krwwatertype, sync_hist):
        """ Return KRWWatertype object."""
        try:
            watertype = KRWWatertype.objects.get(code=krwwatertype)
            return watertype
        except:
            message = "KrwWaterType '%s' is is not in Aqua Domain table." % (
                krwwatertype)
            self.logger.debug(message)
            return None

    def update_or_create_waterbody(self, area, krwwatertype, sync_hist):
        """Update or create Waterbody object"""
        waterbody, created = WaterBody.objects.get_or_create(area=area)
        krw_watertype = self.get_krw_watertype(krwwatertype, sync_hist)
        if krw_watertype != waterbody.krw_watertype:
            waterbody.krw_watertype = krw_watertype
            waterbody.save()
            return True
        return False

    def update_area(self, area_object, properties, geometry,
                    area_type, username, data_set, sync_hist):
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
        mapping = self.fields_mapping(area_type)
        for k, v in mapping.items():
            if k not in properties.keys():
                self.logger.warning(
                    "Wrong fields mapping '%s' NOT in response." % k)
                continue
            value_krw = properties.get(k)
            value_vss = getattr(area_object, v)
            if isinstance(value_vss, unicode) and isinstance(value_krw, int):
                value_krw = unicode(value_krw)
            if isinstance(value_vss, unicode) and isinstance(
                value_krw, Decimal):
                value_krw = unicode(value_krw)
            if isinstance(value_vss, date) and isinstance(value_krw, unicode):
                value_vss = unicode(value_vss)
            if isinstance(value_krw, unicode):
                value_krw = value_krw.encode('ascii', 'ignore')
            if value_vss != value_krw:
                setattr(area_object, v, value_krw)
                updated = True

        mp = self.geometry2mp(geometry)
        if getattr(area_object, 'geometry') != mp:
            setattr(area_object, 'geometry', mp)
            updated = True

        group = self.geo_object_group()
        if getattr(area_object, 'geo_object_group') != group:
            setattr(area_object, 'geo_object_group', group)
            updated = True

        detailniveau = properties.get('detailniveau', None)
        if detailniveau is not None or detailniveau != '':
            if getattr(area_object, 'is_active') == False:
                setattr(area_object, 'is_active', True)
                updated = True
                activated = True

        if getattr(area_object, 'area_type') != area_type:
            setattr(area_object, 'area_type', area_type)
            updated = True

        area_class = Area.AREA_CLASS_AAN_AFVOERGEBIED
        if getattr(area_object, 'area_class') != area_class:
            setattr(area_object, 'area_class', area_class)
            updated = True

        if getattr(area_object, 'data_set') != data_set:
            setattr(area_object, 'data_set', data_set)
            updated = True

        krwwatertype = properties.get('krwwatertype', None)
        if self.update_or_create_waterbody(
            area_object, krwwatertype, sync_hist):
            updated = True

        return updated, activated

    def set_extra_values(self, area_object, created, updated):
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

    def set_parent_relation(self, features, area_type):
        """Create a child-parent relation.

        Arguments:

        features -- list of dict contains krw areas from wfs
        area_type -- area type as string, for example 'peilgebied'
        """
        self.logger.info("Create a child-parent relation.")
        for feature in features:
            properties = self.properties_keys_to_lower(feature['properties'])
            ident = self.get_ident(properties, area_type)
            areas = Area.objects.filter(ident=ident)
            if areas.exists():
                area = areas[0]
                area.parent = self.get_parent_area(properties)
                self.logger.debug("Set parent='%s' to child='%s'." % (
                        area.parent, ident))
                area.save()
            else:
                self.logger.info(
                    'Area with krw_ident=%s does not exist.' % ident)

    def invalidate(self, content, area_type, data_set):
        """Deactivate areas those available in vss
        but not in content. Deactivates areas where
        'detailniveau' is empty.
        Returns amount of deactivated areas.

        Arguments:

        content -- list of dict contains krw areas from wfs
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
                properties = self.properties_keys_to_lower(
                    feature['properties'])
                ident_krw = self.get_ident(properties, area_type)
                detailniveau = properties.get('detailniveau', None)
                if area.ident == ident_krw and detailniveau is not None:
                    is_active = True
                    break

            if is_active == False:
                area.is_active = is_active
                area.save()
                amount_deactivated = amount_deactivated + 1
        return amount_deactivated

    def get_or_create_area(self, geo_object_group, geometry, ident, data_set):
        """Returns area object. This function to catch MultipleObjectsReturned
        error. The error can raise because Ident is not unique field in db.
        In case of error the function returns None."""
        created = False
        area_object = None
        try:
            area_object = Area.objects.get(ident=ident)
            return area_object, created
        except Area.DoesNotExist as ex:
            area_object = Area(ident=ident,
                               geo_object_group=geo_object_group,
                               geometry=geometry,
                               data_set=data_set,
                               area_class=Area.AREA_CLASS_AAN_AFVOERGEBIED)
            created = True
            return area_object, created
        except Exception as ex:
            self.logger.error(".".join(map(str, ex.args)))
        return area_object, created

    def properties_keys_to_lower(self, orig_dict):
        """Set keys to lawer case, map exception keys."""
        special_dict = {}
        for key, value in orig_dict.iteritems():
            lowercase_key = key.lower()
            new_key = FIELDS_MAPPING_EXCEPTION.get(
                lowercase_key, lowercase_key)
            special_dict[new_key] = value

        return special_dict

    def create_update_areas(self, content, username,
                            area_type, data_set, sync_hist):
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
            properties = self.properties_keys_to_lower(feature['properties'])
            geometry = feature['geometry']

            geometry_mp = self.geometry2mp(geometry)
            ident = self.get_ident(properties, area_type)
            self.logger.debug("Synchronise %s ident=%s." % (area_type, ident))
            area_object, created = self.get_or_create_area(
                self.geo_object_group(),
                geometry_mp,
                ident,
                data_set)
            if area_object is None:
                continue
            updated, activated = self.update_area(area_object, properties,
                                                  geometry, area_type,
                                                  username, data_set,
                                                  sync_hist)
            self.set_extra_values(area_object, created, updated)

            if created:
                amount_created = amount_created + 1
            elif updated:
                amount_updated = amount_updated + 1

            if activated:
                amount_activated = amount_activated + 1
            if created or updated:
                try:
                    area_object.save()
                except Exception as ex:
                    self.logger.error(".".join(map(str, ex.args)))
                    self.logger.error('Object ident="%s" is not saved' % ident)

        amount_deactivated = self.invalidate(
            content['features'], area_type, data_set)
        amount_synchronized = len(content['features'])
        self.log_synchistory(sync_hist,
                             **{'amount_created': amount_created,
                                'amount_updated': amount_updated,
                                'amount_activated': amount_activated,
                                'amount_synchronized': amount_synchronized,
                                'amount_deactivated': amount_deactivated})

    def get_content(self, response):
        """Return decoded JSON object or string.

        Argument:
        response -- responce object of HTTP request
        """
        try:
            content = json.loads(response.read())
            return content, True
        except ValueError:
            return response.read(), False

    def sync_areas(self, username, url, area_type, data_set, sync_hist, kw):
        """Create a http request, loads the data as json,
        checks or recived data geojson elements, synchronizes the data.
        During the execution logs into SynchronizationHistory.

        Arguments:

        username -- user logging name as string
        params_str -- request parameter as url string
        area_type -- area type as string for example 'peilgebied'
        data_set -- instance object of lizard_security.DataSet
        sync_hist -- object instance of lizard_area.SynchronizationHistory
        kw -- connection parameters as dict containing hostname and login data
        """
        host = kw["host"]
        kwargs = {"url": url, "host": host, "message": "Connecting.."}
        self.log_synchistory(sync_hist, **kwargs)
        connection = httplib.HTTPConnection(host)
        if kw.get('auth') is not None:
            headers = {"Authorization": kw.get('auth'),
                       "Content-type": "application/json",
                       "Accept": "text/plain"}
            connection.request("GET", url, None, headers)
        else:
            connection.request("GET", url)
        response = connection.getresponse()
        success = False
        if response.status == 200:
            message = "Connected, starting load data."
            self.log_synchistory(sync_hist, **{'message': message})
            content, is_json = self.get_content(response)
            if is_json and self.check_content(content):
                message = "Data loaded, synchronization in progress."
                self.log_synchistory(sync_hist, **{'message': message})
                self.logger.debug(message)
                self.create_update_areas(content, username,
                                         area_type, data_set,
                                         sync_hist)
                self.set_parent_relation(content['features'], area_type)
                success = True
            else:
                message = "Content is not a GeoJSON format or empty."
                self.log_synchistory(sync_hist, **{'message': message})
                self.logger.error(message)
        elif response.status == 404:
            message = "Page Not Found host='%s' url='%s'" % (host, url)
            self.log_synchistory(sync_hist, **{'message': message})
            self.logger.error(message)
        else:
            message = "Connection error status='%s' reason='%s'" % (
                response.status, response.reason)
            self.log_synchistory(sync_hist, **{'message': message})
            self.logger.error(message)
        connection.close()
        return success

    def default_request_parameters(self):
        """Containts request parameters. Expected that this parameter
        will not be changed."""
        parameters = {
            'service': 'WFS',
            'version': '1.0.0',
            'request': 'GetFeature',
            'outputFormat': 'json',
            'srsName': 'EPSG:4326'}
        return parameters

    def set_request_parameters(self, config):
        request_parameters = self.default_request_parameters()
        if config.typeName is not None and config.typeName != '':
            request_parameters['typeName'] = config.typeName
        if config.cql_filter is not None and config.cql_filter != '':
            request_parameters['cql_filter'] = config.cql_filter
        if config.maxFeatures is not None:
            request_parameters['maxFeatures'] = config.maxFeatures
        return request_parameters

    def set_url(self, request_parameters, config):
        url = None
        if config.path is None:
            return url
        if config.url is None or config.url == "":
            params_string = '&'.join(
                ['%s=%s' % (k, v) for k, v in request_parameters.items()])
            return "%s?%s" % (config.path, params_string)
        else:
            return "%s?%s" % (config.path, config.url)

    def set_connection_parameters(self, config):
        connection_parameters = {}
        if config.host is None:
            return None
        connection_parameters['host'] = config.host
        if config.username == '':
            return connection_parameters
        if config.username is None:
            return connection_parameters
        auth = 'Basic ' + str.strip(base64.encodestring(
                '%s:%s' % (config.username, config.password)))
        connection_parameters['auth'] = auth
        return connection_parameters

    def run_sync(self, username, area_type, data_set):
        """Retrieves the request configuration,
        creates a request string and starts syncronization.
        During the execution logs into SynchronizationHistory.

        Arguments:

        username -- user logging name as string
        area_type -- area type as string for example 'peilgebied'
        data_set -- instance object of lizard_security.DataSet
        """
        configurations = AreaWFSConfiguration.objects.filter(
            area_type=area_type, data_set=data_set)

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
                url = self.set_url(self.set_request_parameters(config), config)
                connection_parameters = self.set_connection_parameters(config)
                if connection_parameters is None or url is None:
                    self.logger.warning(
                        'WFS is not properly configured for "%s".' % (
                            config.name))
                    continue
                success = self.sync_areas(
                    username, url, area_type,
                    data_set, sync_hist, connection_parameters)
        else:
            message = "There are no any configuration for %s of %s" % (
                area_type, data_set.name)
            self.log_synchistory(sync_hist, **{'message': message})
            self.logger.info(message)
        if success:
            message = "Synchronization is finished."
        else:
            message = "Synchronization is finished with erors: %s" % (
                sync_hist.message)
        self.log_synchistory(sync_hist, **{'dt_finish': datetime.today(),
                                      'message': message})
