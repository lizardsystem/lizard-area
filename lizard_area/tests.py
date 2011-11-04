# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.test import TestCase

from lizard_area.views import ApiView
from lizard_area.views import Homepage

from lizard_area.api.views import RootView
from lizard_area.api.views import CategoryRootView
from lizard_area.api.views import KRWAreaView
from lizard_area.api.views import CatchmentAreaView

from lizard_area.api.resources import CommuniqueResource
from lizard_area.api.resources import AreaResource
from lizard_area.api.resources import CategoryResource


class ViewsTest(TestCase):
    def test_smoke_api_view(self):
        self.assertTrue(ApiView())

    def test_smoke_homepage(self):
        self.assertTrue(Homepage())


class ApiTest(TestCase):
    def test_smoke_api(self):
        class MockRequest(object):
            GET = {}
        mock_request = MockRequest()
        RootView().get(mock_request)
        CategoryRootView().get(mock_request)
        KRWAreaView().get(mock_request)
        CatchmentAreaView().get(mock_request)

    def test_smoke_resource(self):
        CommuniqueResource(None)
        AreaResource(None)
        CategoryResource(None)
