import os.path
from typing import List
from urllib.parse import quote_plus

from anzo_api.rest_adapter import RestAdapter
from anzo_api.utils import (
    process_json_result,
    handle_complex_params_retrieval,
    check_valid_instance,
    handle_data_location
)
from anzo_api.models import *


class DatasetApi(object):
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

    def list_datasets(self, expand: list = None, dataset_filter: dict = None, limit: int = None, offset: int = None,
                      sort: str = None) -> List[Dataset]:
        """
        Retrieves all datasets.
        Args:
            expand: Additional fields to pull for dataset
            dataset_filter: Filters datasets by attribute. Translation of "filter".
            limit: Upper bound of data to be returned
            offset: Starting index for returned results
            sort: Property to sort results

        Returns:
            A list of Anzo Dataset objects
        """
        params = handle_complex_params_retrieval(expand, dataset_filter, limit, offset, sort)
        result = self._rest_adapter.get("datasets", ep_params=params)
        res = process_json_result(result)
        return [Dataset(**dataset) for dataset in res]

    def retrieve_dataset(self, dataset_uri, expand: list = None) -> Dataset:
        uri = quote_plus(dataset_uri)
        params = {"expand": set(expand).union("title")} if expand is not None else {}
        result = self._rest_adapter.get(endpoint=f"datasets/{uri}", ep_params=params)
        res = process_json_result(result)
        return Dataset(**res)

    def modify_dataset(self, dataset_uri, **kwargs) -> Dataset:
        uri = quote_plus(dataset_uri)
        result = self._rest_adapter.patch(endpoint=f"datasets/{uri}", data=kwargs)
        res = process_json_result(result)
        return Dataset(**res)

    def delete_dataset(self, dataset_uri) -> bool:
        uri = quote_plus(dataset_uri)
        self._rest_adapter.delete(endpoint=f"datasets/{uri}")
        return True

    def create_flds_from_existing(self, data_location: dict, conflict_resolution: str = None, **kwargs) -> Dataset:
        """

        Args:
            data_location: A configuration specifying the "fileConnection" (file store) "filePath" to data
            conflict_resolution: How to handle existing graph in case of a conflict. Valid input: "rename" or "replace"
            **kwargs: Tags or tag title

        Returns:
            Anzo Dataset
        """
        location = handle_data_location(data_location, kwargs)
        if conflict_resolution not in ["rename", "replace"]:
            raise ValueError("Invalid parameter used for conflict_resolution. Valid options: 'rename' or 'replace'")
        # check_valid_instance(location, CreateDatasetFromFldsRequest) todo: better Dataset models
        params = {"conflict_resolution": conflict_resolution} if conflict_resolution is not None else {}
        kwargs["dataLocation"] = location
        result = self._rest_adapter.post(endpoint="datasets/from-flds", ep_params=params, data=kwargs)
        res = process_json_result(result)
        return Dataset(**res)

    def create_flds_from_flds_zip(self, flds_zip: str, conflict_resolution: str = None) -> Dataset:
        """
        This request imports a dataset from an existing FLDS inside a zip file.
        Args:
            flds_zip: the FLDS zip file to import
            conflict_resolution: How to handle existing graph in case of a conflict. Valid input: "rename" or "replace"
        Returns:
            An Anzo dataset
        """
        if conflict_resolution not in ["rename", "replace"]:
            raise ValueError("Invalid parameter used for conflict_resolution. Valid options: 'rename' or 'replace'")
        params = {"conflict_resolution": conflict_resolution} if conflict_resolution is not None else {}
        zip_file = open(flds_zip, 'rb')
        file_form_data = {"fldsZip": (os.path.basename(flds_zip), zip_file)}
        result = self._rest_adapter.post(endpoint="datasets/from-flds-zip", ep_params=params, files=file_form_data)
        res = process_json_result(result)
        zip_file.close()
        return Dataset(**res)

    def create_flds_from_rdf_directory(self, title: str, data_location: dict, models: List[str] = None, **kwargs) -> Dataset:
        """
        This request creates a dataset from an RDF directory of TTL, NT, or N3 files on a fileConnection. RDF files must
         be placed in a directory named rdf.filetype or rdf.filetype.gz. Place uncompressed TTL files in a directory
         called rdf.ttl, and place compressed TTL files in a directory called rdf.ttl.gz. Place uncompressed N-Triple
         files in a directory called rdf.nt or rdf.n3, depending on the file type extension. Place compressed N-Triple
         files in an rdf.nt.gz or rdf.n3.gz directory. When adding the value for the required filePath body parameter,
         take into account that the value of fileConnection may already contain a partial path to the location of the
         RDF directory and filePath is appended to fileConnection.
        Args:
            title: Title of the created Dataset
            data_location: A configuration specifying the "fileConnection" (file store) "filePath" to data
            models: List of model URIs to associate with the Dataset
            **kwargs: Additional args

        Returns:

        """
        location = handle_data_location(data_location, kwargs)
        kwargs["title"] = title
        kwargs["dataLocation"] = location
        kwargs["models"] = models
        check_valid_instance(kwargs, CreateDatasetFromRdfRequest)
        result = self._rest_adapter.post(endpoint="datasets/from-rdf", data=kwargs)
        res = process_json_result(result)
        return Dataset(**res)

    def create_flds_from_rdf_zip(self, title, rdf_zip, **kwargs) -> Dataset:
        """
        Creates a Dataset from a zip of rdf.ttl files. Uses the user's file store as a landing zone.
        Args:
            title:
            rdf_zip:
            **kwargs:

        Returns:

        """
        kwargs["title"] = title
        with open(rdf_zip, 'rb') as f:
            multipart_form_data = {
                "rdfZip": (os.path.basename(rdf_zip), f),
                "title": (None, title)
            }
            if kwargs is not None:
                for k, v in kwargs.items():
                    multipart_form_data.update({k: (None, v)})
            result = self._rest_adapter.post("datasets/from-rdf-zip", files=multipart_form_data)
        res = process_json_result(result)
        return Dataset(**res)

    def create_empty_flds(self, title: str, data_format: str, data_location: dict, **kwargs) -> Dataset:
        """
        Create an empty dataset at the specified location on a file store. If the directory specified in filePath does
        not exist, it will be created. When providing a filePath, consider the file store also has a built-in path.
        Args:
            title: Title of the created dataset
            data_format: Output format of data. Valid input: 'ttl', 'ttl.gz'. Translation from "format"
            data_location: A dict specifying the "fileConnection" (file store URI) "filePath" to data
        Returns:
            Dataset
        """
        location = handle_data_location(data_location, kwargs)
        if data_format not in ["ttl", "ttl.gz"]:
            raise ValueError("Format must be one of: 'ttl', 'ttl.gz'")
        kwargs["title"] = title
        kwargs["format"] = data_format
        kwargs["dataLocation"] = location
        result = self._rest_adapter.post(endpoint=f"datasets/empty", data=kwargs)
        res = process_json_result(result)
        return Dataset(**res)

    def retrieve_dataset_editions(self, dataset_uri, expand: list = None, edition_filter: dict = None,
                                  limit: int = None, offset: int = None, sort: str = None):
        uri = quote_plus(dataset_uri)
        params = handle_complex_params_retrieval(expand, edition_filter, limit, offset, sort)
        result = self._rest_adapter.get(endpoint=f"datasets/{uri}/editions", ep_params=params)
        res = process_json_result(result)
        return [DatasetEdition(**edition) for edition in res]

    def create_dataset_edition(self, dataset_uri, title, **kwargs):
        uri = quote_plus(dataset_uri)
        kwargs["title"] = title
        result = self._rest_adapter.post(endpoint=f"datasets/{uri}/editions", data=kwargs)
        res = process_json_result(result)
        return DatasetEdition(**res)

    def delete_dataset_edition(self, dataset_uri, edition_uri):
        d_uri = quote_plus(dataset_uri)
        e_uri = quote_plus(edition_uri)
        self._rest_adapter.delete(endpoint=f"datasets/{d_uri}/editions/{e_uri}")
        return True

    def retrieve_dataset_components(self, dataset_uri, expand: list = None, component_filter: dict = None,
                                    limit: int = None, offset: int = None, sort: str = None):
        uri = quote_plus(dataset_uri)
        params = handle_complex_params_retrieval(expand, component_filter, limit, offset, sort)
        result = self._rest_adapter.get(endpoint=f"datasets/{uri}/components", ep_params=params)
        res = process_json_result(result)
        for comp in res:
            comp["component_type"] = comp.pop("type")
        return [DatasetComponent(**component) for component in res]

    def delete_dataset_component(self, dataset_uri, component_uri, delete_on_disk=False, force=False):
        d_uri = quote_plus(dataset_uri)
        c_uri = quote_plus(component_uri)
        params = {"delete_on_disk": delete_on_disk, "force": force}
        self._rest_adapter.delete(endpoint=f"datasets/{d_uri}/components/{c_uri}", ep_params=params)
        return True

    def create_component_from_rdf_file(self, dataset_uri, title, rdf_file, **kwargs):
        uri = quote_plus(dataset_uri)
        with open(rdf_file, 'rb') as f:
            multipart_form_data = {
                "rdfFile": (os.path.basename(rdf_file), f),
                "title": (None, title)
            }
            if kwargs is not None:
                for k, v in kwargs.items():
                    multipart_form_data.update({k: (None, v)})
            result = self._rest_adapter.post(endpoint=f"datasets/{uri}/components/from-file", files=multipart_form_data)
        res = process_json_result(result)
        res["component_type"] = res.pop("type")
        return DatasetComponent(**res)

    def retrieve_edition(self, edition_uri, expand: list = None):
        uri = quote_plus(edition_uri)
        params = {"expand": set(expand).union("title")} if expand is not None else {}
        result = self._rest_adapter.get(endpoint=f"editions/{uri}", ep_params=params)
        res = process_json_result(result)
        return DatasetEdition(**res)

    def modify_edition(self, edition_uri, **kwargs):
        check_valid_instance(kwargs, DatasetEdition)
        uri = quote_plus(edition_uri)
        result = self._rest_adapter.patch(endpoint=f"editions/{uri}", data=kwargs)
        res = process_json_result(result)
        return DatasetEdition(**res)

    def delete_edition(self, edition_uri):
        uri = quote_plus(edition_uri)
        self._rest_adapter.delete(endpoint=f"editions/{uri}")
        return True

    def retrieve_component(self, component_uri, expand: list = None):
        uri = quote_plus(component_uri)
        params = {"expand": set(expand).union("title")} if expand is not None else {}
        result = self._rest_adapter.get(endpoint=f"components/{uri}", ep_params=params)
        res = process_json_result(result)
        res["component_type"] = res.pop("type")
        return DatasetComponent(**res)

    def delete_component(self, component_uri, delete_on_disk=False, force=False):
        uri = quote_plus(component_uri)
        params = {"delete_on_disk": delete_on_disk, "force": force}
        self._rest_adapter.delete(endpoint=f"components/{uri}", ep_params=params)
        return True

    def modify_component(self, component_uri, component_type, **kwargs):
        """

        Args:
            component_uri:  URI of target component
            component_type: Type of component. Options are: DatasetComponent, RdfDatasetComponent,
                            StructuredDatasetComponent, OntDatasetComponent, MaterializedDatasetComponent,
                            MaterializedStructuredDatasetComponent

            **kwargs:
        Returns:

        """
        uri = quote_plus(component_uri)
        kwargs.update({"component_type": component_type})
        check_valid_instance(kwargs, DatasetComponent)
        kwargs["type"] = kwargs.pop("component_type")
        result = self._rest_adapter.patch(endpoint=f"components/{uri}", data=kwargs)
        res = process_json_result(result)
        res["component_type"] = res.pop("type")
        return DatasetComponent(**res)

