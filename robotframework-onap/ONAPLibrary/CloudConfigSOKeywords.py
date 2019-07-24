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

from ONAPLibrary.RequestsHelper import RequestsHelper
from ONAPLibrary.TemplatingKeywords import TemplatingKeywords
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn


class CloudConfigSOKeywords(object):
    """SO is an ONAP testing library for Robot Framework that provides functionality for interacting with the serivce
    orchestrator. """

    def __init__(self):
        super(CloudConfigSOKeywords, self).__init__()
        self.builtin = BuiltIn()
        self.reqs = RequestsHelper()
        self.templating = TemplatingKeywords()

    @keyword
    def get_cloud_configuration(self, endpoint, data_path, site_name, auth=None):
        """Gets cloud configuration in SO"""
        return self.reqs.get_request("so", endpoint, data_path + "/" + site_name, auth=auth)

    @keyword
    def create_cloud_configuration(self, endpoint, data_path, templates_folder, template, arguments, auth=None):
        """Creates a cloud configuration in SO, so it knows how to talk to an openstack cloud"""
        self.templating.create_environment("so", templates_folder)
        data = self.templating.apply_template("so", template, arguments)
        resp = self.reqs.post_request("so", endpoint, data_path, data, auth=auth)
        self.builtin.should_match_regexp(str(resp.status_code), "^(201|200)$")

    @keyword
    def upsert_cloud_configuration(self, endpoint, data_path, templates_folder, template, arguments, auth=None):
        """Creates a cloud configuration in SO, or if it exists updates it"""
        get_resp = self.get_cloud_configuration(endpoint, data_path, arguments['site_name'])
        self.templating.create_environment("so", templates_folder)
        data = self.templating.apply_template("so", template, arguments)
        if get_resp.status_code == 404:
            resp = self.reqs.post_request("so", endpoint, data_path, data, auth=auth)
        else:
            resp = self.reqs.put_request("so", endpoint, data_path, data, auth=auth)
        self.builtin.should_match_regexp(str(resp.status_code), "^(201|200)$")
