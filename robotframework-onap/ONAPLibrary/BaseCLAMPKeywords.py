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
from ONAPLibrary.RequestsHelper import RequestsHelper


class BaseCLAMPKeywords(object):
    """The main interface for interacting with CLAMP. It handles low level stuff like managing the http request library
    and required fields. """

    def __init__(self):
        super(BaseCLAMPKeywords, self).__init__()
        self.reqs = RequestsHelper()

    @keyword
    def run_get_request(self, endpoint, data_path, accept="application/json", auth=None):
        """Runs an CLAMP get request"""
        return self.reqs.get_request(alias="clamp", endpoint=endpoint, data_path=data_path, accept=accept, auth=auth)

    @keyword
    def run_post_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an CLAMP post request"""
        return self.reqs.post_request(alias="clamp", endpoint=endpoint, data_path=data_path, data=data, accept=accept,
                                      auth=auth)

    @keyword
    def run_put_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an CLAMP post request"""
        return self.reqs.put_request(alias="clamp", endpoint=endpoint, data_path=data_path, data=data, accept=accept,
                                     auth=auth)

    @keyword
    def run_delete_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an CLAMP delete request"""
        return self.reqs.delete_request(alias="clamp", endpoint=endpoint, data_path=data_path, data=data, accept=accept,
                                        auth=auth)
