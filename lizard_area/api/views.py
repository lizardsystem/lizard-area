"""
API views not coupled to models.
"""
from django.core.urlresolvers import reverse

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
                'parent':{},
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

        return {'data': area.communique.description}

    def post(self, request, ident=None):

        area = Area.objects.get(
            ident=self.CONTENT.get('object_id', None))

        area.communique.description = self.CONTENT.get('communique', '')
        area.communique.save()

        return {'success': True, 'data': area.communique.description}


class AreaPropertyView(View):
    """
    Area information, specially created for dashboards.
    """
    def get(self, request):

        area = Area.objects.get(
                    ident=request.GET.get('object_id'))


        return [
            {'name': 'Naam', 'value': area.name},
            {'name': 'Ident', 'value': area.ident},
            {'name': 'Status', 'value': '-'},
            {'name': 'Waterbeheerder', 'value': 'Waternet'},
        ]



class UserDataView(View):
    """
    Show catchment areas.
    """
    def get(self, request):
        areas = Area.objects.all()
        extent = areas.transform(900913).extent()
