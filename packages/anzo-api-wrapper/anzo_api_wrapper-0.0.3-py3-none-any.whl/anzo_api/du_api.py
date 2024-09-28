from typing import List
from urllib.parse import quote_plus

from anzo_api.rest_adapter import RestAdapter
from anzo_api.utils import (
    process_json_result
)
from anzo_api.models import *


class DuApi(object):
    """A class for interacting with an Anzo Server.

    This wraps the Acl API endpoints to simplify building Anzo workflows that require interactions among many
    system assets.

    The general patterns in this class are:
    - AnzoRestApiException is raised if any errors are returned from the API endpoint
    - A TimeoutError is raised if the operation times out
    - API responses are returned as an object representing the Anzo asset
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

    def run_pipeline(self, pipeline_uri, anzo_launch_configuration=None, du_launch_configuration=None,
                     es_launch_configuration=None):
        uri = quote_plus(pipeline_uri)
        data = dict()
        for name, lc in zip(["anzoLaunchConfiguration", "duLaunchConfiguration", "esLaunchConfiguration"],
                            [anzo_launch_configuration, du_launch_configuration, es_launch_configuration]):
            if lc is not None:
                data.update({name: lc})
        self._rest_adapter.post(endpoint=f"unstructured/{uri}/run")
        return True

    def cancel_pipeline(self, pipeline_uri):
        uri = quote_plus(pipeline_uri)
        self._rest_adapter.post(endpoint=f"unstructured/{uri}/cancel")
        return True

    def retrieve_pipeline_status(self, pipeline_uri, detail=False):
        uri = quote_plus(pipeline_uri)
        result = self._rest_adapter.get(endpoint=f"unstructured/{uri}/status")
        res = process_json_result(result)
        return PipelineRun(**res)

