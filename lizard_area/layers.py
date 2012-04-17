"""
Adapter for areas
"""
import mapnik

from django.conf import settings
from django.contrib.gis.geos import Point

from lizard_map import coordinates
from lizard_map import workspace
from lizard_area.models import Area
from lizard_area.models import Category


class AdapterArea(workspace.WorkspaceItemAdapter):
    """
    Adapter for showing areas from GeoObjects.
    """
    def __init__(self, *args, **kwargs):
        super(AdapterArea, self).__init__(*args, **kwargs)
        self.category_slug = self.layer_arguments['category_slug']

    def layer(self, layer_ids=None, request=None):
        """Return layer and styles for the category.

        TODO: copy-paste from lizard_krw, make it work and make it better.
        """
        layers = []
        styles = {}
        category = Category.objects.get(slug=self.category_slug)

        query = (
            """
          (select geometry from lizard_geo_geoobject as geoobject,
             lizard_geo_geoobjectgroup as geoobjectgroup,
             lizard_area_category_geo_object_groups as cat_geoobjectgroup,
             lizard_area_category as category where
               geoobject.geo_object_group_id = geoobjectgroup.id and
               geoobjectgroup.id = cat_geoobjectgroup.geoobjectgroup_id and
               cat_geoobjectgroup.category_id = category.id and
               category.slug = '%s') data""" % category.slug)

        default_database = settings.DATABASES['default']
        datasource = mapnik.PostGIS(
            host=default_database['HOST'],
            port=default_database['PORT'],
            user=default_database['USER'],
            password=default_database['PASSWORD'],
            dbname=default_database['NAME'],
            table=query.encode('ascii')
            )

        layer = mapnik.Layer("Gebieden", coordinates.WGS84)
        # TODO: ^^^ translation!
        # layer.datasource = mapnik.Shapefile(
        #     file=self.shape_filename)
        layer.datasource = datasource

        if category.mapnik_xml_style_sheet:
            # This part doesn't work yet.
            dummy_map = mapnik.Map(100, 100)
            area_style = mapnik.load_map_from_string(
                dummy_map,
                str(category.mapnik_xml_style_sheet.style))
        else:
            area_looks = mapnik.PolygonSymbolizer(mapnik.Color("#ff8877"))
            line_looks = mapnik.LineSymbolizer(mapnik.Color('#997766'), 1)

            area_looks.fill_opacity = 0.5
            layout_rule = mapnik.Rule()
            layout_rule.symbols.append(area_looks)
            layout_rule.symbols.append(line_looks)
            area_style = mapnik.Style()

            area_style.rules.append(layout_rule)

        # if self.waterbody_slug:
        #     # light up area
        #     water_body = WaterBody.objects.get(slug=self.waterbody_slug)
        #     layout_rule_waterbody = mapnik.Rule()
        #     area_looks_waterbody = mapnik.PolygonSymbolizer(
        #         mapnik.Color("#ff0000"))
        #     line_looks_waterbody = mapnik.LineSymbolizer(
        #         mapnik.Color('#dd0000'), 1)
        #     layout_rule_waterbody.symbols.append(area_looks_waterbody)
        #     layout_rule_waterbody.symbols.append(line_looks_waterbody)
        #     layout_rule_waterbody.filter = mapnik.Filter(
        #         "[WGBNAAM] = '%s'" % str(water_body.name))
        #     area_style.rules.append(layout_rule_waterbody)

        styles['Area style'] = area_style
        layer.styles.append('Area style')
        layers = [layer]
        return layers, styles

    def search(self, x, y, radius=None):
        """Search by coordinates. Return list of dicts for matching
        items.
        """
        p = Point(x, y, srid=900913)
        p.transform(4326)

        category = Category.objects.get(slug=self.category_slug)

        areas = Area.objects.filter(geo_object_group__category=category,
                                    geometry__contains=p)

        result = [{'distance': 0,
        'name': area.name,
        'shortname': area.name,
        'workspace_item': self.workspace_mixin_item,
        'identifier': {'ident': area.ident},
        'google_coords': (x, y),
        'object': area} for area in areas]

        print result

        return result
