"""
API views not coupled to models.
"""
from django.core.urlresolvers import reverse

from djangorestframework.views import View

from lizard_area.models import Category


class RootView(View):
    """
    Startpoint.
    """

    def get(self, request):
        return {
            "categories": reverse('lizard-area:api:category-root')}


class CategoryRootView(View):
    """
    Show categories at root level.
    """
    def get(self, request):
        return {
            "categories": [
                category.get_absolute_url()
                for category in Category.objects.filter(parent=None)]}
