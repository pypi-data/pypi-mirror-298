from anzo_api.graphmart_api import GraphmartApi
from anzo_api.dataset_api import DatasetApi
from anzo_api.acl_api import AclApi
from anzo_api.du_api import DuApi
from anzo_api.model_api import ModelApi
from anzo_api.migration_package_api import MigrationPackageApi
from anzo_api.azg_api import AzgApi
from anzo_api.launch_config_api import LaunchConfigApi


class AnzoApi(GraphmartApi, DatasetApi, AclApi, ModelApi, MigrationPackageApi, AzgApi, LaunchConfigApi, DuApi):
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
                 port: int = None,
                 path="",
                 username="",
                 password="",
                 auth_token="",
                 ssl_verify=False):
        super().__init__(hostname, port, path, username, password, auth_token, ssl_verify)
        """

        Args:
            hostname: Hostname of the Anzo instance
            port: Port for Anzo API (usually 8443)
            path (optional): Additional path for validation with a proxy
            username (optional): Username for the user executing Anzo API calls
            password (optional): Password of the user
            auth_token (optional): The authentication token that is used
            ssl_verify (optional): Path to SSL/TLS certificate. Default is False.
        Returns:
            An Anzo asset
        """
        if username and not password:
            error = "If a username is specified a password also needs to be"
            raise ValueError(error)

        if password and not username:
            error = "If password is specified a username also needs to be"
            raise ValueError(error)

        if username and password and auth_token:
            error = "Username and password specified as well as an auth_token"
            raise ValueError(error)

        if not (username or password or auth_token):
            error = "Some form of authentication must be provided."
            raise ValueError(error)
