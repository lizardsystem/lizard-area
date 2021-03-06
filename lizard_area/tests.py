# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.test import TestCase

import json

from lizard_area.views import ApiView
from lizard_area.views import Homepage

from lizard_area.api.views import RootView
from lizard_area.api.views import CategoryRootView
from lizard_area.api.views import AreaViewForTree

from lizard_area.api.resources import CommuniqueResource
from lizard_area.api.resources import AreaResource
from lizard_area.api.resources import CategoryResource

from lizard_area.sync_areas import Synchronizer


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
        AreaViewForTree().get(mock_request)

    def test_smoke_resource(self):
        CommuniqueResource(None)
        AreaResource(None)
        CategoryResource(None)


class AreaSynchronizationTest(TestCase):
    def test_jsondict2mp(self):
        geojson_file = open(
            'lizard_area/testsources/peilgebieden_from_wfs.json')
        content = json.loads(geojson_file.read())
        geojson_file.close()
        synchronizer = Synchronizer()
        self.assertTrue(synchronizer.check_content(content))

    def test_replace_suffix(self):
        date_string = "11-11-2012"
        synchronizer = Synchronizer()
        self.assertTrue(date_string == synchronizer.replace_suffix(
                "{0}Z".format(date_string)))
        self.assertFalse(date_string == synchronizer.replace_suffix(None))
        self.assertTrue(date_string == synchronizer.replace_suffix(date_string))
