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


class VariableKeywords(object):
    """ Utilities useful for working with varaibles """

    def __init__(self):
        super(VariableKeywords, self).__init__()
        self.builtin = BuiltIn()

    @keyword
    def get_globally_injected_parameters(self):
        dictionary = self.builtin.get_variables(no_decoration=True)
        return self.filter_variables_by_key_prefix(dictionary, "GLOBAL_INJECTED")

    @keyword
    def filter_variables_by_key_prefix(self, dictionary, partial):
        matches = dict()
        for key, val in dictionary.items():
            if key.startswith(partial):
                matches[key] = val
        return matches
