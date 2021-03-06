# Copyright 2019 AT&T Intellectual Property. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests_mock
from unittest import TestCase
from ONAPLibrary.RequestsHelper import RequestsHelper


class RequestsHelperTests(TestCase):

    def test_get(self):
        with requests_mock.mock() as m:
            rh = RequestsHelper()
            m.get('http://test.com/', text='data')
            resp = rh.get_request(alias="alias", endpoint="http://test.com", data_path="/", sdc_user="test123",
                                  accept="application/json", auth={"user", "pass"})
        self.assertEqual("data", resp.text)

    def test_put(self):
        with requests_mock.mock() as m:
            rh = RequestsHelper()
            m.put('http://test.com/', text='data')
            resp = rh.put_request(alias="alias", endpoint="http://test.com", data="data", client_certs={"ca", "pem"})
        self.assertEqual("data", resp.text)

    def test_delete(self):
        with requests_mock.mock() as m:
            rh = RequestsHelper()
            m.delete('http://test.com/', text='data')
            resp = rh.delete_request(alias="alias", endpoint="http://test.com", data="data", client_certs={"ca", "pem"})
        self.assertEqual("data", resp.text)

    def test_post(self):
        with requests_mock.mock() as m:
            rh = RequestsHelper()
            m.post('http://test.com/', text='data')
            resp = rh.post_request(alias="alias", endpoint="http://test.com", data_path="/", sdc_user="test123",
                                   accept="application/json", content_type="application/json", files={'file':"test/123"})
        self.assertEqual("data", resp.text)

    def test_md5_string(self):
        with requests_mock.mock() as m:
            rh = RequestsHelper()
            m.post('http://test.com/', text='data', additional_matcher=self._match_md5_request_header)
            resp = rh.post_request(alias="alias", endpoint="http://test.com", data_path="/", sdc_user="test123",
                                   accept="application/json", content_type="text/string", data="test/123")
            self.assertEqual("data", resp.text)

    def test_md5_bytes(self):
        with requests_mock.mock() as m:
            rh = RequestsHelper()
            m.post('http://test.com/', text='data', additional_matcher=self._match_md5_request_header)
            resp = rh.post_request(alias="alias", endpoint="http://test.com", data_path="/", sdc_user="test123",
                                   accept="application/json", content_type="text/string", data=b"test/123")
            self.assertEqual("data", resp.text)

    @staticmethod
    def _match_md5_request_header(request):
        return (request.headers.get('Content-MD5', None)) is not None
