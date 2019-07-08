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

from ONAPLibrary.Utilities import Utilities


class BaseSDNCKeywords(object):
    """SDNC is an ONAP testing library for Robot Framework that provides functionality for interacting with the network
    controller. """

    def __init__(self):
        super(BaseSDNCKeywords, self).__init__()
        self.application_id = "robot-ete"
        self.uuid = Utilities()
        self.builtin = BuiltIn()

    @keyword
    def run_get_request(self, endpoint, data_path, accept="application/json", auth=None):
        """Runs an SDNC get request"""
        resp = self.get_request(endpoint, data_path, accept, auth)
        self.builtin.should_be_equal_as_strings(resp.status_code, "200")
        return resp

    @keyword
    def run_post_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an SDNC post request"""
        return self.post_request(endpoint, data_path, data, accept, auth)

    @keyword
    def run_put_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an SDNC post request"""
        return self.put_request(endpoint, data_path, data, accept, auth)

    def get_request(self, endpoint, data_path, accept="application/json", auth=None):
        """Runs an SDNC get request"""
        logger.info("Creating session" + endpoint)
        RequestsLibrary().create_session("sdnc", endpoint, auth=auth)
        resp = RequestsLibrary().get_request("sdnc", data_path, headers=self.create_headers(accept))
        logger.info("Received response from sdnc " + resp.text)
        return resp

    def create_headers(self, accept="application/json"):
        """Create the headers that are used by sdnc"""
        uuid = self.uuid.generate_uuid4()
        headers = {
            "Accept": accept,
            "Content-Type": "application/json",
            "X-TransactionId": self.application_id + "-" + uuid,
            "X-FromAppId": self.application_id
        }
        return headers

    def post_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an sdnc post request"""
        logger.info("Creating session" + endpoint)
        RequestsLibrary().create_session("sdnc", endpoint, auth=auth)
        resp = RequestsLibrary().post_request("sdnc", data_path, data=data, headers=self.create_headers(accept))
        logger.info("Received response from sdnc " + resp.text)
        return resp

    def put_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an sdnc post request"""
        logger.info("Creating session" + endpoint)
        RequestsLibrary().create_session("sdnc", endpoint, auth=auth)
        resp = RequestsLibrary().put_request("sdnc", data_path, data=data, headers=self.create_headers(accept))
        logger.info("Received response from sdnc " + resp.text)
        return resp

    def delete_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an sdnc post request"""
        logger.info("Creating session" + endpoint)
        RequestsLibrary().create_session("sdnc", endpoint, auth=auth)
        resp = RequestsLibrary().delete_request("sdnc", data_path, data=data, headers=self.create_headers(accept))
        logger.info("Received response from sdnc " + resp.text)
        return resp
