"""
Model resources for API.
"""
from djangorestframework.resources import ModelResource

from lizard_area.models import Category
from lizard_area.models import Communique
from lizard_area.models import GeoObjectGroup


class CommuniqueResource(ModelResource):
    """
    A Communique is a GeoObject with extra metadata on that object.
    """
    model = Communique
    fields = ('ident', 'geometry', 'geo_object_group', 'name', 'code',
              'status', 'area_type', 'province', 'municipality', 'basin',
              'watermanagementarea', )
    ordering = ('name', )

    def geo_object_group(self, instance):
        return instance.geo_object_group.get_absolute_url()


class GeoObjectGroupResource(ModelResource):
    """
    """
    model = GeoObjectGroup
    fields = ('name', 'slug', 'created_by', 'last_modified', 'categories', )
    ordering = ('name', )

    def categories(self, instance):
        return [
            category.get_absolute_url()
            for category in instance.category_set.all()]


class CategoryResource(ModelResource):
    """
    A category and its communique objects.
    """
    model = Category
    fields = ('name', 'slug', 'parent', 'children', 'communiques', )
    ordering = ('name', )

    def children(self, instance):
        return [child.get_absolute_url()
                for child in Category.objects.filter(parent=instance)]

    def communiques(self, instance):
        groups = instance.geo_object_groups.all()
        communiques = Communique.objects.filter(
            geo_object_group__in=groups).distinct()
        return [communique.get_absolute_url() for communique in communiques]

    def parent(self, instance):
        if instance.parent:
            return instance.parent.get_absolute_url()
        else:
            return None
