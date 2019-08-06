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

from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.api.deco import keyword
import os


class VariableKeywords(object):
    """ keyword class for useful keywords for working with varaibles """

    def __init__(self):
        super(VariableKeywords, self).__init__()
        self.builtin = BuiltIn()

    @keyword
    def get_globally_injected_parameters(self):
        return self._filter_variables_by_key_prefix(self._retrieve_robot_variables(), "GLOBAL_INJECTED_")

    @keyword
    def get_global_parameters(self):
        global_variables = self._filter_variables_by_key_prefix(self._retrieve_robot_variables(), "GLOBAL_")
        # strip out global injected (get those above)
        for key in self.get_globally_injected_parameters():
            del global_variables[key]
        return global_variables

    def _retrieve_robot_variables(self):
        """ try to get the parameters from the robot keyword, but if it is ran out of robot context,
        allow an env to be used instead """
        dictionary = dict()
        try:
            dictionary = self.builtin.get_variables(no_decoration=True)
        except RobotNotRunningError:
            try:
                dictionary = os.environ['GLOBAL_ROBOT_VARIABLES']
            except KeyError:
                pass
        return dictionary

    @staticmethod
    def _filter_variables_by_key_prefix(dictionary, partial):
        matches = dict()
        for key, val in dictionary.items():
            if key.startswith(partial):
                matches[key] = val
        return matches
