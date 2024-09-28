from unittest import TestCase
from typing import List
from anzo_api.launch_config_api import LaunchConfigApi
from anzo_api.graphmart_api import GraphmartApi
from anzo_api.tests.test_utils.test_common import *
from anzo_api.models import *


class TestLaunchConfigApi(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.anzo = LaunchConfigApi(DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)

    def test_list_azg_launch_configs(self):
        configs = self.anzo.list_azg_launch_configs()
        are_azg_launch_configs = [isinstance(config, AnzographLaunchConfig) for config in configs]
        self.assertTrue(all(are_azg_launch_configs))

    def test_list_es_launch_configs(self):
        self.fail()
