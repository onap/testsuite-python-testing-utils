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

import requests_mock
from unittest import TestCase
from unittest import main

from ONAPLibrary.SO import SO


class SOTests(TestCase):

    def test_get(self):
        with requests_mock.mock() as m:
            so = SO()
            m.get('http://test.com/', text='data')
            resp = so.run_get_request(endpoint="http://test.com", data_path="/",
                                      accept="application/json", auth={"user", "pass"})
        self.assertEqual("data", resp.text)

    if __name__ == '__main__':
        main()
