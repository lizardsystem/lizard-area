"""
Model resources for API.
"""
from djangorestframework.resources import ModelResource

from lizard_area.models import Area
from lizard_area.models import Category
from lizard_area.models import Communique


class CommuniqueResource(ModelResource):
    """
    A Communique is a GeoObject with extra metadata on that object.
    """
    model = Communique
    fields = ()
    ordering = ('name', )

    def __init__(self, *args, **kwargs):
        super(CommuniqueResource, self).__init__(*args, **kwargs)
        self.fields = (
            'ident', 'geometry', 'geo_object_group', 'name', 'code',
            'status', 'area_type', 'province', 'municipality', 'basin',
            'watermanagementarea', )

    def geo_object_group(self, instance):
        return {'name': instance.name,
                'url': instance.geo_object_group.get_absolute_url()}


class AreaResource(CommuniqueResource):
    """
    An Area is an extended Communique object.
    """
    model = Area

    def __init__(self, *args, **kwargs):
        super(AreaResource, self).__init__(*args, **kwargs)
        self.fields = list(self.fields) + [
            'children', 'parent', 'area_class', 'area_class_name']

    def area_class_name(self, instance):
        return Area.AREA_CLASS_DICT[instance.area_class]

    def children(self, instance):
        return [{'name': child.name, 'url': child.get_absolute_url()} for
                child in instance.get_children()]

    def parent(self, instance):
        if instance.parent:
            return {'name': instance.parent.name,
                    'url': instance.parent.get_absolute_url()}
        else:
            return None


class CategoryResource(ModelResource):
    """
    A category and its communique objects.
    """
    model = Category
    fields = ('name', 'slug', 'parent', 'children', 'areas', )
    ordering = ('name', )

    def children(self, instance):
        return [{'name': child.name,
                 'url': child.get_absolute_url()}
                for child in Category.objects.filter(parent=instance)]

    def areas(self, instance):
        groups = instance.geo_object_groups.all()
        areas = Area.objects.filter(
            geo_object_group__in=groups).distinct()
        return [{'name': area.name,
                 'url': area.get_absolute_url() }
                for area in areas]

    def parent(self, instance):
        if instance.parent:
            return {'name': instance.name,
                    'url': instance.parent.get_absolute_url()}
        else:
            return None
