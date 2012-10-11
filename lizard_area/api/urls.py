# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from djangorestframework.views import InstanceModelView

from lizard_area.api.resources import AreaResource
from lizard_area.api.resources import CategoryResource
from lizard_area.api.resources import CommuniqueResource

from lizard_area.api.views import (
    RootView,
    CategoryRootView,
    AreaSpecial,
    AreaViewForTree,
    AreaCommuniqueView,
    AreaPropertyView,
    AreaLinkView,
    BoundsView,
    AreaExistsView,
)

from lizard_area.models import Area

admin.autodiscover()

NAME_PREFIX = 'lizard_area_api_'

urlpatterns = patterns(
    '',
    url(r'^$',
        RootView.as_view(),
        name=NAME_PREFIX + 'root'),
    url(r'^category/$',
        CategoryRootView.as_view(),
        name=NAME_PREFIX + 'category_root'),
    url(r'^category/(?P<slug>[^/]+)/$',
        InstanceModelView.as_view(resource=CategoryResource),
        name=NAME_PREFIX + 'category'),
    url(r'^krw-areas/$',
        AreaViewForTree.as_view(),
         {'area_classes': (Area.AREA_CLASS_KRW_WATERLICHAAM,)},
        name=NAME_PREFIX + 'krw_areas'),
    url(r'^catchment-areas/$',  # Aan-/afvoergebieden
        AreaViewForTree.as_view(),
        {'area_classes': (Area.AREA_CLASS_AAN_AFVOERGEBIED,
                          Area.AREA_CLASS_DEEL_AAN_AFVOERGEBIED,)},
        name=NAME_PREFIX + 'catchment_areas'),
    url(r'^communique/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=CommuniqueResource),
        name=NAME_PREFIX + 'communique'),
    url(r'^property/$',
        AreaPropertyView.as_view(),
        name=NAME_PREFIX + 'property'),
    url(r'^area_communique/$',
        AreaCommuniqueView.as_view(),
        name=NAME_PREFIX + 'area_communique'),
    url(r'^area/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=AreaResource),
        name=NAME_PREFIX + 'area'),
    url(r'^area_special/(?P<ident>[^/]+)/$',
        AreaSpecial.as_view(),
        name=NAME_PREFIX + 'area_special'),
    url(r'^area_link/$',
        AreaLinkView.as_view(),
        name=NAME_PREFIX + 'area_link'),
    url(r'^bounds/$',
        BoundsView.as_view(),
        name=NAME_PREFIX + 'bounds'),
    url(r'^area_exists/$',
        AreaExistsView.as_view(),
        name=NAME_PREFIX + 'area_exists'),
)
