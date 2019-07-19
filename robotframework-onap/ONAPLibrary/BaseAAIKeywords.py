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

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn


from ONAPLibrary.RequestsHelper import RequestsHelper


class BaseAAIKeywords(object):
    """The main interface for interacting with AAI. It handles low level stuff like managing the http request library
    and required fields. """

    def __init__(self):
        super(BaseAAIKeywords, self).__init__()
        self.reqs = RequestsHelper()
        self.builtin = BuiltIn()

    @keyword
    def run_get_request(self, endpoint, data_path, accept="application/json", auth=None):
        """Runs an AAI get request"""
        resp = self.reqs.get_request("aai", endpoint, data_path, sdc_user=None, accept=accept, auth=auth)
        self.builtin.should_be_equal_as_strings(resp.status_code, "200")
        return resp

    @keyword
    def run_post_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an AAI post request"""
        return self.reqs.post_request("aai", endpoint, data_path, data, sdc_user=None, files=None,
                                      accept=accept, auth=auth)

    @keyword
    def run_put_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an AAI post request"""
        return self.reqs.put_request("aai", endpoint, data_path, data, sdc_user=None, accept=accept, auth=auth)

    @keyword
    def run_delete_request(self, endpoint, data_path, resource_version, accept="application/json", auth=None):
        """Runs an AAI delete request"""
        return self.reqs.delete_request("aai", endpoint, data_path + '?resource-version=' + resource_version, data=None,
                                        sdc_user=None, accept=accept, auth=auth)
