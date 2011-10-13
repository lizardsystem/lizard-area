# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from djangorestframework.views import InstanceModelView

from lizard_area.api.resources import CategoryResource
from lizard_area.api.resources import CommuniqueResource
from lizard_area.api.resources import GeoObjectGroupResource

from lizard_area.api.views import RootView
from lizard_area.api.views import CategoryRootView


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
    url(r'^communique/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=CommuniqueResource),
        name='communique'),
    url(r'^geo_object_group/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=GeoObjectGroupResource),
        name='geo_object_group'),
    )
