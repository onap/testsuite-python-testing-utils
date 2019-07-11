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

from ONAPLibrary.RequestsHelper import RequestsHelper


class MUSICKeywords(object):
    """MUSIC is an ONAP testing library for Robot Framework that provides functionality for interacting with the serivce
    orchestrator. """

    def __init__(self):
        super(MUSICKeywords, self).__init__()
        self.reqs = RequestsHelper()
        self.builtin = BuiltIn()

    @keyword
    def run_get_request(self, endpoint, data_path, accept="application/json", auth=None):
        """Runs an MUSIC get request"""
        resp = self.get_request(endpoint, data_path, accept, auth)
        return resp

    def get_request(self, endpoint, data_path, accept="application/json", auth=None):
        """Runs an MUSIC get request"""
        logger.info("Creating session" + endpoint)
        RequestsLibrary().create_session("music", endpoint, auth=auth)
        resp = RequestsLibrary().get_request("music", data_path, headers=self.reqs.create_headers(accept=accept))
        logger.info("Received response from music " + resp.text)
        return resp

    def run_health_check(self, endpoint, health_check_path):
        """Runs MUSIC Health check"""
        resp = self.run_get_request(endpoint, health_check_path)
        self.builtin.should_be_equal_as_strings(resp.status_code, "200")
        self.builtin.should_be_equal_as_strings(resp.json()['status'], "SUCCESS")

    def run_cassandra_connection_check(self, endpoint, health_check_path):
        """Confirm MUSIC's connection to Cassandra in active"""
        resp = self.run_get_request(endpoint, health_check_path)
        self.builtin.should_be_equal_as_strings(resp.status_code, "200")
        self.builtin.should_be_equal_as_strings(resp.json()['Cassandra'], "Active")
