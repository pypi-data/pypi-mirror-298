import os.path
from typing import List
from urllib.parse import quote_plus

from anzo_api.rest_adapter import RestAdapter
from anzo_api.utils import (
    process_json_result,
    handle_complex_params_retrieval
)
from anzo_api.models import *


class LaunchConfigApi(object):
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

    def list_azg_launch_configs(self, expand: list = None, launch_config_filter: dict = None, limit: int = None,
                                offset: int = None, sort: str = None) -> List[AnzographLaunchConfig]:
        params = handle_complex_params_retrieval(expand, launch_config_filter, limit, offset, sort)
        result = self._rest_adapter.get(endpoint="launchconfigs/azg", ep_params=params)
        res = process_json_result(result)
        return [AnzographLaunchConfig(**alc) for alc in res]

    def list_es_launch_configs(self, expand: list = None, launch_config_filter: dict = None, limit: int = None,
                               offset: int = None, sort: str = None) -> List[ElasticSearchLaunchConfig]:
        params = handle_complex_params_retrieval(expand, launch_config_filter, limit, offset, sort)
        result = self._rest_adapter.get(endpoint="launchconfigs/elastic", ep_params=params)
        res = process_json_result(result)
        return [ElasticSearchLaunchConfig(**alc) for alc in res]
