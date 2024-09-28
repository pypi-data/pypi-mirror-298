from typing import List, Dict
from json import JSONDecodeError
import requests
import requests.packages

from anzo_api.exceptions import AnzoRestApiException
from anzo_api.models import (
    Result,
    Model,
    Graphmart,
    Layer,
    Step,
    Acl
)


class RestAdapter(object):
    def __init__(self,
                 hostname: str,
                 port: int = None,
                 username: str = "",
                 password: str = "",
                 auth_token: str = "",
                 ssl_verify=False) -> None:
        """
        Constructor for RestAdapter
        Args:
            hostname: Anzo machine hostname
            ssl_verify: Set to false. Use True if you have an SSL/TLS cert
        """
        self.url = hostname
        self.port = port
        self.username = username
        self.password = password
        self.auth_token = auth_token
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings

    def _do(self, http_method, endpoint, headers=None, params=None, data=None, files=None) -> Result:
        """
        Generic class for executing API calls
        Args:
            http_method: API method to execute (GET, POST, PUT, DELETE)
            endpoint: Anzo machine hostname
            headers: Additional headers for Anzo request
            params: additional parameters to add to the request

        Returns:
            Anzo API Result
        """

        if files is not None:
            headers = headers
        elif headers is None:
            headers = {"Content-Type": "application/json"}
        elif "Content-Type" not in headers.keys():
            headers.update({"Content-Type": "application/json"})

        port_str = f":{self.port}" if self.port else ""

        full_url = self.url.rstrip("/") + port_str + "/api/" + endpoint

        if self.auth_token:
            headers.update({'Authorization': self.auth_token})
            auth = None
        else:
            auth = (self.username, self.password)
        try:
            response = requests.request(
                method=http_method,
                url=full_url,
                auth=auth,
                params=params,
                headers=headers,
                json=data,
                files=files,
                verify=self._ssl_verify
            )
        except requests.exceptions.RequestException as e:
            raise AnzoRestApiException("Request failed") from e
        if 200 <= response.status_code <= 299:     # OK
            return Result(response.status_code, data=response.text, content=response.content)
        try:
            res = response.json()
        except JSONDecodeError as e:
            raise AnzoRestApiException("Response returned malformed json") from e
        raise AnzoRestApiException(f"Response returned with non-success code {response.status_code}"
                                   f" and message: '{res['summary']}'")

    def get(self, endpoint, headers=None, ep_params=None, data=None) -> Result:
        return self._do(http_method='GET', endpoint=endpoint, headers=headers, params=ep_params)

    def post(self, endpoint: str, headers=None, ep_params=None, data=None, files=None) -> Result:
        return self._do(http_method='POST', endpoint=endpoint, headers=headers, params=ep_params, data=data,
                        files=files)

    def put(self, endpoint: str, headers=None, ep_params=None, data=None) -> Result:
        return self._do(http_method='PUT', endpoint=endpoint, headers=headers, params=ep_params, data=data)

    def patch(self, endpoint: str, headers=None, ep_params=None, data=None) -> Result:
        return self._do(http_method='PATCH', endpoint=endpoint, headers=headers, params=ep_params, data=data)

    def delete(self, endpoint: str, ep_params=None) -> Result:
        return self._do(http_method='DELETE', endpoint=endpoint)
