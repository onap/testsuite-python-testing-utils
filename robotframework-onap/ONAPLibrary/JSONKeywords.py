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

import json
from robot.api.deco import keyword
from deepdiff import DeepDiff
from six import string_types


class JSONKeywords(object):
    """JSON is common resource for simple json helper keywords.
    """

    def __init__(self):
        super(JSONKeywords, self).__init__()

    @keyword
    def json_equals(self, left, right):
        """JSON Equals takes in two strings or json objects, converts them into json if needed and then compares them,
        returning if they are equal or not."""
        if isinstance(left, string_types):
            left_json = json.loads(left)
        else:
            left_json = left
        if isinstance(right, string_types):
            right_json = json.loads(right)
        else:
            right_json = right

        ddiff = DeepDiff(left_json, right_json, ignore_order=True)
        if ddiff == {}:
            return True
        else:
            return False

    @keyword
    def make_list_into_dict(self, dict_list, key):
        """ Converts a list of dicts that contains a field that has a unique key into a dict of dicts """
        d = {}
        if isinstance(dict_list, list):
            for thisDict in dict_list:
                v = thisDict[key]
                d[v] = thisDict
        return d

    @keyword
    def find_element_in_array(self, searched_array, key, value):
        """ Takes in an array and a key value, it will return the items in the array that has a key and value that
        matches what you pass in """
        elements = []
        for item in searched_array:
            if key in item:
                if item[key] == value:
                    elements.append(item)
        return elements
