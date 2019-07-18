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

from unittest import TestCase

from ONAPLibrary.UUIDKeywords import UUIDKeywords


class UUIDKeywordsTest(TestCase):

    def test_uuid4(self):
        uuid = UUIDKeywords()
        self.assertGreater(len(uuid.generate_uuid4()), 0)

    def test_uuid1(self):
        uuid = UUIDKeywords()
        self.assertGreater(len(uuid.generate_uuid1()), 0)

    def test_timestamp(self):
        uuid = UUIDKeywords()
        self.assertGreater(uuid.generate_timestamp(), 0)
