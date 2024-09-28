from unittest import TestCase
from anzo_api.azg_api import AzgApi
from anzo_api.models import Anzograph
from anzo_api.tests.test_utils.test_common import DOMAIN, PORT, USERNAME, PASSWORD


class TestAzgApi(TestCase):
    def setUp(self):
        self.anzo = AzgApi(DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)

    def test_list_static_azgs(self):
        result = self.anzo.list_static_azgs()
        results_are_azg = [isinstance(azg, Anzograph) for azg in result]
        self.assertTrue(all(results_are_azg))
