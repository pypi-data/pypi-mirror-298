from typing import List
from urllib.parse import quote_plus

from anzo_api.rest_adapter import RestAdapter
from anzo_api.utils import (
    process_json_result
)
from anzo_api.models import *


class AclApi(object):
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

    def retrieve_acls(self, object_uri, acl_inherited_by: bool = True) -> AclDetailsView:
        uri = quote_plus(object_uri)
        params = {"aclInheritedBy": acl_inherited_by}
        result = self._rest_adapter.get(endpoint=f"acls/{uri}", ep_params=params)
        res = process_json_result(result)
        return AclDetailsView(**res)

    def replace_acls(self, acl_edits: List[dict], preserve_inheritance=True) -> bool:
        """
        This request sets the ACLs for an object by replacing all existing ACLs with the ones in the request.
        Args:
            acl_edits: A list of dictionaries indicating asset URIs and their ACLs.
            preserve_inheritance: Boolean indicator to keep existing inherited ACLs
        Returns:
            True if the operation is successful
        Notes:
            acl_edits should define at most one of "explicitAcls" or "explicitShortFormAcls"
            Edit dictionaries should adhere to the following format:
                {
                    "subject": str,
                    "inheritedAcls": List[str],
                    "metaInheritedAcls": List[str],
                    "explicitAcls": [{
                        "role": str,
                        "acl": str [Options: VIEW, ADD, DELETE, METAVIEW, METAADD, METADELETE]
                    }],
                    "explicitShortFormAcls": [{
                        "role": str,
                        "access": str [Options: VIEW, MODIFY, ADMIN]
                    }]
                }
        """
        data = {
            "aclEdits": acl_edits,
            "preserveInheritance": preserve_inheritance
        }
        for edit in acl_edits:
            AclDetailsSet(edit)
        self._rest_adapter.post(endpoint=f"acls/set", data=data)
        return True

    def modify_acls(self, acl_edits: List[dict]) -> bool:
        """
        This request modifies the ACLs for an object by adding or removing ACL statements. Requests for removals of
        statements that do not exist will not trigger errors. ACLs are processed in the order given. If there are
        conflicts, the last statements override previous statements.
        Args:
            acl_edits: A list of dictionaries indicating asset URIs and their ACL updates.
        Returns:
            bool
        Notes:
            acl_edits should define at most one of "explicitAclsToAdd" or "explicitShortFormAclsToAdd"
            acl_edits should define at most one of "explicitAclsToRemove" or "explicitShortFormAclsToRemove"
            Edit dictionaries should adhere to the following format:
                {
                    "subject": str,
                    "inheritedAclsToAdd": List[str],
                    "metaInheritedAclsToAdd": List[str],
                    "inheritedAclsToRemove": List[str],
                    "metaInheritedAclsToRemove": List[str],
                    "explicitAclsToAdd": [{
                        "role": str,
                        "acl": str [Options: VIEW, ADD, DELETE, METAVIEW, METAADD, METADELETE]
                    }],
                    "explicitAclsToRemove": [{
                        "role": str,
                        "acl": str [Options: VIEW, ADD, DELETE, METAVIEW, METAADD, METADELETE]
                    }],
                    "explicitShortFormAclsToAdd": [{
                        "role": str,
                        "access": str [Options: VIEW, MODIFY, ADMIN]
                    }],
                    "explicitShortFormAclsToRemove": [{
                        "role": str,
                        "access": str [Options: VIEW, MODIFY, ADMIN]
                    }]
                }
        """
        data = {"aclEdits": acl_edits}
        for edit in acl_edits:
            AclDetailsEdit(edit)
        self._rest_adapter.post(endpoint=f"acls/edit", data=data)
        return True

    def reset_acls(self, object_uri) -> bool:
        """
        This request updates the ACLs for the given object by resetting the statements according to the associated
        Default Access Policy. Inheritance statements are not modified by this method.
        Args:
            object_uri:

        Returns:
            bool
        """
        uri = quote_plus(object_uri)
        self._rest_adapter.post(endpoint=f"acls/reset/{uri}")
        return True

