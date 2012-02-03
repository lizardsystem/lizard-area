"""
API views not coupled to models.
"""
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from djangorestframework.views import View

from lizard_area.models import Area
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


class KRWAreaView(View):
    """
    Show KRW areas.
    """
    def get(self, request):
        node = request.GET.get('node', 'root')

        if node == 'root':
            areas = Area.objects.filter(
                    area_class=Area.AREA_CLASS_KRW_WATERLICHAAM)
        else:
            areas = Area.objects.filter(
                    parent__ident=node)

        query = request.GET.get('query', None)
        id = request.GET.get('id', None)
        if id == 'id':
            use_id = True
        else:
            use_id = False

        if query:
            areas = areas.filter(name__istartswith=query)[0:25]

        result = []
        for area in areas:
            rec = {'name': area.name,
                 'id': area.ident,
                 'leaf': True,
                 'parent': area.parent_id,
                 'url': area.get_absolute_url()
            }
            if use_id:
                rec['id'] = area.id

            result.append(rec)

        return {
            "areas": result
            }


class CatchmentAreaView(View):
    """
    Show catchment areas.
    """
    def get(self, request):

        node = request.GET.get('node', 'root')

        if node == 'root':
            areas = Area.objects.filter(
                    area_class=Area.AREA_CLASS_AAN_AFVOERGEBIED)

        elif node == 'sub':
            areas = Area.objects.filter(
                    area_class=Area.AREA_CLASS_DEEL_AAN_AFVOERGEBIED)
        else:
            areas = Area.objects.filter(
                    parent__ident=node)

        query = request.GET.get('query', None)
        id = request.GET.get('id', None)
        if id == 'id':
            use_id = True
        else:
            use_id = False

        if query:
            areas = areas.filter(name__istartswith=query)[0:25]

        result = []
        for area in areas:
            rec = {'name': area.name,
                 'id': area.ident,
                 'leaf': area.is_leaf(),
                 'parent': area.parent_id,
                 'url': area.get_absolute_url()
            }
            if use_id:
                rec['id'] = area.id

            result.append(rec)

        return {
            "areas": result
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
        username = User.objects.get(username=request.user).get_full_name()
        now = datetime.today()

        area.communique.edited_by = username
        area.communique.edited_at = now
        area.communique.description = self.CONTENT.get('description', '')
        area.communique.save()

        return {'success': True, 'data': self.get_data(area)}

    def get_data(self, area):
        return {
            'edited_by': area.communique.edited_by,
            'edited_at': area.communique.edited_at,
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
        if area.waterbody_set.all().exists() == False:
            return data
        waterbody = area.waterbody_set.all()[0]
        if waterbody.krw_status is not None:
            data.append({'name': 'Status', 'value': waterbody.krw_status.code})
        if waterbody.krw_watertype is not None:
            data.append({'name': 'Watertype',
                         'value': waterbody.krw_watertype.code})
        return data


class UserDataView(View):
    """
    Show catchment areas.
    """
    def get(self, request):
        areas = Area.objects.all()
        extent = areas.transform(900913).extent()
