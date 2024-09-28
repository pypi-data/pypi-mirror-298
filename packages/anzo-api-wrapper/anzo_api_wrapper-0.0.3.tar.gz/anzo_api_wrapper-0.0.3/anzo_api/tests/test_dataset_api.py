from unittest import TestCase

from anzo_api.dataset_api import DatasetApi
from anzo_api.exceptions import AnzoRestApiException
from anzo_api.models import *
from anzo_api.tests.test_utils.test_common import *


class TestDatasetApi(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.anzo = DatasetApi(DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)
        cls.file_store = FILE_STORE_URI
        cls.dataset = cls.anzo.create_empty_flds(
            title="My Empty API Dataset", data_format="ttl",
            data_location={
                "fileConnection": cls.file_store,
                "filePath": "setup-class"})
        cls.component = cls.anzo.create_component_from_rdf_file(
            dataset_uri=cls.dataset.uri,
            title="Set Up Component URI",
            rdf_file="./test_utils/233.ttl")
        cls.edition = cls.anzo.create_dataset_edition(
            dataset_uri=cls.dataset.uri,
            title="Set Up Edition",
            components=[cls.component.as_dict()]
        )
        cls.anzo.modify_dataset(
            dataset_uri=cls.dataset.uri,
            workingEdition=cls.edition.uri
        )

    @classmethod
    def tearDownClass(cls):
        cls.anzo.delete_dataset(dataset_uri=cls.dataset.uri)
        cls.anzo.delete_component(component_uri=cls.component.uri, delete_on_disk=True, force=True)

    def test_list_datasets_returns_datasets(self):
        result = self.anzo.list_datasets()
        results_are_datasets = [isinstance(dataset, Dataset) for dataset in result]
        self.assertTrue(results_are_datasets)

    def test_retrieve_dataset_returns_dataset(self):
        result = self.anzo.retrieve_dataset(dataset_uri=self.dataset.uri)
        self.assertIsInstance(result, Dataset)

    def test_modify_dataset(self):
        result = self.anzo.modify_dataset(dataset_uri=self.dataset.uri, description="Modifying a dataset")
        self.assertIsInstance(result, Dataset)

    def test_delete_dataset(self):
        dataset = self.anzo.create_empty_flds(
            title="My Empty API Dataset", data_format="ttl",
            data_location={
                "fileConnection": self.file_store,
                "filePath": "delete-dataset"})
        result = self.anzo.delete_dataset(dataset_uri=dataset.uri)
        self.assertTrue(result)

    def test_create_flds_from_existing(self):
        result = self.anzo.create_flds_from_existing(
            data_location={
                "fileConnection": self.file_store,
                "filePath": "delete-dataset"},
            conflict_resolution="rename"
        )
        self.anzo.delete_dataset(dataset_uri=result.uri)
        self.assertIsInstance(result, Dataset)

    def test_create_flds_from_flds_zip(self):
        result = self.anzo.create_flds_from_flds_zip(
            flds_zip=PATH_TO_FLDS_ZIP,
            conflict_resolution="rename"
        )
        self.anzo.delete_dataset(result.uri)
        self.assertIsInstance(result, Dataset)

    def test_fail_create_flds_from_flds_zip_no_flds(self):
        with self.assertRaises(FileNotFoundError):
            self.anzo.create_flds_from_flds_zip(
                "/no/path/should/exist.zip",
                conflict_resolution="rename")

    def test_create_flds_from_rdf_directory(self):
        result = self.anzo.create_flds_from_rdf_directory(
            title="Create FLDS From RDF Directory",
            data_location={
                "fileConnection": self.file_store,
                "filePath": PATH_TO_RDF_TTL
            }
        )
        self.anzo.delete_dataset(result.uri)
        self.assertIsInstance(result, Dataset)

    def test_create_flds_from_rdf_zip(self):
        result = self.anzo.create_flds_from_rdf_zip(
            title="Zipped 300 Small TTL Files",
            rdf_zip="/opt/anzoshare/small-ttl-zip/rdf.ttl.zip"
        )
        self.assertIsInstance(result, Dataset)

    def test_create_empty_flds_returns_dataset(self):
        result = self.anzo.create_empty_flds(
            title="My Empty API Dataset", data_format="ttl",
            data_location={
                "fileConnection": self.file_store,
                "filePath": "my-empty-api-dataset"})
        self.anzo.delete_dataset(result.uri)
        self.assertIsInstance(result, Dataset)

    def test_retrieve_dataset_editions(self):
        result = self.anzo.retrieve_dataset_editions(
            dataset_uri=self.dataset.uri
        )
        results_are_editions = [isinstance(edition, DatasetEdition) for edition in result]
        self.assertTrue(all(results_are_editions))

    def test_create_dataset_edition(self):
        edition = self.anzo.create_dataset_edition(
            title="Test Create Dataset Edition",
            dataset_uri=self.dataset.uri
        )
        self.anzo.delete_edition(edition.uri)
        self.assertIsInstance(edition, DatasetEdition)

    def test_delete_dataset_edition(self):
        edition = self.anzo.create_dataset_edition(
            title="Test Create Dataset Edition",
            dataset_uri=self.dataset.uri
        )
        result = self.anzo.delete_edition(edition.uri)
        self.assertTrue(result)

    def test_retrieve_dataset_components(self):
        result = self.anzo.retrieve_dataset_components(dataset_uri=self.dataset.uri)
        results_are_components = [isinstance(component, DatasetComponent) for component in result]
        self.assertTrue(all(results_are_components))

    def test_create_component_from_rdf_file(self):
        component = self.anzo.create_component_from_rdf_file(
            dataset_uri=self.dataset.uri,
            title="Test Create Component From RDF File",
            rdf_file="test_utils/233.ttl"
        )
        self.anzo.delete_dataset_component(
            dataset_uri=self.dataset.uri,
            component_uri=component.uri
        )
        self.assertIsInstance(component, DatasetComponent)

    def test_delete_dataset_component(self):
        component = self.anzo.create_component_from_rdf_file(
            dataset_uri=self.dataset.uri,
            title="Test Create Component From RDF File",
            rdf_file="test_utils/233.ttl"
        )
        result = self.anzo.delete_dataset_component(
            dataset_uri=self.dataset.uri,
            component_uri=component.uri
        )
        self.assertTrue(result)

    def test_retrieve_edition(self):
        result = self.anzo.retrieve_edition(edition_uri=self.edition.uri)
        self.assertIsInstance(result, DatasetEdition)

    def test_modify_edition(self):
        modified_edition = self.anzo.modify_edition(
            edition_uri=self.edition.uri,
            comment="Test  Modify Edition"
        )
        self.assertIsInstance(modified_edition, DatasetEdition)

    def test_delete_edition(self):
        edition = self.anzo.create_dataset_edition(
            title="A Deleted Edition",
            dataset_uri=self.dataset.uri
        )
        result = self.anzo.delete_edition(edition_uri=edition.uri)
        self.assertTrue(result)

    def test_retrieve_component(self):
        result = self.anzo.retrieve_component(component_uri=self.component.uri)
        self.assertIsInstance(result, DatasetComponent)

    def test_delete_component(self):
        component = self.anzo.create_component_from_rdf_file(
            dataset_uri=self.dataset.uri,
            title="My API Component",
            rdf_file="test_utils/233.ttl"
        )
        result = self.anzo.delete_component(
            component_uri=component.uri,
            delete_on_disk=True
        )
        self.assertTrue(result)

    def test_modify_component(self):
        result = self.anzo.modify_component(
            component_uri=self.component.uri,
            component_type="RdfDatasetComponent",
            title="Test Modify Component"
        )
        self.assertTrue(result)
