from django.contrib.gis import admin

from lizard_area.models import GeoObject
from lizard_area.models import GeoObjectGroup

from lizard_area.models import Category
from lizard_area.models import MapnikXMLStyleSheet

from lizard_area.models import DataAdministrator
from lizard_area.models import Communique
from lizard_area.models import Area

from lizard_area.models import AreaCode
from lizard_area.models import Status
from lizard_area.models import AreaType
from lizard_area.models import Province
from lizard_area.models import Municipality
from lizard_area.models import Basin
from lizard_area.models import WaterManagementArea


class GeoObjectInline(admin.TabularInline):
    model = GeoObject


class GeoObjectGroupAdmin(admin.ModelAdmin):
    inlines = [
        GeoObjectInline,
        ]


class AreaAdmin(admin.ModelAdmin):
    list_filter = ('data_administrator', 'area_class', )


# admin.site.register(GeoObject)
admin.site.register(GeoObjectGroup, GeoObjectGroupAdmin)

admin.site.register(Category)
admin.site.register(MapnikXMLStyleSheet)

admin.site.register(DataAdministrator)
admin.site.register(Communique)
admin.site.register(Area, AreaAdmin)

admin.site.register(AreaCode)
admin.site.register(Status)
admin.site.register(AreaType)
admin.site.register(Province)
admin.site.register(Municipality)
admin.site.register(Basin)
admin.site.register(WaterManagementArea)
