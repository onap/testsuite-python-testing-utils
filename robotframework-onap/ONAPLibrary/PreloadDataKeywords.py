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

from robot import utils
from robot.api.deco import keyword
import os.path
import json


class PreloadDataKeywords(object):
    """PreloadData is used for loading data for services into the robot framework in a structured decentralized way
    that lets vnfs be added without code change to testuite"""

    def __init__(self):
        super(PreloadDataKeywords, self).__init__()
        self._cache = utils.ConnectionCache('No Preload Data directories loaded')

    @keyword
    def set_directory(self, alias, preload_data_directory):
        self._cache.register(preload_data_directory, alias=alias)

    @keyword
    def get_preload_data(self, alias, service, template):
        """returns a dictionary with all of the preload data for the passed in service and template"""
        return self._preload_data(alias, service)[template]

    @keyword
    def get_default_preload_data(self, alias):
        """returns a dictionary with all of the default values"""
        return self._preload_data(alias, "defaults")

    def _preload_data(self, alias, service):
        filepath = os.path.join(self._cache.switch(alias), service, 'preload_data.json')
        with open(filepath, 'r') as f:
            return json.load(f)
