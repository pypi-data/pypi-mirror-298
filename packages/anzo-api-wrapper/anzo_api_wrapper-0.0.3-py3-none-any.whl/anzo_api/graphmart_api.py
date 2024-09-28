from typing import List
from urllib.parse import quote_plus

from anzo_api.rest_adapter import RestAdapter
from anzo_api.anzo_statics import STEP_SOURCE_DEFAULT
from anzo_api.utils import (
    process_json_result,
    handle_complex_params_retrieval,
    check_valid_instance
)
from anzo_api.models import *


class GraphmartApi(object):
    """A class for interacting with an Anzo Server.

    This wraps the Anzo API endpoints to simplify building Anzo workflows that require interactions among many
    system assets.

    The general patterns in this class are:
    - AnzoRestApiException is raised if any errors are returned from the API endpoint
    - A TimeoutError is raised if the operation times out
    - API responses are returned as an object representing the Anzo asset (i.e. Graphmart, Layer, Model, etc.)
    """
    def __init__(self,
                 hostname,
                 port,
                 path="",
                 username="",
                 password="",
                 auth_token="",
                 ssl_verify=False):
        self._rest_adapter = RestAdapter(hostname, port, username, password, auth_token, ssl_verify)

    def list_graphmarts(self, expand: list = None, gm_filter: dict = None, limit: int = None, offset: int = None,
                        sort: str = None) -> List[Graphmart]:
        """

        Args:
            expand: A list of properties to attach to the Graphmart object
            gm_filter: A dictionary of properties and values to filter on
            limit: The upper bound of Graphmarts to return
            offset: The index for the first Graphmart in list
            sort: The property to sort returned Graphmarts with

        Returns:
            A list of Graphmart objects
        """
        params = handle_complex_params_retrieval(expand, gm_filter, limit, offset, sort)
        result = self._rest_adapter.get(endpoint="graphmarts", ep_params=params)
        res = process_json_result(result)
        return [Graphmart(**gm) for gm in res]

    def create_graphmart(self, title, **kwargs) -> Graphmart:
        """Creates a Graphmart
        Returns:
            Anzo Graphmart object
        """
        kwargs["title"] = title
        result = self._rest_adapter.post(endpoint="graphmarts", data=kwargs)
        res = process_json_result(result)
        return Graphmart(**res)

    def retrieve_graphmart(self, graphmart_uri, expand: List[str] = None) -> Graphmart:
        params = {"expand": ",".join(set(expand).union(["title"]))} if expand is not None else {}  # Include title
        uri = quote_plus(graphmart_uri)
        result = self._rest_adapter.get(endpoint=f"graphmarts/{uri}", ep_params=params)
        res = process_json_result(result)
        return Graphmart(**res)

    def create_or_replace_graphmart(self, graphmart_uri, title, force=False, **kwargs) -> Graphmart:
        """

        Args:
            graphmart_uri: URI for Graphmart
            title: Title of Graphmart. Does not have to match existing title.
            force: Required True to send request.
            **kwargs:

        Returns:
            A Graphmart Asset
        Note:
            When creating a new Graphmart, "title" is a required function parameter
        """
        params = {"force": True} if force else {}
        kwargs["title"] = title
        uri = quote_plus(graphmart_uri)
        result = self._rest_adapter.put(endpoint=f"graphmarts/{uri}", ep_params=params, data=kwargs)
        res = process_json_result(result)
        return Graphmart(**res)

    def modify_graphmart(self, graphmart_uri, **kwargs) -> Graphmart:
        params = dict()
        uri = quote_plus(graphmart_uri)
        result = self._rest_adapter.patch(endpoint=f"graphmarts/{uri}", ep_params=params, data=kwargs)
        res = process_json_result(result)
        return Graphmart(**res)

    def delete_graphmart(self, graphmart_uri) -> bool:
        """

        Args:
            graphmart_uri: The URI of the graphmart to delete

        Returns:
            boolean

        """
        uri = quote_plus(graphmart_uri)
        self._rest_adapter.delete(endpoint=f"graphmarts/{uri}")
        return True

    def retrieve_graphmart_status(self, graphmart_uri, detail=False) -> Status:
        params = dict()
        uri = quote_plus(graphmart_uri)
        if detail:
            params["detail"] = detail
        result = self._rest_adapter.get(endpoint=f"graphmarts/{uri}/status", ep_params=params)
        res = process_json_result(result)
        return Status(**res)

    def activate_graphmart(self, graphmart_uri, **kwargs) -> bool:
        """Activates a Graphmart
        Args:
            graphmart_uri: The URI of the graphmart to activate

        Returns:
            True if Graphmart is activated
        """
        uri = quote_plus(graphmart_uri)
        self._rest_adapter.post(endpoint=f"graphmarts/{uri}/activate", data=kwargs)
        return True

    def deactivate_graphmart(self, graphmart_uri) -> bool:
        uri = quote_plus(graphmart_uri)
        self._rest_adapter.post(endpoint=f"graphmarts/{uri}/deactivate")
        return True

    def refresh_graphmart(self, graphmart_uri) -> bool:
        uri = quote_plus(graphmart_uri)
        self._rest_adapter.post(endpoint=f"graphmarts/{uri}/refresh")
        return True

    def reload_graphmart(self, graphmart_uri) -> bool:
        uri = quote_plus(graphmart_uri)
        self._rest_adapter.post(endpoint=f"graphmarts/{uri}/reload")
        return True

    def retrieve_graphmart_layers(self, graphmart_uri, expand: list = None, gm_filter: dict = None, limit: int = None,
                                  offset: int = None, sort: str = None) -> List[Layer]:
        uri = quote_plus(graphmart_uri)
        params = handle_complex_params_retrieval(expand, gm_filter, limit, offset, sort)
        result = self._rest_adapter.get(endpoint=f"graphmarts/{uri}/layers", ep_params=params)
        res = process_json_result(result)
        return [Layer(**layer) for layer in res]

    def create_graphmart_layer(self, graphmart_uri, title, **kwargs):
        uri = quote_plus(graphmart_uri)
        kwargs["title"] = title
        result = self._rest_adapter.post(endpoint=f"graphmarts/{uri}/layers", data=kwargs)
        res = process_json_result(result)
        return Layer(**res)

    def replace_all_graphmart_layers(self, graphmart_uri, layers: list, force=False):
        for layer in layers:
            check_valid_instance(layer, Layer)
        params = {"force": True} if force else {}
        uri = quote_plus(graphmart_uri)
        result = self._rest_adapter.put(endpoint=f"graphmarts/{uri}/layers", ep_params=params, data=layers)
        res = process_json_result(result)
        return [Layer(**layer) for layer in res]

    def delete_all_graphmart_layers(self, graphmart_uri):
        uri = quote_plus(graphmart_uri)
        self._rest_adapter.delete(endpoint=f"graphmarts/{uri}/layers")
        return True

    def delete_graphmart_layer(self, graphmart_uri, layer_uri):
        gm_uri = quote_plus(graphmart_uri)
        l_uri = quote_plus(layer_uri)
        self._rest_adapter.delete(endpoint=f"graphmarts/{gm_uri}/layers/{l_uri}")
        return True

    def create_or_replace_graphmart_layer(self, graphmart_uri, layer_uri, force=False, **kwargs) -> bool:
        """
        Creates a Layer in Graphmart with a specified URI
        Args:
            graphmart_uri: URI of Graphmart to add Layer
            layer_uri: URI of Layer
            force: Manually set to True to allow to overwrite of data
            **kwargs: Parameters acceptable for Layer schema

        Returns:
            bool
        """
        gm_uri = quote_plus(graphmart_uri)
        l_uri = quote_plus(layer_uri)
        params = {"force": True} if force else {}
        check_valid_instance(kwargs, Layer)
        self._rest_adapter.put(endpoint=f"graphmarts/{gm_uri}/layers/{l_uri}", ep_params=params, data=kwargs)
        return True

    def move_graphmart_layer(self, graphmart_uri, layer_uri, before_layer="", after_layer=""):
        if not before_layer and not after_layer:
            raise ValueError("One of 'before_uri' or 'after_uri' must be set")
        if before_layer and after_layer:
            raise ValueError("Only one of 'before_uri' or 'after_uri' can be set")
        params = dict()
        if before_layer:
            params["before"] = before_layer
        if after_layer:
            params["after"] = after_layer
        gm_uri = quote_plus(graphmart_uri)
        l_uri = quote_plus(layer_uri)
        self._rest_adapter.post(endpoint=f"graphmarts/{gm_uri}/layers/{l_uri}/move", ep_params=params)
        return True

    def enable_layers(self, graphmart_uri, layer_uris: list, include_steps=False) -> bool:
        """
        Enable a list of layers specified by URI within a Graphmart.
        Args:
            graphmart_uri: URI of the Graphmart the Layers are in
            layer_uris: A list of layer URIs
            include_steps: Enables steps if true. Otherwise will not change steps.
            fail_on_error: todo add fail_on_error after filing ticket; not seeing difference in response

        Returns:
            bool
        Raises:
            AnzoRestApiException
        """
        uri = quote_plus(graphmart_uri)
        params = {"include_steps": include_steps}
        # params["fail_on_error"] = fail_on_error
        self._rest_adapter.patch(endpoint=f"graphmarts/{uri}/enableLayers", ep_params=params, data=layer_uris)
        return True

    def disable_layers(self, graphmart_uri, layer_uris: list, include_steps=False):
        uri = quote_plus(graphmart_uri)
        params = {"include_steps": include_steps}
        # params["fail_on_error"] = fail_on_error
        self._rest_adapter.patch(endpoint=f"graphmarts/{uri}/disableLayers", ep_params=params, data=layer_uris)
        return True

    def refresh_layer(self, layers: list) -> True:
        """

        Args:
            layers: A list of layer URIs to refresh

        Returns:
            bool
        """
        params = {"layers": layers}
        self._rest_adapter.post(endpoint=f"layers/refresh", ep_params=params)
        return True

    def retrieve_layer(self, layer_uri, expand: list = None):
        params = dict()
        if expand:
            expand_include_title = set(expand).union(["title"])
            params = ",".join(expand_include_title)
        uri = quote_plus(layer_uri)
        result = self._rest_adapter.get(endpoint=f"layers/{uri}", ep_params=params)
        res = process_json_result(result)
        return Layer(**res)

    def modify_layer(self, layer_uri, **kwargs):
        # check_valid_instance(kwargs, Layer) todo: create separate models for modify and create
        uri = quote_plus(layer_uri)
        result = self._rest_adapter.patch(endpoint=f"layers/{uri}", data=kwargs)
        res = process_json_result(result)
        return Layer(**res)

    def delete_layer(self, layer_uri):
        uri = quote_plus(layer_uri)
        self._rest_adapter.delete(endpoint=f"layers/{uri}")
        return True

    def retrieve_layer_steps(self, layer_uri, expand: list = None, gm_filter: dict = None, limit: int = None,
                             offset: int = None, sort: str = None):
        params = handle_complex_params_retrieval(expand, gm_filter, limit, offset, sort)
        uri = quote_plus(layer_uri)
        result = self._rest_adapter.get(endpoint=f"layers/{uri}/steps", ep_params=params)
        res = process_json_result(result)
        for step in res:
            step["step_type"] = step.pop("type")
        return [Step(**step) for step in res]

    def create_layer_step(self, layer_uri, title, step_type, source_layers: list = None, **kwargs):
        """

        Args:
            layer_uri: Specified URI for Layer
            title: Title of the Step
            step_type: Type of step. Valid types: 'DirectLoadStep', 'QueryStep', 'QueryDrivenTemplatedStep',
                                             'LoadDatasetStep', 'ExportStep', 'ElasticsearchIndexingStep',
                                             'ElasticsearchSnapshotStep', 'InferenceStep',
                                             'TemplatedStep', 'ValidationStep', 'PreCompileQueryStep'
            source_layers: Layers that step operates against. If none are provided, uses default steps "Self" and
                           "All Previous Layers Within Graphmart"
            **kwargs: Additional parameters to attach to the step
        Returns:
            Anzo Step
        """
        if source_layers is None:
            source_layers = STEP_SOURCE_DEFAULT
        kwargs.update({"title": title, "step_type": step_type, "source": source_layers})
        check_valid_instance(kwargs, Step)
        kwargs["type"] = kwargs.pop("step_type")  # Dancing around using reserved variable "type"
        uri = quote_plus(layer_uri)
        result = self._rest_adapter.post(endpoint=f"layers/{uri}/steps", data=kwargs)
        res = process_json_result(result)
        res["step_type"] = res.pop("type")
        return Step(**res)

    def replace_all_layer_steps(self, layer_uri, steps: List[dict], force=False):
        uri = quote_plus(layer_uri)
        data = []
        for step in steps:
            if "source" not in step.keys():
                step.update({"source": STEP_SOURCE_DEFAULT})
            check_valid_instance(step, Step)
            step['type'] = step.pop("step_type")
            data.append(step)
        params = {"force": True} if force else {}
        result = self._rest_adapter.put(endpoint=f"layers/{uri}/steps", ep_params=params, data=data)
        res = process_json_result(result)
        for step in res:
            step["step_type"] = step.pop("type")
        return [Step(**step) for step in res]

    def delete_all_layer_steps(self, layer_uri):
        uri = quote_plus(layer_uri)
        self._rest_adapter.delete(endpoint=f"layers/{uri}/steps")
        return True

    def delete_layer_step(self, layer_uri, step_uri):
        l_uri = quote_plus(layer_uri)
        s_uri = quote_plus(step_uri)
        self._rest_adapter.delete(endpoint=f"layers/{l_uri}/steps/{s_uri}")
        return True

    def create_or_replace_layer_step(self, layer_uri, step_uri, force=False, **kwargs):
        l_uri = quote_plus(layer_uri)
        s_uri = quote_plus(step_uri)
        params = {"force": True} if force else {}
        kwargs['source'] = STEP_SOURCE_DEFAULT if kwargs.get("source") is None else kwargs.get("source")
        check_valid_instance(kwargs, Step)
        kwargs['type'] = kwargs.pop("step_type")
        self._rest_adapter.put(endpoint=f"layers/{l_uri}/steps/{s_uri}", ep_params=params, data=kwargs)
        return True

    def retrieve_layer_status(self, layer_uri, detail=False) -> Status:
        uri = quote_plus(layer_uri)
        params = {"detail": detail}
        result = self._rest_adapter.get(endpoint=f"layers/{uri}/status", ep_params=params)
        res = process_json_result(result)
        return Status(**res)

    def enable_layer_steps(self, layer_uri, step_uris: list = None, include_layer=False):
        uri = quote_plus(layer_uri)
        params = {"includeLayer": include_layer}
        layer_steps = self.retrieve_layer_steps(layer_uri)
        valid_uris = [step.uri for step in layer_steps]
        for candidate_uri in step_uris:
            if candidate_uri not in valid_uris:
                raise ValueError(f"Step URI '{candidate_uri}' does not exist in layer '{layer_uri}'")
                # todo: get titles
        self._rest_adapter.patch(endpoint=f"layers/{uri}/enableSteps", ep_params=params, data=step_uris)
        return True

    def disable_layer_steps(self, layer_uri, step_uris: list = None, include_layer=False):
        uri = quote_plus(layer_uri)
        params = {"includeLayer": include_layer}
        layer_steps = self.retrieve_layer_steps(layer_uri)
        valid_uris = [step.uri for step in layer_steps]
        for candidate_uri in step_uris:
            if candidate_uri not in valid_uris:
                raise ValueError(f"Step URI '{candidate_uri}' does not exist in layer '{layer_uri}'")
                # todo: get titles
        self._rest_adapter.patch(endpoint=f"layers/{uri}/enableSteps", ep_params=params, data=step_uris)
        return True

    # todo: refactor views and steps to use same function with view parameterized
    def retrieve_layer_views(self, layer_uri, expand: list = None, gm_filter: dict = None, limit: int = None,
                             offset: int = None, sort: str = None):
        params = handle_complex_params_retrieval(expand, gm_filter, limit, offset, sort)
        uri = quote_plus(layer_uri)
        result = self._rest_adapter.get(endpoint=f"layers/{uri}/views", ep_params=params)
        res = process_json_result(result)
        for view in res:
            view["step_type"] = view.pop("type")
        return [View(**view) for view in res]

    def create_layer_view(self, layer_uri, title, source_layers: list = None, **kwargs):
        """

        Args:
            layer_uri: Specified URI for Layer
            title: Title of the Step
            source_layers: Layers that step operates against. If none are provided, uses default steps "Self" and
                           "All Previous Layers Within Graphmart"
            **kwargs: Additional parameters to attach to the step
        Returns:
            Anzo Step
        """
        if source_layers is None:
            source_layers = STEP_SOURCE_DEFAULT
        kwargs.update({"title": title, "step_type": "QueryDefinedView", "source": source_layers})
        check_valid_instance(kwargs, View)
        kwargs["type"] = kwargs.pop("step_type")  # Dancing around using reserved variable "type"
        uri = quote_plus(layer_uri)
        result = self._rest_adapter.post(endpoint=f"layers/{uri}/views", data=kwargs)
        res = process_json_result(result)
        res["step_type"] = res.pop("type")
        return View(**res)

    def replace_all_layer_views(self, layer_uri, views: List[dict], force=False):
        uri = quote_plus(layer_uri)
        data = []
        for view in views:
            if "source" not in view.keys():
                view.update({"source": STEP_SOURCE_DEFAULT})
            view.update({"step_type": "QueryDefinedView"})
            check_valid_instance(view, View)
            view['type'] = view.pop("step_type")
            data.append(view)
        params = {"force": True} if force else {}
        result = self._rest_adapter.put(endpoint=f"layers/{uri}/views", ep_params=params, data=data)
        res = process_json_result(result)
        return [View(**view) for view in res]

    def delete_all_layer_views(self, layer_uri):
        uri = quote_plus(layer_uri)
        self._rest_adapter.delete(endpoint=f"layers/{uri}/views")
        return True

    def delete_layer_view(self, layer_uri, view_uri):
        l_uri = quote_plus(layer_uri)
        v_uri = quote_plus(view_uri)
        self._rest_adapter.delete(endpoint=f"layers/{l_uri}/views/{v_uri}")
        return True

    def create_or_replace_layer_view(self, layer_uri, view_uri, force=False, **kwargs):
        l_uri = quote_plus(layer_uri)
        v_uri = quote_plus(view_uri)
        params = {"force": True} if force else {}
        kwargs['source'] = STEP_SOURCE_DEFAULT if kwargs.get("source") is None else kwargs.get("source")
        kwargs['step_type'] = "QueryDefinedView"
        check_valid_instance(kwargs, View)
        kwargs['type'] = kwargs.pop("step_type")
        self._rest_adapter.put(endpoint=f"layers/{l_uri}/views/{v_uri}", ep_params=params, data=kwargs)
        return True

    def enable_layer_views(self, layer_uri, view_uris: list = None, include_layer=False):
        uri = quote_plus(layer_uri)
        params = {"includeLayer": include_layer}
        layer_views = self.retrieve_layer_views(layer_uri)
        valid_uris = [view.uri for view in layer_views]
        for candidate_uri in view_uris:
            if candidate_uri not in valid_uris:
                raise ValueError(f"Step URI '{candidate_uri}' does not exist in layer '{layer_uri}'")
                # todo: get titles
        self._rest_adapter.patch(endpoint=f"layers/{uri}/enableViews", ep_params=params, data=valid_uris)
        return True

    def disable_layer_views(self, layer_uri, view_uris: list = None, include_layer=False):
        uri = quote_plus(layer_uri)
        params = {"includeLayer": include_layer}
        layer_views = self.retrieve_layer_views(layer_uri)
        valid_uris = [view.uri for view in layer_views]
        for candidate_uri in view_uris:
            if candidate_uri not in valid_uris:
                raise ValueError(f"Step URI '{candidate_uri}' does not exist in layer '{layer_uri}'")
                # todo: get titles
        self._rest_adapter.patch(endpoint=f"layers/{uri}/enableSteps", ep_params=params, data=view_uris)
        return True

    def retrieve_step(self, step_uri, expand: List[str] = None):
        uri = quote_plus(step_uri)
        # Always include title and type in params
        params = {"expand": ",".join(set(expand).union(["title", "type"]))} if expand is not None else {}
        result = self._rest_adapter.get(endpoint=f"steps/{uri}", ep_params=params)
        res = process_json_result(result)
        res['step_type'] = res.pop("type")
        return Step(**res)

    def modify_step(self, step_uri, step_type, **kwargs):
        uri = quote_plus(step_uri)
        kwargs["type"] = step_type
        result = self._rest_adapter.patch(endpoint=f"steps/{uri}", data=kwargs)
        res = process_json_result(result)
        res['step_type'] = res.pop('type')
        return Step(**res)

    def delete_step(self, step_uri):
        uri = quote_plus(step_uri)
        self._rest_adapter.delete(endpoint=f"steps/{uri}")
        return True

    def retrieve_view(self, view_uri, expand: List[str] = None):
        uri = quote_plus(view_uri)
        # Always include title and type in params
        params = {"expand": ",".join(set(expand).union(["title", "type"]))} if expand is not None else {}
        result = self._rest_adapter.get(endpoint=f"views/{uri}", ep_params=params)
        res = process_json_result(result)
        res['step_type'] = res.pop("type")
        return View(**res)

    def modify_view(self, view_uri, **kwargs):
        uri = quote_plus(view_uri)
        view_type = "QueryDefinedView"
        kwargs["type"] = view_type
        result = self._rest_adapter.patch(endpoint=f"views/{uri}", data=kwargs)
        res = process_json_result(result)
        res['step_type'] = res.pop('type')
        return View(**res)

    def delete_view(self, view_uri):
        uri = quote_plus(view_uri)
        self._rest_adapter.delete(endpoint=f"views/{uri}")
        return True

    def retrieve_step_status(self, step_uri, detail=False):
        uri = quote_plus(step_uri)
        params = {"detail": detail}
        result = self._rest_adapter.get(endpoint=f"steps/{uri}/status", ep_params=params)
        res = process_json_result(result)
        return Status(**res)


