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
import base64
from unittest import TestCase

from ONAPLibrary.Base64Keywords import Base64Keywords


class Base64KeywordsTests(TestCase):

    def test_base64_encode(self):
        enc = Base64Keywords().base64_encode("string_to_encode")
        enc_base = base64.b64encode("string_to_encode".encode("utf-8"))
        self.assertEqual(enc_base, enc)

    def test_base64_decode(self):
        enc = Base64Keywords().base64_decode('c3RyaW5nX3RvX2RlY29kZQ==')
        self.assertEqual("string_to_decode", enc.decode("utf-8"))
