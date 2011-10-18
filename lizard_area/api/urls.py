# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from djangorestframework.views import InstanceModelView

from lizard_area.api.resources import AreaResource
from lizard_area.api.resources import CategoryResource
from lizard_area.api.resources import CommuniqueResource
from lizard_area.api.resources import GeoObjectGroupResource

from lizard_area.api.views import RootView
from lizard_area.api.views import CategoryRootView
from lizard_area.api.views import KRWAreaView
from lizard_area.api.views import CatchmentAreaView


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$',
        RootView.as_view(),
        name='root'),
    url(r'^category/$',
        CategoryRootView.as_view(),
        name='category-root'),
    url(r'^category/(?P<slug>[^/]+)/$',
        InstanceModelView.as_view(resource=CategoryResource),
        name='category'),
    url(r'^krw-areas/$',
        KRWAreaView.as_view(),
        name='krw-areas'),
    url(r'^catchment-areas/$',  # Aan-/afvoergebieden
        CatchmentAreaView.as_view(),
        name='catchment-areas'),
    url(r'^communique/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=CommuniqueResource),
        name='communique'),
    url(r'^area/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=AreaResource),
        name='area'),
    url(r'^geo_object_group/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=GeoObjectGroupResource),
        name='geo_object_group'),
    )
