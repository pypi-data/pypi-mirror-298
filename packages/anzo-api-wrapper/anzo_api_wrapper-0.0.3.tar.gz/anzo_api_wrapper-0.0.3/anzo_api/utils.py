from json import JSONDecodeError, loads
from urllib.parse import quote
from typing import Union

from anzo_api.exceptions import AnzoRestApiException
from anzo_api.models import *

STEP_TYPE_REF = { # Assigns string representation of step to models defined in models.py
    "QueryStep": QueryStep,
    "DirectLoadStep": DirectLoadStep,
    "LoadDatasetStep": LoadDatasetStep,
    "QueryDefinedView": View,
    "ExportStep": ExportStep
}


def process_json_result(result) -> Union[dict, list]:
    """Utility to unpack the request result against the API. Only used when API request returns Anzo artifacts
        Args:
            result: The output of the request to the Anzo API endpoint

        Returns:
            A dictionary or list of dictionaries of assets
    """
    try:
        res = loads(result.data)
    except JSONDecodeError as e:
        raise AnzoRestApiException("The API call returned a malformed response") from e
    return res


def handle_complex_params_retrieval(expand, asset_filter, limit, offset, sort) -> dict:
    """Validates params provided for "retrieve" functions and transform into expected shape.
        Args:
            expand: A list of properties to attach to the object
            asset_filter: A dictionary of properties and values to filter on
            limit: The upper bound of assets to return
            offset: The index for the first asset in list
            sort: The property to sort returned assets with

        Returns:
            A dictionary of valid parameters to be passed to the API request
    """
    params = dict()
    for k, v in zip(["expand", "filter", "limit", "offset", "sort"], [expand, asset_filter, limit, offset, sort]):
        if k == "expand" and v is not None:
            expand_include_title = set(v).union(["title"])
            params[k] = ",".join(expand_include_title)
        elif k == "filter" and v is not None:
            if len(v) == 1:
                for prop, filterVal in v.items():
                    params[k] = quote(":".join([prop, f'"{filterVal}"']))
            else:
                raise ValueError("*_filter property accepts dictionary of length: 1")
        elif v is not None:
            params[k] = v
    return params


def check_valid_instance(obj, model, modify=False):
    """Validates construction of object sent to Anzo according to the defined model. Used predominantly for step
        validation.
        Args:
            obj: A dictionary representing an Anzo asset
            model: The model definition of the Anzo artifact
            modify: True for "modify" (usually PATCH) requests

        Returns:
            None
    """
    if model is Step and not modify:
        step_type = obj.get("step_type") if obj.get("step_type") is not None else obj.get("type")
        if step_type not in STEP_TYPE_REF.keys():
            raise ValueError(f"Invalid step type provided. Valid step types are: {list(STEP_TYPE_REF.keys())}")
        model = STEP_TYPE_REF[step_type]
    try:
        model(**obj)
    except TypeError as e:
        raise AnzoRestApiException(f"Invalid construction for {model.__name__}") from e


def handle_data_location(data_location: dict, provided_args: dict) -> dict:
    """Validates payload before sending to Anzo. Data location requests require nested definitions. Used for datasets
        Args:
            data_location: Required fields for data location: a dict with URI of a filestore, path to write.
            provided_args: Optional fields for data location: title, isPrimary, checksum

        Returns:
            A dictionary of valid parameters
    """
    if "fileConnection" not in data_location.keys() or "filePath" not in data_location.keys():
        raise ValueError("fileConnection and filePath are required keys for data_location.")
    if provided_args.get("dataLocation") is not None:
        for arg, v in provided_args.get("dataLocation").items():
            if arg in ["title", "isPrimary", "checksum"]:
                data_location.update({arg: v})
    return data_location
