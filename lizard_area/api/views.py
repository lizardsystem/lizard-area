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
            "categories": reverse('lizard-area:api:category-root'),
            "krw-areas": reverse('lizard-area:api:krw-areas'),
            "catchment-areas": reverse('lizard-area:api:catchment-areas'),
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
        return {
            "areas": [
                {'name': area.name,
                 'url': area.get_absolute_url()}
                for area in Area.objects.filter(
                    area_class=Area.AREA_CLASS_AAN_AFVOERGEBIED)
                ]
            }
