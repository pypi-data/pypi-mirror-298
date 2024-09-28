import os.path
from urllib.parse import quote_plus
from io import BytesIO
from typing import List


from anzo_api.utils import process_json_result, handle_complex_params_retrieval

from anzo_api.rest_adapter import RestAdapter

from anzo_api.models import *


class MigrationPackageApi(object):
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

    def import_migration_package(self, migration_package, new_version_label=None, new_version_comment=None,
                                 current_state_version_label=None, current_state_version_comment=None,
                                 apply_import=False, force=False) -> bool:
        with open(migration_package, 'rb') as f:
            multipart_files = {
                "migrationPackage": (os.path.basename(migration_package), f),
                "newVersionLabel": (None, new_version_label),
                "newVersionComment": (None, new_version_comment),
                "currentStateVersionLabel": (None, current_state_version_label),
                "currentStateVersionComment": (None, current_state_version_comment),
                "applyImport": (None, apply_import)
            }
            params = {"force": force}
            self._rest_adapter.post(endpoint=f"migration/import", ep_params=params, files=multipart_files)
        return True

    def export_migration_package(self, migration_package_uri) -> BytesIO:
        """

        Args:
            migration_package_uri: URI of the migration package

        Returns:
            Native Python BytesIO object
        """
        uri = quote_plus(migration_package_uri)
        result = self._rest_adapter.post(endpoint=f"migration/{uri}/export")
        result_in_bytes = BytesIO(result.content)
        return result_in_bytes

    def create_migration_package(self, title, core_artifacts: list = None, **kwargs):
        # uris = [quote_plus(artifact_uri) for artifact_uri in core_artifacts]
        kwargs.update({'title': title, 'coreArtifacts': core_artifacts})
        result = self._rest_adapter.post(endpoint=f"migration", data=kwargs)
        res = process_json_result(result)
        return MigrationPackage(res)

    def list_migration_packages(self, expand: list = None, mp_filter: dict = None, limit: int = None,
                                offset: int = None, sort: str = None) -> List[MigrationPackage]:
        params = handle_complex_params_retrieval(expand, mp_filter, limit, offset, sort)
        result = self._rest_adapter.get(endpoint="migration", ep_params=params)
        res = process_json_result(result)
        return [MigrationPackage(**mp) for mp in res]

    def retrieve_migration_package(self, migration_package_uri, expand: list = None):
        params = {"expand": ",".join(set(expand).union(["title"]))} if expand is not None else {}  # Include title
        uri = quote_plus(migration_package_uri)
        result = self._rest_adapter.get(endpoint=f"migration/{uri}", ep_params=params)
        res = process_json_result(result)
        return MigrationPackage(**res)