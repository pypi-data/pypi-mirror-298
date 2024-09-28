from unittest import TestCase, mock

from anzo_api.graphmart_api import GraphmartApi
from anzo_api.launch_config_api import LaunchConfigApi
from anzo_api.dataset_api import DatasetApi
from anzo_api.exceptions import AnzoRestApiException
from anzo_api.models import *
from anzo_api.tests.test_utils.test_common import DOMAIN, PORT, USERNAME, PASSWORD, FILE_STORE_URI


class TestAnzoApi(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.anzo = GraphmartApi(hostname=DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)
        cls.gm_view_config = {
            "title": "Unittest View",
            "description": "View created from API",
            "type": "QueryDefinedView",
            "step_type": "QueryDefinedView",
            "enabled": True,
            "source": STEP_SOURCE_DEFAULT,
            "transformQuery": "CONSTRUCT {<urn:testStatement> <urn:testPredicate> 'Hello World'} WHERE { ?s a <urn://nil> .}"
        }
        cls.gm_step_config = {
            "title": "Unittest Step",
            "description": "Step created from API",
            "type": "QueryStep",
            "step_type": "QueryStep",
            "enabled": True,
            "source": STEP_SOURCE_DEFAULT,
            "transformQuery": "INSERT DATA {<urn:testStatement> <urn:testPredicate> 'Hello World'}"
        }
        cls.gm_layer_config = {
            "title": "Unittest Layer",
            "description": "Layer created from API",
            "enabled": True,
            "layerStep": [cls.gm_step_config],
            "view": [cls.gm_view_config]
        }
        cls.gm = cls.anzo.create_graphmart(
            title="Unittest Graphmart",
            layer=[cls.gm_layer_config]
        )

    @classmethod
    def tearDownClass(cls):
        cls.anzo.delete_graphmart(cls.gm.uri)

    def setUp(self):
        self.graphmart = self.anzo.retrieve_graphmart(self.gm.uri, expand=["layer", "layer.layerStep", "layer.view"])
        # In case layers get deleted during test
        try:
            self.layer = Layer(**self.graphmart.layer[0])
        except (AttributeError, IndexError):
            self.layer = self.anzo.create_graphmart_layer(graphmart_uri=self.graphmart.uri, **self.gm_layer_config)
        try:
            self.step = QueryStep(**self.layer.layerStep[0])
        except TypeError:
            self.step = self.layer.layerStep[0]
        except (AttributeError, KeyError, IndexError) as e:
            self.step = self.anzo.create_layer_step(layer_uri=self.layer.uri, **self.gm_step_config)
        try:
            self.view = View(**self.layer.view[0])
        except TypeError:
            self.view = self.layer.view[0]
        except (AttributeError, KeyError, IndexError) as e:
            self.view = self.anzo.create_layer_view(layer_uri=self.layer.uri, **self.gm_view_config)
        self.bad_uri = "csi.com/Graphmart"
        self.valid_layers_config = [{"title": "My First Layer", "enabled": True}, {"title": "My Second Layer"}]
        self.valid_step_uri = "http://csi.com/Step/TestStep"
        self.valid_view_uri = "http://csi.com/View/TestView"
        self.transformQuery = """INSERT DATA { <http://csi.com/Example> <http://csi.com/prop> 'Hello World' } """
        self.valid_steps_config = [{"title": "My First Step", "enabled": True, "step_type": "QueryStep",
                                    "transformQuery": self.transformQuery},
                                   {"title": "My Second Step", "step_type": "QueryStep",
                                    "transformQuery": self.transformQuery}]
        self.valid_views_config = [{"title": "My First View", "enabled": True, "transformQuery": self.transformQuery},
                                   {"title": "My Second View", "transformQuery": self.transformQuery}]

    def test_list_graphmarts_results_are_graphmarts(self):
        graphmarts = self.anzo.list_graphmarts()
        types_are_graphmarts = [isinstance(gm, Graphmart) for gm in graphmarts]
        self.assertTrue(all(types_are_graphmarts))

    def test_list_graphmarts_with_valid_expand(self):
        graphmarts = self.anzo.list_graphmarts(expand=["description", "creator"])
        types_are_graphmarts = [isinstance(gm, Graphmart) for gm in graphmarts]
        self.assertTrue(all(types_are_graphmarts))

    def test_fail_list_graphmarts_with_invalid_expand(self):
        with self.assertRaises(AnzoRestApiException):
            self.anzo.list_graphmarts(expand=["nastyProp"])

    def test_retrieve_graphmart_result_is_graphmart(self):
        graphmart = self.anzo.retrieve_graphmart(
            graphmart_uri=self.graphmart.uri)
        self.assertTrue(isinstance(graphmart, Graphmart))

    def test_fail_retrieve_graphmart_with_invalid_uri(self):
        with self.assertRaises(AnzoRestApiException):
            self.anzo.retrieve_graphmart(graphmart_uri="http://csi.com/BadGraphmart")

    def test_create_graphmart_result_is_graphmart(self):
        graphmart = self.anzo.create_graphmart(title="Create from test suite")
        self.anzo.delete_graphmart(graphmart_uri=graphmart.uri)
        self.assertTrue(isinstance(graphmart, Graphmart))

    def test_create_graphmart_with_args_result_is_graphmart(self):
        graphmart = self.anzo.create_graphmart(title="Create from test suite with params",
                                               description="I was created from a test suite.")
        self.anzo.delete_graphmart(graphmart_uri=graphmart.uri)
        self.assertTrue(isinstance(graphmart, Graphmart))

    def test_create_or_replace_graphmart_new_graphmart_result_is_graphmart(self):
        graphmart = self.anzo.create_or_replace_graphmart(
            graphmart_uri="http://csi.com/PutAGraphmart", title="Put New Graphmart", force=True)
        self.assertTrue(isinstance(graphmart, Graphmart))

    def test_create_or_replace_existing_graphmart_result_is_graphmart(self):
        graphmart = self.anzo.create_or_replace_graphmart(
            graphmart_uri="http://csi.com/PutAGraphmart", title="Put New Graphmart", description="Describe Graphmart",
            force=True)
        self.assertTrue(isinstance(graphmart, Graphmart))

    def test_fail_create_or_replace_graphmart_without_force(self):
        with self.assertRaises(AnzoRestApiException):
            self.anzo.create_or_replace_graphmart(
                graphmart_uri="http://csi.com/PutAGraphmart", title="Put New Graphmart")

    def test_fail_create_or_replace_graphmart_with_bad_uri(self):
        with self.assertRaises(AnzoRestApiException):
            self.anzo.create_or_replace_graphmart(
                graphmart_uri="putagraphmart.com", title="Put an Invalid Graphmart", force=True)

    def test_modify_graphmart_result_is_graphmart(self):
        graphmart = self.anzo.modify_graphmart(graphmart_uri=self.graphmart.uri, description="Test Modify Graphmart.")
        self.assertTrue(isinstance(graphmart, Graphmart))

    def test_fail_modify_graphmart_with_invalid_uri(self):
        with self.assertRaises(AnzoRestApiException):
            self.anzo.modify_graphmart(graphmart_uri="putagraphmart.com")

    def test_delete_graphmart_result_is_ok_status_code(self):
        result = self.anzo.delete_graphmart(graphmart_uri="http://csi.com/PutAGraphmart")
        self.assertTrue(result)

    def test_fail_delete_graphmart_with_invalid_uri(self):
        with self.assertRaises(AnzoRestApiException):
            self.anzo.delete_graphmart(graphmart_uri="putagraphmart.com")

    def test_retrieve_graphmart_status_result_is_graphmart_status(self):
        result = self.anzo.retrieve_graphmart_status(graphmart_uri=self.graphmart.uri)
        self.assertIsInstance(result, Status)

    def test_retrieve_graphmart_status_result_with_detail_is_graphmart_status(self):
        result = self.anzo.retrieve_graphmart_status(graphmart_uri=self.graphmart.uri, detail=True)
        self.assertIsInstance(result, Status)

    def test_fail_retrieve_graphmart_status_with_invalid_uri(self):
        with self.assertRaises(AnzoRestApiException):
            self.anzo.retrieve_graphmart_status(graphmart_uri=self.bad_uri)

    def test_activate_graphmart_is_true(self):
        launch_configs = LaunchConfigApi(hostname=DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)\
            .list_azg_launch_configs()
        result = self.anzo.activate_graphmart(self.graphmart.uri, azgLaunchConfiguration=launch_configs[0].__dict__)
        self.assertTrue(result)

    def test_fail_activate_graphmart_bad_uri(self):
        with self.assertRaises(AnzoRestApiException):
            self.anzo.activate_graphmart(self.bad_uri)

    def test_retrieve_graphmart_layers_result_is_layers(self):
        layers = self.anzo.retrieve_graphmart_layers(graphmart_uri=self.graphmart.uri)
        types_are_layers = [isinstance(layer, Layer) for layer in layers]
        self.assertTrue(all(types_are_layers))

    def test_create_graphmart_layer_result_is_layer(self):
        layer = self.anzo.create_graphmart_layer(graphmart_uri=self.graphmart.uri, title="New Layer from API")
        self.assertIsInstance(layer, Layer)

    def test_replace_all_graphmart_layers_is_layers(self):
        layers = self.anzo.replace_all_graphmart_layers(self.graphmart.uri, layers=self.valid_layers_config, force=True)
        types_are_layers = [isinstance(layer, Layer) for layer in layers]
        self.assertTrue(all(types_are_layers))

    def test_delete_all_graphmart_layers(self):
        result = self.anzo.delete_all_graphmart_layers(self.graphmart.uri)
        self.assertTrue(result)

    def test_delete_graphmart_layer(self):
        new_layer = self.anzo.create_graphmart_layer(self.graphmart.uri, title="Delete Graphmart Layer")
        result = self.anzo.delete_graphmart_layer(graphmart_uri=self.graphmart.uri, layer_uri=new_layer.uri)
        self.assertTrue(result)

    def test_create_or_replace_graphmart_layer(self):
        new_layer = self.anzo.create_graphmart_layer(self.graphmart.uri, title="Create or Replace GM Layer")
        result = self.anzo.create_or_replace_graphmart_layer(
            graphmart_uri=self.graphmart.uri, layer_uri=new_layer.uri, force=True,
            title="Created Another Layer")
        self.assertTrue(result)

    def test_move_graphmart_layer(self):
        layer = self.anzo.create_graphmart_layer(self.graphmart.uri, "Layer 2")
        result = self.anzo.move_graphmart_layer(
            self.graphmart.uri, layer_uri=self.layer.uri, after_layer=layer.uri)
        self.assertTrue(result)

    def test_enable_layers(self):
        result = self.anzo.enable_layers(graphmart_uri=self.graphmart.uri, layer_uris=[self.layer.uri])
        self.assertTrue(result)

    def test_refresh_layer(self):
        result = self.anzo.refresh_layer(layers=[self.layer.uri])
        self.assertTrue(result)

    def test_retrieve_layer_result_is_layer(self):
        result = self.anzo.retrieve_layer(layer_uri=self.layer.uri)
        self.assertIsInstance(result, Layer)

    def test_modify_layer_result_is_layer(self):
        result = self.anzo.modify_layer(layer_uri=self.layer.uri, description="Patched layer.")
        self.assertIsInstance(result, Layer)

    def test_delete_layer(self):
        new_layer = self.anzo.create_graphmart_layer(graphmart_uri=self.graphmart.uri, title="Test Delete Layer")
        result = self.anzo.delete_layer(layer_uri=new_layer.uri)
        self.assertTrue(result)

    def test_retrieve_layer_steps(self):
        result = self.anzo.retrieve_layer_steps(layer_uri=self.layer.uri)
        results_are_steps = [isinstance(step, Step) for step in result]
        self.assertTrue(all(results_are_steps))

    def test_create_layer_step(self):
        # todo: this test needs a lot more support
        result = self.anzo.create_layer_step(
            layer_uri=self.layer.uri, title="Create Layer Step", step_type="QueryStep",
            description="Created from API", transformQuery=self.transformQuery)
        self.assertIsInstance(result, Step)

    def test_create_layer_export_step(self):
        dataset_api = DatasetApi(hostname=DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)
        dataset = dataset_api.create_empty_flds(
            title="Test Create Export Step",
            data_format="ttl",
            data_location={
                "fileConnection": FILE_STORE_URI,
                "filePath": "setup-class"}
        )
        result = self.anzo.create_layer_step(
            layer_uri=self.layer.uri, title="Create Layer Export Step", step_type="ExportStep",
            description="Created from API", gmLinkedDataset=dataset.cat_entry_uri)
        self.assertIsInstance(result, Step)

    def test_replace_all_layer_steps(self):
        result = self.anzo.replace_all_layer_steps(
            layer_uri=self.layer.uri, steps=self.valid_steps_config, force=True)
        valid_steps = [isinstance(step, Step) for step in result]
        self.assertTrue(all(valid_steps))

    def test_delete_all_layer_steps(self):
        result = self.anzo.delete_all_layer_steps(self.layer.uri)
        self.assertTrue(result)

    def test_delete_layer_step(self):
        step = self.anzo.create_layer_step(
            self.layer.uri, title="Delete Layer Step", step_type="QueryStep", transformQuery=self.transformQuery)
        result = self.anzo.delete_layer_step(self.layer.uri, step.uri)
        self.assertTrue(result)

    def test_create_or_replace_layer_step(self):
        step = self.anzo.create_or_replace_layer_step(
            self.layer.uri, step_uri=self.valid_step_uri, **self.valid_steps_config[0],
            description="Adding a description", force=True)
        self.assertTrue(step)

    def test_retrieve_layer_status(self):
        status = self.anzo.retrieve_layer_status(self.layer.uri)
        self.assertIsInstance(status, Status)

    def test_enable_layer_steps(self):
        enabled = self.anzo.enable_layer_steps(
            layer_uri=self.layer.uri,
            step_uris=[self.step['uri']])
        self.assertTrue(enabled)

    def test_disable_layer_steps(self):
        disabled = self.anzo.enable_layer_steps(
            layer_uri=self.layer.uri,
            step_uris=[self.step['uri']])
        self.assertTrue(disabled)

    def test_retrieve_layer_views(self):
        result = self.anzo.retrieve_layer_views(layer_uri=self.layer.uri)
        results_are_views = [isinstance(view, View) for view in result]
        self.assertTrue(all(results_are_views))

    def test_create_layer_views(self):
        result = self.anzo.create_layer_view(
            layer_uri=self.layer.uri, title="Create Layer View",
            description="Created from API", transformQuery=self.transformQuery)
        self.assertIsInstance(result, View)

    def test_replace_all_layer_views(self):
        result = self.anzo.replace_all_layer_views(
            layer_uri=self.layer.uri, views=self.valid_views_config, force=True)
        valid_views = [isinstance(view, View) for view in result]
        self.assertTrue(all(valid_views))

    def test_delete_all_layer_views(self):
        result = self.anzo.delete_all_layer_views(self.layer.uri)
        self.assertTrue(result)

    def test_delete_layer_view(self):
        view = self.anzo.create_layer_view(
            self.layer.uri, title="Delete Layer View", transformQuery=self.transformQuery)
        result = self.anzo.delete_layer_view(self.layer.uri, view.uri)
        self.assertTrue(result)

    def test_create_or_replace_layer_view(self):
        view = self.anzo.create_or_replace_layer_view(
            self.layer.uri, view_uri=self.valid_view_uri, **self.valid_views_config[0],
            description="Adding a description", force=True)
        self.assertTrue(view)

    def test_enable_layer_views(self):
        enabled = self.anzo.enable_layer_views(
            layer_uri=self.layer.uri,
            view_uris=[self.view['uri']])
        self.assertTrue(enabled)

    def test_disable_layer_views(self):
        disabled = self.anzo.enable_layer_views(
            layer_uri=self.layer.uri,
            view_uris=[self.view['uri']])
        self.assertTrue(disabled)

    def test_retrieve_step(self):
        step = self.anzo.retrieve_step(step_uri=self.step['uri'])
        self.assertIsInstance(step, Step)

    def test_modify_step(self):
        step = self.anzo.modify_step(
            step_uri=self.step['uri'], step_type="QueryStep", description="Adding a description")
        self.assertIsInstance(step, Step)

    def test_delete_step(self):
        new_step = self.anzo.create_layer_step(self.layer.uri, **self.gm_step_config)
        deleted = self.anzo.delete_step(step_uri=new_step.uri)
        self.assertTrue(deleted)

    def test_retrieve_view(self):
        view = self.anzo.retrieve_view(view_uri=self.view['uri'])
        self.assertIsInstance(view, View)

    def test_modify_view(self):
        view = self.anzo.modify_view(
            view_uri=self.view['uri'], description="Adding a description")
        self.assertIsInstance(view, View)

    def test_delete_view(self):
        new_view = self.anzo.create_layer_view(self.layer.uri, **self.gm_view_config)
        deleted = self.anzo.delete_view(view_uri=new_view.uri)
        self.assertTrue(deleted)

    def test_retrieve_step_status(self):
        status = self.anzo.retrieve_step_status(step_uri=self.step['uri'])
        self.assertIsInstance(status, Status)
