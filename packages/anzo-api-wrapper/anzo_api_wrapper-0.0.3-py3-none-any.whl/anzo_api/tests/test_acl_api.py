from unittest import TestCase
from anzo_api.acl_api import AclApi
from anzo_api.anzo_api import AnzoApi
from anzo_api.models import *
from anzo_api.anzo_statics import DEFAULT_ROLE_URI_REF
from anzo_api.tests.test_utils.test_common import *


class TestAclApi(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.anzo = AclApi(DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)
        cls.config_anzo = AnzoApi(DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)
        cls.graphmart = cls.config_anzo.create_graphmart(title="Unittest Acls")
        cls.dataset = cls.config_anzo.create_empty_flds(
            title="My Empty API Dataset", data_format="ttl",
            data_location={
                "fileConnection": FILE_STORE_URI,
                "filePath": "setup-class"})

    @classmethod
    def tearDownClass(cls):
        cls.config_anzo.delete_graphmart(cls.graphmart.uri)
        cls.config_anzo.delete_dataset(cls.dataset.uri)

    def test_retrieve_acls_from_graphmart_is_acls(self):
        result = self.anzo.retrieve_acls(object_uri=self.graphmart.uri)
        self.assertIsInstance(result, AclDetailsView)

    def test_retrieve_acls_from_dataset_is_acls(self):
        result = self.anzo.retrieve_acls(object_uri=self.dataset.uri)
        self.assertIsInstance(result, AclDetailsView)

    def test_replace_acls(self):
        result = self.anzo.replace_acls([{
            "subject": self.graphmart.uri,
            "explicitShortFormAcls": [{
                "role": DEFAULT_ROLE_URI_REF["Data Citizen"],
                "access": "VIEW"
            }, {
                "role": DEFAULT_ROLE_URI_REF["Data Scientist"],
                "access": "MODIFY"
            }]
        }, {
            "subject": self.dataset.uri,
            "explicitShortFormAcls": [{
                "role": DEFAULT_ROLE_URI_REF["Data Citizen"],
                "access": "VIEW"
            }, {
                "role": DEFAULT_ROLE_URI_REF["Data Scientist"],
                "access": "MODIFY"
            }]
        }])
        self.assertTrue(result)

    def test_modify_acls(self):
        result = self.anzo.modify_acls(acl_edits=[{
            "subject": self.graphmart.uri,
            "inheritedAclsToAdd": [self.dataset.uri]
        }])
        self.assertTrue(result)

    def test_modify_acls_with_user(self):
        result = self.anzo.modify_acls(acl_edits=[{
            "subject": self.graphmart.uri,
            "explicitShortFormAclsToAdd": [{
                "role": TEST_USER_URI,
                "access": "VIEW"
            }]
        }])
        self.assertTrue(result)

    def test_modify_acls_with_group(self):
        result = self.anzo.modify_acls(acl_edits=[{
            "subject": self.graphmart.uri,
            "explicitShortFormAclsToAdd": [{
                "role": TEST_GROUP_URI,
                "access": "MODIFY"
            }]
        }])
        self.assertTrue(result)

    def test_reset_acls(self):
        result = self.anzo.reset_acls(object_uri=self.graphmart.uri)
        self.assertTrue(result)
