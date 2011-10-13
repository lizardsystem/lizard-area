"""
Adapter for areas
"""
from lizard_map import adapter


class AdapterArea(workspace.WorkspaceItemAdapter):
    """
    Adapter for showing areas from GeoObjects.
    """
    def __init__(self, *args, **kwargs):
        super(WorkspaceItemAdapterKrw, self).__init__(*args, **kwargs)
        self.category_slug = self.layer_arguments['category_slug']

    def layer(self, layer_ids=None, request=None):
        """Return layer and styles for the category.

        TODO: copy-paste from lizard_krw, make it work and make it better.
        """


        category = Category.objects.get(self.category_slug)

        layers = []
        styles = {}
        layer = mapnik.Layer("Krw gegevens", coordinates.RD)
        # TODO: ^^^ translation!
        layer.datasource = mapnik.Shapefile(
            file=self.shape_filename)
        area_looks = mapnik.PolygonSymbolizer(
            mapnik.Color(self.layer_colors[self.layer_name]))
        if self.layer_name == 'background':
            line_looks = mapnik.LineSymbolizer(mapnik.Color('#dddddd'), 1)
        else:
            line_looks = mapnik.LineSymbolizer(mapnik.Color('#dd0000'), 1)

        area_looks.fill_opacity = 0.5
        layout_rule = mapnik.Rule()
        layout_rule.symbols.append(area_looks)
        layout_rule.symbols.append(line_looks)
        area_style = mapnik.Style()

        area_style.rules.append(layout_rule)

        if self.waterbody_slug:
            # light up area
            water_body = WaterBody.objects.get(slug=self.waterbody_slug)
            layout_rule_waterbody = mapnik.Rule()
            area_looks_waterbody = mapnik.PolygonSymbolizer(
                mapnik.Color("#ff0000"))
            line_looks_waterbody = mapnik.LineSymbolizer(
                mapnik.Color('#dd0000'), 1)
            layout_rule_waterbody.symbols.append(area_looks_waterbody)
            layout_rule_waterbody.symbols.append(line_looks_waterbody)
            layout_rule_waterbody.filter = mapnik.Filter(
                "[WGBNAAM] = '%s'" % str(water_body.name))
            area_style.rules.append(layout_rule_waterbody)

        styles['Area style'] = area_style
        layer.styles.append('Area style')
        layers = [layer]
        return layers, styles


