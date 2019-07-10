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
from RequestsLibrary import RequestsLibrary
from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

import hashlib

from ONAPLibrary.Base64Keywords import Base64Keywords
from ONAPLibrary.UUIDKeywords import UUIDKeywords


class BaseSDCKeywords(object):
    """The main interface for interacting with SDC. It handles low level stuff like managing the http request library
    and required fields. """

    def __init__(self):
        super(BaseSDCKeywords, self).__init__()
        self.application_id = "robot-ete"
        self.uuid = UUIDKeywords()
        self.builtin = BuiltIn()

    @keyword
    def run_get_request(self, endpoint, data_path, user, accept="application/json", auth=None):
        """Runs an SDC get request"""
        resp = self.get_request(endpoint, data_path, user, accept, auth)
        self.builtin.should_be_equal_as_strings(resp.status_code, "200")
        return resp

    @keyword
    def run_post_request(self, endpoint, data_path, data, user, accept="application/json", auth=None):
        """Runs an SDC post request"""
        return self.post_request(endpoint, data_path, data, user, files=None, accept=accept, auth=auth)

    @keyword
    def run_post_files_request(self, endpoint, data_path, files, user, accept="application/json", auth=None):
        """Runs an SDC post files request"""
        return self.post_request(endpoint, data_path, files, user, files=None, accept=accept,
                                 content_type="multipart/form-data", auth=auth)

    @keyword
    def run_put_request(self, endpoint, data_path, data, user, accept="application/json", auth=None):
        """Runs an SDC post request"""
        return self.put_request(endpoint, data_path, data, user, accept, auth)

    def get_request(self, endpoint, data_path, user, accept="application/json", auth=None):
        """Runs an SDC get request"""
        logger.info("Creating session" + endpoint)
        RequestsLibrary().create_session("sdc", endpoint, auth=auth)
        resp = RequestsLibrary().get_request("sdc", data_path, headers=self.create_headers(user, accept))
        logger.info("Received response from sdc " + resp.text)
        return resp

    def create_headers(self, user=None, accept="application/json", content_type="application/json", md5=None):
        """Create the headers that are used by sdc"""
        uuid = self.uuid.generate_uuid4()
        headers = {
            "Accept": accept,
            "Content-Type": content_type,
            "X-TransactionId": self.application_id + "-" + uuid,
            "X-FromAppId": self.application_id
        }
        if not user:
            headers["USER_ID"] = user
        if not md5:
            headers["Content-MD5"] = md5
        return headers

    def post_request(self, endpoint, data_path, data, user, files=None, accept="application/json",
                     content_type="application/json", auth=None):
        """Runs an SDC post request"""
        logger.info("Creating session" + endpoint)
        md5 = hashlib.md5()
        md5checksum = Base64Keywords().base64_encode(md5.update(data).hexdigest())
        RequestsLibrary().create_session("sdc", endpoint, auth=auth)
        headers = self.create_headers(user, accept=accept, content_type=content_type, md5=md5checksum)
        resp = RequestsLibrary().post_request("sdc", data_path, files=files, data=data, headers=headers)

        logger.info("Received response from sdc " + resp.text)
        return resp

    def put_request(self, endpoint, data_path, data, user, accept="application/json", auth=None):
        """Runs an SDC post request"""
        logger.info("Creating session" + endpoint)
        RequestsLibrary().create_session("sdc", endpoint, auth=auth)
        resp = RequestsLibrary().put_request("sdc", data_path, data=data, headers=self.create_headers(user, accept))
        logger.info("Received response from sdc " + resp.text)
        return resp

    def delete_request(self, endpoint, data_path, data, user, accept="application/json", auth=None):
        """Runs an SDC post request"""
        logger.info("Creating session" + endpoint)
        RequestsLibrary().create_session("sdc", endpoint, auth=auth)
        resp = RequestsLibrary().delete_request("sdc", data_path, data=data, headers=self.create_headers(user, accept))
        logger.info("Received response from sdc " + resp.text)
        return resp
