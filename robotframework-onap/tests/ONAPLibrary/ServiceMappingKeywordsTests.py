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
import os.path
from unittest import TestCase
from ONAPLibrary.ServiceMappingKeywords import ServiceMappingKeywords


class ServiceMappingKeywordsTests(TestCase):

    @staticmethod
    def _get_location():
        path = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        return path

    @keyword
    def test(self):
        sm = ServiceMappingKeywords()
        sm.set_directory("default", self._get_location())
        self.assertEqual(['vFW'], sm.get_service_folder_mapping("default", "vFW"))
