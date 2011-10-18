# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from lizard_ui.urls import debugmode_urlpatterns
from lizard_area.views import ApiView
from lizard_area.views import Homepage

admin.autodiscover()

urlpatterns = patterns(
    '',
    # (r'^admin/', include(admin.site.urls)),
    url(r'^$', Homepage.as_view(), name='homepage'),
    url(r'^api-view/$', ApiView.as_view(), name='api-view'),
    (r'^api/', include('lizard_area.api.urls', namespace='api')),
    )
urlpatterns += debugmode_urlpatterns()
