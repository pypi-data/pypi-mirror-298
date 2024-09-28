import os.path
from typing import List
from urllib.parse import quote_plus

from anzo_api.rest_adapter import RestAdapter
from anzo_api.utils import (
    process_json_result
)


class ModelApi(object):
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

    def upload_model(self, model_data) -> bool:
        """
        Uploads an ontology file to Anzo
        Args:
            model_data: Path to a model file

        Returns:
            True
        """
        with open(model_data, 'rb') as f:
            multipart_files = {
                "modelData": (os.path.basename(model_data), f)
            }
            self._rest_adapter.post(endpoint=f"models", files=multipart_files)
        return True

    def retrieve_models(self) -> List[str]:
        result = self._rest_adapter.get(endpoint=f"models")
        res = process_json_result(result)
        return res

    def delete_model(self, model_uri) -> bool:
        uri = quote_plus(model_uri)
        self._rest_adapter.delete(endpoint=f"models/{uri}")
        return True

    def download_model(self, model_uri) -> str:
        uri = quote_plus(model_uri)
        result = self._rest_adapter.get(endpoint=f"models/{uri}")
        return result.data
