# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from djangorestframework.views import InstanceModelView

from lizard_area.api.resources import AreaResource
from lizard_area.api.resources import CategoryResource
from lizard_area.api.resources import CommuniqueResource

from lizard_area.api.views import RootView
from lizard_area.api.views import CategoryRootView
from lizard_area.api.views import KRWAreaView
from lizard_area.api.views import CatchmentAreaView
from lizard_area.api.views import AreaSpecial
from lizard_area.api.views import AreaCommuniqueView

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
        KRWAreaView.as_view(),
        name=NAME_PREFIX + 'krw_areas'),
    url(r'^catchment-areas/$',  # Aan-/afvoergebieden
        CatchmentAreaView.as_view(),
        name=NAME_PREFIX + 'catchment_areas'),
    url(r'^communique/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=CommuniqueResource),
        name=NAME_PREFIX + 'communique'),
    url(r'^area_communique/$',
        AreaCommuniqueView.as_view(),
        name=NAME_PREFIX + 'area_communique'),
    url(r'^area/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=AreaResource),
        name=NAME_PREFIX + 'area'),
    url(r'^area_special/(?P<ident>[^/]+)/$',
        AreaSpecial.as_view(),
        name=NAME_PREFIX + 'area_special'),
    )
