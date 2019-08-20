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
from ONAPLibrary.VariableKeywords import VariableKeywords


class BaseAAIKeywords(object):
    """The main interface for interacting with AAI. It handles low level stuff like managing the http request library
    and required fields. """

    def __init__(self):
        super(BaseAAIKeywords, self).__init__()
        self.reqs = RequestsHelper()
        self.builtin = BuiltIn()
        self.vars = VariableKeywords()
        aai_ip_addr = self.vars.get_globally_injected_parameters().get('GLOBAL_INJECTED_AAI_IP_ADDR', '')
        aai_server_protocol = self.vars.get_global_parameters().get('GLOBAL_AAI_SERVER_PROTOCOL', '')
        aai_server_port = self.vars.get_global_parameters().get('GLOBAL_AAI_SERVER_PORT', '')
        self.aai_endpoint = str(aai_server_protocol) + '://' + str(aai_ip_addr) + ':' + str(aai_server_port)

    @keyword
    def run_get_request(self, endpoint, data_path, accept="application/json", auth=None, client_certs=None):
        """Runs an AAI get request"""
        return self.reqs.get_request(alias="aai", endpoint=endpoint, data_path=data_path, accept=accept, auth=auth,
                                     client_certs=client_certs)

    @keyword
    def run_post_request(self, endpoint, data_path, data, accept="application/json", auth=None, client_certs=None):
        """Runs an AAI post request"""
        return self.reqs.post_request(alias="aai", endpoint=endpoint, data_path=data_path, data=data, accept=accept,
                                      auth=auth, client_certs=client_certs)

    @keyword
    def run_put_request(self, endpoint, data_path, data, accept="application/json", auth=None, client_certs=None):
        """Runs an AAI post request"""
        return self.reqs.put_request(alias="aai", endpoint=endpoint, data_path=data_path, data=data, accept=accept,
                                     auth=auth, client_certs=client_certs)

    @keyword
    def run_delete_request(self, endpoint, data_path, resource_version, accept="application/json", auth=None,
                           client_certs=None):
        """Runs an AAI delete request"""
        return self.reqs.delete_request(alias="aai", endpoint=endpoint, accept=accept, auth=auth,
                                        client_certs=client_certs,
                                        data_path=data_path + '?resource-version=' + resource_version)

    @keyword
    def wait_for_node_to_exist(self, search_node_type, key, uuid, auth=None, client_certs=None):
        logger.info('Waiting for AAI traversal to complete...')
        for i in range(30):
            logger.trace("running iteration " + str(i))
            time.sleep(1)
            result = self.find_node(search_node_type, key, uuid, auth=auth, client_certs=client_certs)
            if result:
                return result

        error_message = "AAI traversal didn't finish in 30 seconds. Something is wrong. Type {0}, UUID {1}".format(
            search_node_type, uuid)
        logger.error(error_message)
        self.builtin.fail(error_message)

    @keyword
    def find_node(self, search_node_type, key, node_uuid, auth=None, client_certs=None):
        data_path = '/aai/v11/search/nodes-query?search-node-type={0}&filter={1}:EQUALS:{2}'.format(
            search_node_type, key, node_uuid)
        resp = self.reqs.get_request("aai", self.aai_endpoint, data_path, accept="application/json", auth=auth,
                                     client_certs=client_certs)
        response = resp.json()
        return 'result-data' in response
