from django.core.urlresolvers import reverse

from djangorestframework.views import View

from lizard_area.models import Category
from lizard_area.models import Communique
from lizard_area.models import GeoObjectGroup


class RootView(View):
    """
    """

    def get(self, request):
        return {
            "categories": reverse('category-root')
            }


class CategoryView(View):
    """
    """

    def get(self, request, category_slug=None):
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            category_name = category.name
            categories = Category.objects.filter(parent=category)
            groups = category.geo_object_groups.all()
        else:
            categories = Category.objects.filter(parent=None)
            category_name = ''
            groups = []

        return {
            "name": category_name,
            "slug": category_slug,
            "categories": [
                reverse('category', kwargs={'category_slug': category.slug})
                for category in categories],
            "communique-groups": [
                reverse('communique_group', kwargs={
                        'geo_object_group_slug': group.slug})
                for group in groups]}


class CommuniqueGroupView(View):
    """
    Display all Communique objects in geo object view
    """

    def get(self, request, geo_object_group_slug):
        gog = GeoObjectGroup.objects.get(slug=geo_object_group_slug)
        communiques = Communique.objects.filter(geo_object_group=gog)
        return {
            "name": gog.name,
            "slug": gog.slug,
            "communiques": [reverse('communique', kwargs={'pk': communique.pk}) for communique in communiques]
            }


class CommuniqueView(View):
    """

    """

    def get(self, request, pk):
        communique = Communique.objects.get(pk=pk)
        return communique
