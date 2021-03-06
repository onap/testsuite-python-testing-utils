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
from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn


class RequestSOKeywords(object):
    """SO is an ONAP testing library for Robot Framework that provides functionality for interacting with the serivce
    orchestrator. """

    def __init__(self):
        super(RequestSOKeywords, self).__init__()
        self.builtin = BuiltIn()
        self.reqs = RequestsHelper()

    @keyword
    def run_polling_get_request(self, endpoint, data_path, complete_states=None, fail_states=None, tries=20,
                                interval=15, auth=None):
        """Runs an SO get request until a certain state is received."""
        if fail_states is None:
            fail_states = ["FAILED"]
        if complete_states is None:
            complete_states = ["COMPLETE"]
        # do this until it is done
        for i in range(tries):
            resp = self.reqs.get_request(alias="so", endpoint=endpoint, data_path=data_path, auth=auth)
            logger.info(resp.json()['request']['requestStatus']['requestState'])
            if resp.json()['request']['requestStatus']['requestState'] in fail_states:
                self.builtin.fail("Received failure response from so " + resp.text)
            if resp.json()['request']['requestStatus']['requestState'] in complete_states:
                logger.info("Received complete response from so " + resp.text)
                return True, resp
            else:
                self.builtin.sleep(interval, "Response from SO is not in requested status")
        return False, None

    @keyword
    def run_create_request(self, endpoint, data_path, data, auth=None):
        """Runs an SO create request and returns the request id and instance id."""
        response = self.reqs.post_request(alias="so", endpoint=endpoint, data_path=data_path, data=data, auth=auth)
        logger.info("Creation request submitted to SO, got response")

        req_id = response.get('requestReferences', {}).get('requestId', '')
        instance_id = response.get('requestReferences', {}).get('instanceId', '')

        return req_id, instance_id
