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


        return {
            "areas": [
                {'name': area.name,
                 'id': area.ident,
                 'leaf': True,
                 'parent': area.parent_id,
                 'url': area.get_absolute_url()}
                for area in areas]
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
        else:
            areas = Area.objects.filter(
                    parent__ident=node)

        return {
            "areas": [
                {'name': area.name,
                 'id': area.ident,
                 'leaf': area.get_children_count() == 0,
                 'parent': area.parent_id,
                 'url': area.get_absolute_url()}
                for area in areas]}


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
                    ident=self.CONTENT.get('object_id'))

        return area.communique

    def post(self, request, ident=None):

        area = Area.objects.get(
            ident=self.CONTENT.get('object_id', None))

        communique = area.communique
        communique.name = self.CONTENT.get('communique', '')
        communique.save()

        return { 'success': True}


class UserDataView(View):
    """
    Show catchment areas.
    """
    def get(self, request):
        areas = Area.objects.all()
        extent = areas.transform(900913).extent()
