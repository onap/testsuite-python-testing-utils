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


class BaseSDCKeywords(object):
    """The main interface for interacting with SDC. It handles low level stuff like managing the http request library
    and required fields. """

    def __init__(self):
        super(BaseSDCKeywords, self).__init__()
        self.reqs = RequestsHelper()
        self.builtin = BuiltIn()

    @keyword
    def run_get_request(self, endpoint, data_path, user, accept="application/json", auth=None):
        """Runs an SDC get request"""
        return self.reqs.get_request("sdc", endpoint, data_path, sdc_user=user, accept=accept, auth=auth)

    @keyword
    def run_post_request(self, endpoint, data_path, data, user, accept="application/json", auth=None):
        """Runs an SDC post request"""
        return self.reqs.post_request("sdc", endpoint, data_path, data, user, files=None, accept=accept, auth=auth)

    @keyword
    def run_post_files_request(self, endpoint, data_path, files, user, accept="application/json", auth=None):
        """Runs an SDC post files request"""
        return self.reqs.post_request("sdc", endpoint, data_path, None, user, files=files, accept=accept,
                                      content_type="multipart/form-data", auth=auth)

    @keyword
    def run_put_request(self, endpoint, data_path, data, user, accept="application/json", auth=None):
        """Runs an SDC post request"""
        return self.reqs.put_request("sdc", endpoint, data_path, data, sdc_user=user, accept=accept, auth=auth)

    @keyword
    def run_delete_request(self, endpoint, data_path, data, user, accept="application/json", auth=None):
        """Runs an SDC delete request"""
        return self.reqs.delete_request("sdc", endpoint, data_path, data, sdc_user=user, accept=accept, auth=auth)
