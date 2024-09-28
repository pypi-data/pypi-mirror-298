from anzo_api.anzo_construct import *
from urllib.parse import quote_plus


class Result(object):
    def __init__(self, status_code, data=None, content=None):
        """

        Args:
            status_code: Standard HTTP status code
            data: Data returned for endpoint
            content: Files returned from endpoint
        """
        self.status_code = int(status_code)
        self.data = data if data else []
        self.content = content if content else []


class AnzoAsset(object):
    def __str__(self):
        return f"{self.uri}"

    def __repr__(self):
        return (f"{type(self).__name__}"
                f"(title={self.title}, "
                f"uri={self.uri})")

    def __getitem__(self, key):
        return getattr(self, key)

    def as_dict(self):
        return self.__dict__

    def list_props(self):
        return list(self.__dict__.keys())


class Model(object):
    def __init__(self, uri, title):
        self.uri = uri


# Graphmart API
class Graphmart(AnzoAsset):
    def __init__(self, uri, title, **kwargs):
        self.uri = uri
        self.title = title
        self.__dict__.update(kwargs)


class Status(object):
    def __init__(self, status, **kwargs):
        self.status = status
        self.__dict__.update(kwargs)

    def __repr__(self):
        return (f"{type(self).__name__}"
                f"(status={self.status})")


class Layer(AnzoAsset):
    def __init__(self, title, **kwargs):
        self.title = title
        self.__dict__.update(kwargs)

    @staticmethod
    def basic(with_step=False):
        if with_step:
            return BASIC_LAYER.update({"layerStep": BASIC_QUERY_STEP})
        return BASIC_LAYER


class Step(AnzoAsset):
    def __init__(self, title, source, **kwargs):
        super().__init__()
        if "type" not in kwargs.keys() and "step_type" not in kwargs.keys():
            raise ValueError("Either step_type or type must be provided as a parameter")
        self.title = title
        self.step_type = kwargs["step_type"] if "step_type" in kwargs.keys() else kwargs["type"]
        self.source = source
        self.__dict__.update(kwargs)


class QueryStep(Step):
    def __init__(self, title, source, transformQuery, **kwargs):
        super().__init__(title, source, **kwargs)
        self.transformQuery = transformQuery

    @staticmethod
    def query_template():
        return QUERY_TEMPLATE

    @staticmethod
    def basic():
        return BASIC_QUERY_STEP


class DirectLoadStep(Step):
    def __init__(self, title, source, transformQuery, **kwargs):
        super().__init__(title, source, **kwargs)
        self.transformQuery = transformQuery

    @staticmethod
    def query_template():
        return DIRECT_LOAD_TEMPLATE


class LoadDatasetStep(Step):
    def __init__(self, title, source, gmLinkedDataset, **kwargs):
        super().__init__(title, source, **kwargs)
        self.gmLinkedDataset = gmLinkedDataset


class ExportStep(Step):
    def __init__(self, title, source, gmLinkedDataset, **kwargs):
        super().__init__(title, source, **kwargs)
        self.gmLinkedDataset = gmLinkedDataset


class View(AnzoAsset):
    def __init__(self, **kwargs):
        if "type" not in kwargs.keys() and "step_type" not in kwargs.keys():
            raise ValueError("Either step_type or type must be provided as a parameter")
        super().__init__(**kwargs)
        self.__dict__.update(kwargs)

    @staticmethod
    def query_template():
        return VIEW_TEMPLATE


class Acl(object):
    def __init__(self, subject):
        self.subject = subject

    @staticmethod
    def options():
        return DEFAULT_ROLE_URI_REF


# Dataset API
class Dataset(AnzoAsset):
    def __init__(self, uri, **kwargs):
        super().__init__()
        self.uri = uri
        self.cat_entry_uri = self.create_cat_entry_uri(uri)
        self.__dict__.update(kwargs)

    @staticmethod
    def create_cat_entry_uri(uri):
        encoded_uri = quote_plus(uri)
        cat_entry_uri = (f"http://openanzo.org/catEntry(%5B{encoded_uri}%5D%40%5B"
                         f"http%3A%2F%2Fopenanzo.org%2Fdatasource%2FsystemDatasource%5D)")
        return cat_entry_uri


