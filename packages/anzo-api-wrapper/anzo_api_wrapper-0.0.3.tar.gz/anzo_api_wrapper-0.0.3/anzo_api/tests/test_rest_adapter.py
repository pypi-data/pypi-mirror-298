from unittest import TestCase, mock
import requests

from anzo_api.rest_adapter import RestAdapter
from anzo_api.exceptions import AnzoRestApiException
from anzo_api.models import *

class TestRestAdapter(TestCase):

    def setUp(self):
        self.rest_adapter = RestAdapter()
        self.response = requests.Response()

    def test__do_good_request_returns_result(self):
        self.response.status_code = 200
        self.response._content = "{}".encode()
        with mock.patch("requests.request", return_value=self.response):
            result = self.rest_adapter._do('GET', '')
            self.assertIsInstance(result, Result)

    def test__do_bad_json_raises_anzoapi_exception(self): # TODO realistic fail implementation
        bad_json = '{"some bad json": '
        self.response._content = bad_json
        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(AnzoRestApiException):
                self.rest_adapter._do("GET", "")

    def test__do(self):
        self.fail()

    def test_get(self):
        self.fail()

    def test_post(self):
        self.fail()

    def test_put(self):
        self.fail()

    def test_delete(self):
        self.fail()
