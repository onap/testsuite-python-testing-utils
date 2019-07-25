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

from ONAPLibrary.VESProtobuf import VESProtobuf
from ONAPLibrary.JSONKeywords import JSONKeywords
from robot.api.deco import keyword


class ProtobufKeywords(object):
    """ Utilities useful for Protobuf manipulation """

    def __init__(self):
        super(ProtobufKeywords, self).__init__()
        self.vpf = VESProtobuf()

    @keyword
    def compare_file_to_message(self, file_name, message):
        with open(file_name, "rb") as file_to_do:
            return self.compare_two_messages(file_to_do.read(), message)

    def compare_two_messages(self, left, right):
        left_json = self.vpf.binary_to_json(left)
        right_json = self.vpf.binary_to_json(right)
        return JSONKeywords().json_equals(left_json, right_json)
