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
        return {
            "areas": [
                {'name': area.name,
                 'url': area.get_absolute_url()}
                for area in Area.objects.filter(
                    area_class=Area.AREA_CLASS_KRW_WATERLICHAAM)
                ]
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
                 'leaf': area.get_children_count()==0,
                 'parent': area.parent_id,
                 'url': area.get_absolute_url()}
                for area in areas
                ]
            }


class UserDataView(View):
    """
    Show catchment areas.
    """
    def get(self, request):

        areas = GeoObject.objects.all()

        extent = areas.transform(900913).extent()
