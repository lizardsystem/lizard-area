from django.contrib.gis import admin

from lizard_area.models import GeoObject
from lizard_area.models import GeoObjectGroup

from lizard_area.models import Category
from lizard_area.models import MapnikXMLStyleSheet

from lizard_area.models import AreaAdministrator
from lizard_area.models import Communique


class GeoObjectInline(admin.TabularInline):
    model = GeoObject


class GeoObjectGroupAdmin(admin.ModelAdmin):
    inlines = [
        GeoObjectInline,
        ]


# admin.site.register(GeoObject)
admin.site.register(GeoObjectGroup, GeoObjectGroupAdmin)

admin.site.register(Category)
admin.site.register(MapnikXMLStyleSheet)

admin.site.register(AreaAdministrator)
admin.site.register(Communique)

