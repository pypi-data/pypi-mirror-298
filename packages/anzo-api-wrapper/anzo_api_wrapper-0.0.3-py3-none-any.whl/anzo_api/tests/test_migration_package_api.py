from unittest import TestCase
from typing import List
from anzo_api.migration_package_api import MigrationPackageApi
from anzo_api.graphmart_api import GraphmartApi
from anzo_api.tests.test_utils.test_common import *
from anzo_api.models import *
from io import BytesIO


class TestMigrationPackageApi(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.anzo = MigrationPackageApi(DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)
        cls.gmAnzo = GraphmartApi(DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)
        cls.gm = cls.gmAnzo.create_graphmart(
            title="Unittest - Migration Graphmart"
        )

    @classmethod
    def tearDownClass(cls):
        cls.gmAnzo.delete_graphmart(cls.gm.uri)

    def setUp(self):
        self.migration_uri = "http://cambridgesemantics.com/MigrationPackage/6f27007afef546d1b5fbba9062bc1d9c"

    def test_import_migration_package(self):
        result = self.anzo.import_migration_package(migration_package="./test_utils/ExamplePackage_20240320181221.zip")
        self.assertTrue(result)

    def test_export_migration_package(self):
        self.anzo.import_migration_package(migration_package="./test_utils/ExamplePackage_20240320181221.zip")
        result = self.anzo.export_migration_package(migration_package_uri=self.migration_uri)
        self.assertIsInstance(result, BytesIO)

    def test_create_migration_package(self):
        result = self.anzo.create_migration_package(title="My Test Migration Package", core_artifacts=[self.gm.uri])
        self.assertIsInstance(result, MigrationPackage)

    def test_list_migration_packages(self):
        packages = self.anzo.list_migration_packages()
        types_are_packages = [isinstance(mp, MigrationPackage) for mp in packages]
        self.assertTrue(all(types_are_packages))

    def test_retrieve_migration_package(self):
        packages = self.anzo.list_migration_packages()
        package_uri = packages[0].uri
        package = self.anzo.retrieve_migration_package(package_uri)
        self.assertTrue(isinstance(package, MigrationPackage))


    # todo: add more tests