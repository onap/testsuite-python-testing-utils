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

from ONAPLibrary.UUIDKeywords import UUIDKeywords
from RequestsLibrary import RequestsLibrary
import hashlib
from ONAPLibrary.Base64Keywords import Base64Keywords
from ONAPLibrary.HTTPKeywords import HTTPKeywords
from ONAPLibrary.RequestsDecorators import log_wrapped
from ONAPLibrary.RequestsDecorators import default_keywords


class RequestsHelper(object):
    """ non keyword methods related to Requests library """

    def __init__(self):
        super(RequestsHelper, self).__init__()
        self.uuid = UUIDKeywords()
        self.application_id = "robot-ete"
        self.requests = RequestsLibrary()
        self.http = HTTPKeywords()

    @default_keywords
    @log_wrapped
    def get_request(self, **kwargs):
        """Runs a get request"""
        return self.requests.get_request(alias=kwargs['alias'],  uri=kwargs['data_path'],
                                         headers=self._perform_setup(**kwargs))

    @default_keywords
    @log_wrapped
    def post_request(self, **kwargs):
        """Runs a post request"""
        kwargs['md5'] = self._format_md5(kwargs['data'])
        return self.requests.post_request(alias=kwargs['alias'],  uri=kwargs['data_path'], files=kwargs['files'],
                                          data=kwargs['data'], headers=self._perform_setup(**kwargs))

    @default_keywords
    @log_wrapped
    def put_request(self, **kwargs):
        """Runs a put request"""
        return self.requests.put_request(alias=kwargs['alias'],  uri=kwargs['data_path'], data=kwargs['data'],
                                         headers=self._perform_setup(**kwargs))

    @default_keywords
    @log_wrapped
    def delete_request(self, **kwargs):
        """Runs a delete request"""
        return self.requests.delete_request(alias=kwargs['alias'],  uri=kwargs['data_path'], data=kwargs['data'],
                                            headers=self._perform_setup(**kwargs))

    def _perform_setup(self, **kwargs):
        self.http.disable_warnings()
        self._create_session(alias=kwargs['alias'], endpoint=kwargs['endpoint'], auth=kwargs['auth'],
                             client_certs=kwargs['client_certs'])
        return self._create_headers(sdc_user_id=kwargs['sdc_user'], accept=kwargs['accept'],
                                    content_type=kwargs['content_type'], md5=kwargs.get("md5", None))

    def _create_session(self, alias, endpoint, auth=None, client_certs=None):
        if client_certs is not None:
            self.requests.create_client_cert_session(alias, endpoint, client_certs=client_certs)
        else:
            self.requests.create_session(alias, endpoint, auth=auth)

    def _create_headers(self, sdc_user_id=None, accept="application/json", content_type="application/json", md5=None):
        """Create the headers that are used by onap"""
        uuid = self.uuid.generate_uuid4()
        headers = {
            "Accept": accept,
            "Content-Type": content_type,
            "X-TransactionId": self.application_id + "-" + uuid,
            "X-FromAppId": self.application_id
        }
        if sdc_user_id is not None:
            headers["USER_ID"] = sdc_user_id
        if md5 is not None:
            headers["Content-MD5"] = md5
        return headers

    @staticmethod
    def _format_md5(md5_input):
        if md5_input is not None and isinstance(md5_input, str):
            md5 = hashlib.md5()
            md5.update(md5_input.encode('utf-8'))
            return Base64Keywords().base64_encode(md5.hexdigest())
        else:
            return None
