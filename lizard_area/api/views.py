"""
API views not coupled to models.
"""
from datetime import datetime
from django.core.urlresolvers import reverse

from djangorestframework.views import View
from lizard_api.base import BaseApiView

from lizard_area.models import Area
from lizard_area.models import AreaLink
from lizard_area.models import Category


class RootView(View):
    """
    Startpoint.
    """
    def get(self, request):
        return {
            "categories": reverse(
                'lizard_area_api_category_root'),
            "krw-areas": reverse(
                'lizard_area_api_krw_areas'),
            "catchment-areas": reverse(
                'lizard_area_api_catchment_areas'),
            }


class CategoryRootView(View):
    """
    Show categories at root level.
    """
    def get(self, request):
        return {
            "categories": [
                {'name': category.name,
                 'url': category.get_absolute_url()}
                for category in Category.objects.filter(parent=None)]}


class AreaViewForTree(View):
    """
    Show areas in a way that is usefull for a dynamic loading extjs tree .

    Filter using:
    - node == 'root', '' or parent_id
    - area_classes: a list of area classes
    """
    def get(self, request, area_classes=None):

        node = request.GET.get('node', 'root')
        start = request.GET.get('start', None)
        limit = request.GET.get('limit', None)
        size = request.GET.get('size', None)
        flat = request.GET.get('flat', None)

        # Enable this when sync functions are ready for it.
        #areas = Area.objects.filter(is_active=True)
        areas = Area.objects.all()

        if (not node) or flat == 'true':
            pass
        elif node == 'root':
            areas = areas.filter(
                    parent__isnull=True)
        else:
            areas = areas.filter(
                    parent__id=node)

        if area_classes is not None:
            # Assume area_class is a tuple or list
            areas = areas.filter(area_class__in=area_classes)

        query = request.GET.get('query', None)

        if query:
            areas = areas.filter(name__istartswith=query)
        count = None
        if not start is  None and not limit is None:
            start = int(start)
            limit = int(limit)
            count = areas.count()
            areas = areas[start:(start + limit)]

        # To make is_leaf call unnecessary
        area_children = set([
                area.parent_id for area in Area.objects.filter(parent__in=areas)])
        result = []

        if size == 'id_name':
            # Only return names and ids.
            for area in areas:
                rec = {'name': area.name,
                     'id': area.id,
                }
                result.append(rec)
        else:
            for area in areas:
                name = area.name
                rec = {'name': name,
                     'id': area.id,
                     'ident': area.ident,
                     'leaf': area.id not in area_children,
                     'parent': area.parent_id,
                }

                result.append(rec)

        return {
            "areas": result,
            "count": count,
            "total": count
            }


class AreaSpecial(View):
    """
    Area information, specially created for dashboards.
    """
    def get(self, request, ident):

        area = Area.objects.get(
                    ident=ident)

        output = {
            "area": {
                'name': area.name,
                'id': area.ident,
                'extent': area.extent(),
                'parent': {},
                'children': [{
                    'id': child.ident,
                    'name': child.name
                } for child in area.get_children()],
                'url': area.get_absolute_url()
            }
        }
        if area.parent:
            output['parent'] = {
                    'id': area.parent.ident,
                    'name': area.parent.name
                }

        return output


class AreaCommuniqueView(View):
    """
    Area information, specially created for dashboards.
    """
    def get(self, request):

        area = Area.objects.get(
                    ident=request.GET.get('object_id'))
        return  self.get_data(area)

    def post(self, request, ident=None):

        area = Area.objects.get(
            ident=self.CONTENT.get('object_id', None))
        username = request.user.get_full_name()
        now = datetime.today()

        area.communique.edited_by = username
        area.communique.edited_at = now
        area.communique.description = self.CONTENT.get('description', '')
        area.communique.save()

        return {'success': True, 'data': self.get_data(area)}

    def get_data(self, area):

        return {
            'edited_by': area.communique.edited_by if area.communique.edited_by else '',
            'edited_at': area.communique.edited_at if area.communique.edited_at else '',
            'description': area.communique.description
        }


class AreaPropertyView(View):
    """
    Area information, specially created for dashboards.
    """
    def get(self, request):

        area = Area.objects.get(
                    ident=request.GET.get('object_id'))
        waterbeheerder = ''
        if area.data_set is not None:
            waterbeheerder = area.data_set.name
        data = [
            {'name': 'Naam', 'value': area.name},
            {'name': 'Code', 'value': area.ident},
            {'name': 'Waterbeheerder', 'value': waterbeheerder},
        ]
        if area.area_class == Area.AREA_CLASS_AAN_AFVOERGEBIED:
            data.extend(self.get_area_data(area))
        elif area.area_class == Area.AREA_CLASS_KRW_WATERLICHAAM:
            data.extend(self.get_waterbody_data(area))

        return data

    def get_area_data(self, area):
        """Return area prperties as list of dict."""
        return [
            {'name': 'Datum laatste wijziging',
             'value': area.dt_latestchanged_krw},
            {'name': 'Oppervlakte', 'value': area.surface},
            {'name': 'Soort gebied', 'value': area.areasort},
            {'name': 'Soort deelstroomgebied', 'value': area.areasort_krw},
            {'name': 'Watertype', 'value': area.watertype_krw}]

    def get_waterbody_data(self, area):
        """Return waterbody properties as list of dict."""
        data = []
        if area.water_bodies.all().exists() == False:
            return data
        waterbody = area.water_bodies.all()[0]
        if waterbody.krw_status is not None:
            status = "%s - %s" % (
                waterbody.krw_status.code, waterbody.krw_status.description)
            data.append({'name': 'Status', 'value': status})
        if waterbody.krw_watertype is not None:
            krw_watertype = "%s - %s" % (
               waterbody.krw_watertype.code, waterbody.krw_watertype.description)
            data.append({'name': 'Watertype',
                         'value': krw_watertype})
        return data


class UserDataView(View):
    """
    Show catchment areas.
    """
    def get(self, request):
        areas = Area.objects.all()
        extent = areas.transform(900913).extent()


class AreaLinkView(BaseApiView):
    """
    see and edit links between areas
    """
    model_class = AreaLink
    name_field = 'link_type'

    field_mapping = {
        'id': 'id',
        'area_a': 'area_a__name',
        'area_b': 'area_b__name',
    }

    def get_object_for_api(self,
                           link,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
        create object of measure
        """

        output = {
            'id': link.id,
            'area_a': self._get_related_object(
                link.area_a,
                flat,
            ),
            'area_b': self._get_related_object(
                link.area_b,
                flat,
            ),
        }
        return output
