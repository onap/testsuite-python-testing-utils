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
from six import string_types
from robot.api.deco import keyword
from jsonpath_rw import parse


class JSONPathKeywords(object):
    """JSONPATH is common resource for json path keywords.
    """

    def __init__(self):
        super(JSONPathKeywords, self).__init__()

    @keyword
    def json_search(self, expression, target):
        """JSON Search takes in two params, the first is the jsonpath expression and the second is the json target
        which is converted into string if needed and then compares them, returning the matches."""

        jsonpath_expr = parse(expression)
        if isinstance(target, string_types):
            search_json = json.dumps(target)
        else:
            search_json = target

        results = jsonpath_expr.find(search_json)
        return results
