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


class PreloadSDNCKeywords(object):
    """SDNC is an ONAP testing library for Robot Framework that provides functionality for interacting with the network
    controller. """

    def __init__(self):
        super(PreloadSDNCKeywords, self).__init__()
        self.reqs = RequestsHelper()
        self.templating = TemplatingKeywords()

    @keyword
    def preload_vfmodule(self, endpoint, data_path, templates_folder, template, preload_dictionary):
        """Runs an SDNC request to preload certain data."""
        self.templating.create_environment("sdnc", templates_folder)
        data = self.templating.apply_template("sdnc", template, preload_dictionary)
        return self.reqs.post_request(alias="sdnc", endpoint=endpoint, data_path=data_path, data=data)
