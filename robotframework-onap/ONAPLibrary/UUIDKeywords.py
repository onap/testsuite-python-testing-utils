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

import uuid
import time
import datetime
from robot.api.deco import keyword


class UUIDKeywords(object):
    """ Utilities useful for generating UUIDs """

    def __init__(self):
        super(UUIDKeywords, self).__init__()

    @keyword
    def generate_uuid4(self):
        """generate a uuid"""
        return str(uuid.uuid4())

    @keyword
    def generate_uuid1(self):
        """generate a timestamp uuid"""
        return str(uuid.uuid1())

    @keyword
    def generate_timestamp(self):
        """generate a timestamp"""
        then = datetime.datetime.now()
        return int(time.mktime(then.timetuple()) * 1e3 + then.microsecond / 1e3)
