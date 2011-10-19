# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from lizard_ui.urls import debugmode_urlpatterns
from lizard_area.views import ApiView
from lizard_area.views import Homepage

admin.autodiscover()

API_URL_NAME = 'lizard_area_api_root'
NAME_PREFIX = 'lizard_area_'

urlpatterns = patterns(
    '',
    url(r'^$', Homepage.as_view(), name=NAME_PREFIX + 'homepage'),
    url(r'^api-view/$', ApiView.as_view(), name=NAME_PREFIX + 'api_view'),
    (r'^api/', include('lizard_area.api.urls')),
    )
urlpatterns += debugmode_urlpatterns()
