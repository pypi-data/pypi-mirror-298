from unittest import TestCase
from typing import List
from anzo_api.model_api import ModelApi
from anzo_api.tests.test_utils.test_common import *


class TestModelApi(TestCase):

    def setUp(self):
        self.anzo = ModelApi(DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)
        self.mesh_uri = "http://id.nlm.nih.gov/mesh/vocab"

    def test_upload_model(self):
        result = self.anzo.upload_model(model_data="./test_utils/meshontology-ont.trig")
        self.assertTrue(result)

    def test_retrieve_models(self):
        result = self.anzo.retrieve_models()
        self.assertIsInstance(result, list)

    def test_delete_model(self):
        result = self.anzo.delete_model(model_uri=self.mesh_uri)
        models = self.anzo.retrieve_models()
        self.assertTrue(result and self.mesh_uri not in models)

    def test_download_model(self):
        self.anzo.upload_model(model_data="./test_utils/meshontology-ont.trig")
        result = self.anzo.download_model(model_uri=self.mesh_uri)
        self.assertTrue(self.mesh_uri in result)
