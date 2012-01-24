"""
Adapter for areas
"""

import httplib
import csv
import logging
import StringIO

from django.contrib.gis.geos import WKTReader
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from lizard_area.models import Area

from lizard_geo.models import GeoObjectGroup

logger = logging.getLogger(__name__)


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


def parse_csvreader(csv_reader, username):
    """ """
    header = None
    rownum = 0
    #fields_to_save = ['fid', 'bron', 'geometrie', 'gpgident', 'gpgname']
    fields_to_save = {'fid': 'ident',
                      'bron': 'bron',
                      'gpgname': 'name',
                      'geometrie': 'geometry'}
    for row in csv_reader:
        if rownum == 0:
            header = row
        else:
            colnum = 0
            area_object = Area()
            for col in row:
                value = None
                if header[colnum].lower() == 'geometrie':
                    wktreader = WKTReader()
                    print "Col %s", col
                    value = wktreader.read(col)
                    print "GEO value %s", type(value)
                    print fields_to_save[header[colnum].lower()]
                    setattr(area_object, fields_to_save[header[colnum].lower()], value)
                    colnum += 1
                    continue
                if header[colnum].lower() in fields_to_save.keys():
                    value = col
                    setattr(area_object, fields_to_save[header[colnum].lower()], value)
                colnum += 1

            setattr(area_object, 'geo_object_group', geo_object_group(username))
            area_object.save()
            print("area object is saved %s", area_object.ident)
        rownum += 1
        if rownum == 2:
            break


def import_layers_from_web(username, host=None, url=None):
    host = "maps.waterschapservices.nl"
    url = "/wsh/ows?service=WFS&version=1.0.0&request=GetFeature"\
        "&typeName=wsh:peilgebied&maxFeatures=50&outputFormat=csv&srsName=EPSG:4326"
    print("import data from host='%s' url='%s'" % (host, url))
    connection = httplib.HTTPConnection(host)
    connection.request("GET", url)
    response = connection.getresponse()
    print "Response is %s", response.status
    if response.status == 200:
        content = response.read()
        print "content %d", len(content)
        out = StringIO.StringIO(content)
        print "out file %d", len(out.getvalue())
        csvreader = csv.reader(out)
        parse_csvreader(csvreader, username)
        out.close()
    elif response.status == 404:
        logger.error("Page Not Found host='%s' url='%s'" % (host, url))
    else:
        logger.error("Connection error status='%s' reason='%s'" % (response.status,
                                                                   response.reason))

    connection.close()