class CreateDatasetFromFldsRequest(object):
    def __init__(self, dataLocation, **kwargs):
        self.fileConnection = dataLocation['fileConnection']
        self.filePath = dataLocation['filePath']
        self.__dict__.update(kwargs)


class CreateDatasetFromRdfRequest(CreateDatasetFromFldsRequest):
    def __init__(self, dataLocation, title, **kwargs):
        super().__init__(dataLocation, **kwargs)
        self.title = title
        self.__dict__.update(kwargs)


class DatasetEdition(AnzoAsset):
    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)


class DatasetComponent(AnzoAsset):
    def __init__(self, component_type, **kwargs):
        super().__init__()
        self.component_type = component_type
        self.__dict__.update(kwargs)

    @staticmethod
    def options():
        return COMPONENT_TYPES


# ACL API
class AclDetailsView(object):
    def __init__(self, subject, **kwargs):
        self.subject = subject
        self.__dict__.update(kwargs)

    def __repr__(self):
        return (f"{type(self).__name__}"
                f"(subject={self.subject})")

    def access_control_definition(self):
        acl_props = self.__dict__.copy()
        acl_props.pop("subject")
        return list(acl_props.keys())


class AclDetailsSet(object):
    def __init__(self, edit):
        edit_details = [
            edit.get("inheritedAcls"),
            edit.get("metaInheritedAcls"),
            edit.get("explicitAcls"),
            edit.get("explicitShortFormAcls")
        ]
        if edit.get("explicitAcls") is not None and edit.get("explicitShortFormAcls") is not None:
            raise ValueError("Only one of explicitAcls or explicitShortFormAcls should be set")
        if not any(edit_details):
            raise ValueError("At least one field must be set for edits: inheritedAcls, metaInheritedAcls, explicitAcls,"
                             " explicitShortFormAcls.")
        for detail in edit_details:
            if detail is not None and not isinstance(detail, list):
                raise ValueError("The specified fields must be of type 'list': inheritedAcls, metaInheritedAcls, "
                                 "explicitAcls, explicitShortFormAcls")

        self.subject = edit.get('subject')
        self.inheritsFrom = edit.get('inheritedAcls')
        self.metaInheritsFrom = edit.get('metaInheritedAcls')
        self.explicitAcls = edit.get("explicitAcls")
        self.explicitShortFormAcls = edit.get("explicitShortFormAcls")


class AclDetailsEdit(object):
    def __init__(self, edit):
        edit_details = [
            edit.get("inheritedAclsToAdd"),
            edit.get("inheritedAclsToRemove"),
            edit.get("metaInheritedAclsToAdd"),
            edit.get("metaInheritedAclsToRemove"),
            edit.get("explicitAclsToAdd"),
            edit.get("explicitAclsToRemove"),
            edit.get("explicitShortFormAclsToAdd"),
            edit.get("explicitShortFormAclsToRemove")
        ]
        if not any(edit_details):
            raise ValueError("At least one field must be set for edits")
        for detail in edit_details:
            if detail is not None and not isinstance(detail, list):
                raise ValueError("The edit fields must be of type 'list'")
        self.edit = edit


class MigrationPackage(AnzoAsset):
    def __init__(self, title, **kwargs):
        super().__init__()
        self.title = title
        self.__dict__.update(kwargs)


class Anzograph(AnzoAsset):
    def __init__(self, title, host, **kwargs):
        super().__init__()
        self.title = title
        self.host = host
        self.__dict__.update(kwargs)


class LaunchConfig(AnzoAsset):
    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)


class AnzographLaunchConfig(LaunchConfig):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ElasticSearchLaunchConfig(LaunchConfig):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# DU Api
class PipelineRun(object):
    def __init__(self, uri, **kwargs):
        self.uri = uri
        self.__dict__.update(kwargs)
