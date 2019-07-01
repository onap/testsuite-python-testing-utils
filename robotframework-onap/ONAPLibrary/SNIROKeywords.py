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
from ONAPLibrary.TemplatingKeywords import TemplatingKeywords
from ONAPLibrary.Base64Keywords import Base64Keywords


class SNIROKeywords(object):
    """OOF is an ONAP testing library for Robot Framework that provides functionality for interacting with the
    optimiztion framework. """

    def __init__(self):
        super(SNIROKeywords, self).__init__()
        self.application_id = "robot-ete"
        self.uuid = Utilities()
        self.templating = TemplatingKeywords()
        self.base64 = Base64Keywords()
        self.builtin = BuiltIn()

    @keyword
    def run_sniro_get_request(self, endpoint, data_path, accept="application/json", auth=None):
        """Runs OOF-SNIRO Get request"""
        resp = self.get_request(endpoint, data_path, accept, auth)
        self.builtin.should_be_equal_as_strings(resp.status_code, "200")
        return resp

    @keyword
    def reset_sniro(self, endpoint):
        logger.debug('Clearing SNIRO data')
        resp = self.post_request(endpoint, '/reset', None)
        self.builtin.should_be_equal_as_strings(resp.status_code, "200", 'Clearing SNIRO date failed.')

    @keyword
    def preload_sniro(self, endpoint, template_directory, template_sniro_data, template_sniro_request,
                      tunnelxconn_ar_name, vgw_name, vbrg_ar_name, vgmux_svc_instance_uuid, vbrg_svc_instance_uuid):
        self.templating.create_environment("sniro", template_directory)
        logger.info('Preloading SNIRO for homing service')
        replace_dict = {'tunnelxconn_ar_name': tunnelxconn_ar_name,
                        'vgw_name': vgw_name,
                        'brg_ar_name': vbrg_ar_name,
                        'vgmux_svc_instance_uuid': vgmux_svc_instance_uuid,
                        'vbrg_svc_instance_uuid': vbrg_svc_instance_uuid
                        }
        sniro_data = self.templating.apply_template("sniro", template_sniro_data, replace_dict)
        base64_sniro_data = self.base64.base64_encode(sniro_data)
        replace_dict = {'base64_sniro_data': base64_sniro_data}
        sniro_request = self.templating.apply_template("sniro", template_sniro_request, replace_dict)
        resp = self.post_request(endpoint, '/', sniro_request)
        self.builtin.should_be_equal_as_strings(resp.status_code, "200", 'SNIRO preloading failed.')
        return True

    def post_request(self, endpoint, data_path, data, accept="application/json", auth=None):
        """Runs an SNIRO post request"""
        logger.info("Creating session" + endpoint)
        RequestsLibrary().create_session("so", endpoint, auth=auth)
        resp = RequestsLibrary().post_request("so", data_path, data=data, headers=self.create_headers(accept))
        logger.info("Received response from so " + resp.text)
        return resp

    def get_request(self, endpoint, data_path, accept="application/json", auth=None):
        """Runs an SNIRO get request"""
        logger.info("Creating session" + endpoint)
        RequestsLibrary().create_session("sniro", endpoint, auth=auth)
        resp = RequestsLibrary().get_request("sniro", data_path, headers=self.create_headers(accept))
        logger.info("Received response from OOF-SNIRO " + resp.text)
        return resp

    def create_headers(self, accept="application/json"):
        """Create the headers that are used by so"""
        uuid = self.uuid.generate_uuid4()
        headers = {
            "Accept": accept,
            "Content-Type": "application/json",
            "X-TransactionId": self.application_id + "-" + uuid,
            "X-FromAppId": self.application_id
        }
        return headers
