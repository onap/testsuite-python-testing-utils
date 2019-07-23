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

from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import time

from ONAPLibrary.RequestsHelper import RequestsHelper
from ONAPLibrary.HTTPKeywords import HTTPKeywords


class BaseAAIKeywords(object):
    """The main interface for interacting with AAI. It handles low level stuff like managing the http request library
    and required fields. """

    def __init__(self):
        super(BaseAAIKeywords, self).__init__()
        self.reqs = RequestsHelper()
        self.builtin = BuiltIn()
        self.http = HTTPKeywords()

    @keyword
    def run_get_request(self, endpoint, data_path, accept="application/json", auth=None):
        """Runs an AAI get request"""
        self.http.disable_warnings()
        resp = self.reqs.get_request("aai", endpoint, data_path, sdc_user=None, accept=accept, auth=auth)
        self.builtin.should_be_equal_as_strings(resp.status_code, "200")
        return resp

    @keyword
    def run_post_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an AAI post request"""
        self.http.disable_warnings()
        return self.reqs.post_request("aai", endpoint, data_path, data, sdc_user=None, files=None,
                                      accept=accept, auth=auth)

    @keyword
    def run_put_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an AAI post request"""
        self.http.disable_warnings()
        return self.reqs.put_request("aai", endpoint, data_path, data, sdc_user=None, accept=accept, auth=auth)

    @keyword
    def run_delete_request(self, endpoint, data_path, resource_version, accept="application/json", auth=None):
        """Runs an AAI delete request"""
        self.http.disable_warnings()
        return self.reqs.delete_request("aai", endpoint, data_path + '?resource-version=' + resource_version, data=None,
                                        sdc_user=None, accept=accept, auth=auth)

    @keyword
    def wait_for_node_to_exist(self, endpoint, search_node_type, key, uuid, auth=None):
        logger.info('Waiting for AAI traversal to complete...')
        for i in range(30):
            time.sleep(1)
            result = self.find_node(endpoint, search_node_type, key, uuid, auth=auth)
            if result:
                return result

        error_message = "AAI traversal didn't finish in 30 seconds. Something is wrong. Type {0}, UUID {1}".format(
            search_node_type, uuid)
        logger.error(error_message)
        self.builtin.fail(error_message)

    @keyword
    def find_node(self, endpoint, search_node_type, key, node_uuid, auth=None):
        data_path = '/aai/v11/search/nodes-query?search-node-type={0}&filter={1}:EQUALS:{2}'.format(
            search_node_type, key, node_uuid)
        self.http.disable_warnings()
        resp = self.reqs.get_request("aai", endpoint, data_path, accept="application/json", auth=auth)
        response = resp.json()
        return 'result-data' in response