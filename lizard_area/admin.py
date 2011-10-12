from django.contrib import admin

from lizard_area.models import GeoObject
from lizard_area.models import GeoObjectGroup

from lizard_area.models import Category

from lizard_area.models import AreaAdministrator
from lizard_area.models import Communique


admin.site.register(GeoObject)
admin.site.register(GeoObjectGroup)

admin.site.register(Category)

admin.site.register(AreaAdministrator)
admin.site.register(Communique)

