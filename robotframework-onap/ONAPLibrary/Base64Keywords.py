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
import base64


class Base64Keywords(object):
    """ Utilities useful for generating UUIDs """

    def __init__(self):
        super(Base64Keywords, self).__init__()

    @keyword
    def base64_encode(self, string_to_encode):
        """generate a base64 encoded string"""
        return base64.b64encode(string_to_encode.encode("utf-8"))

    @keyword
    def base64_decode(self, string_to_decode):
        """decode a base64 encoded string"""
        return base64.b64decode(string_to_decode.encode("utf-8"))
