"""
Testing resources.
"""

from djangorestframework.resources import ModelResource

from lizard_area.models import Category
from lizard_area.models import Communique

class CategoryResource(ModelResource):
    model = Category
    fields = ('name', 'slug', )
    ordering = ('name', )

class CommuniqueResource(ModelResource):
    model = Communique
    fields = ('name', )
    ordering = ('name', )
