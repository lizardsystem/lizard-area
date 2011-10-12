# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from lizard_area.api.resources import CategoryResource
from lizard_area.api.resources import CommuniqueResource

from lizard_area.api.views import RootView
from lizard_area.api.views import CategoryView
from lizard_area.api.views import CommuniqueGroupView
from lizard_area.api.views import CommuniqueView

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$',
        RootView.as_view(),
        name='root'),
    url(r'^category/$',
        CategoryView.as_view(),
        name='category-root'),
    url(r'^category/(?P<category_slug>[^/]+)/$',
        CategoryView.as_view(),
        name='category'),
    url(r'^category/group/(?P<geo_object_group_slug>[^/]+)/$',
        CommuniqueGroupView.as_view(),
        name='communique_group'),
    url(r'^communique/(?P<pk>[^/]+)/$',
        CommuniqueView.as_view(),
        name='communique'),
    )
