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
import os

from unittest import TestCase

from ONAPLibrary.ProtobufKeywords import ProtobufKeywords


class ProtobufKeywordsTest(TestCase):

    @staticmethod
    def _get_location():
        path = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        return path

    def test(self):
        with open(os.path.join(self._get_location(), "hvves_msg.raw"), "rb") as fileToDo:
            value = fileToDo.read()
        pb = ProtobufKeywords()
        result = pb.compare_file_to_message(os.path.join(self._get_location(), "hvves_msg.raw"), value)
        self.assertTrue(result)

    def test_compare_two(self):
        with open(os.path.join(self._get_location(), "hvves_msg.raw"), "rb") as fileToDo:
            value = fileToDo.read()
        pb = ProtobufKeywords()
        result = pb.compare_two_messages(value, value)
        self.assertTrue(result)

    def test_compare_two_many(self):
        with open(os.path.join(self._get_location(), "hvves_msg.raw"), "rb") as fileToDo:
            value = fileToDo.read()
        pb = ProtobufKeywords()
        result = pb.compare_two_messages(value, value)
        self.assertTrue(result)
        result = pb.compare_two_messages(value, value)
        self.assertTrue(result)
