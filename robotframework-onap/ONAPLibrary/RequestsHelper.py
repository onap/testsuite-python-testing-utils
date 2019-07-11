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

from ONAPLibrary.UUIDKeywords import UUIDKeywords


class RequestsHelper(object):
    """ non keywords methods related to Requests library """

    def __init__(self):
        super(RequestsHelper, self).__init__()
        self.uuid = UUIDKeywords()
        self.application_id = "robot-ete"

    def create_headers(self, sdc_user_id=None, accept="application/json", content_type="application/json", md5=None):
        """Create the headers that are used by onap"""
        uuid = self.uuid.generate_uuid4()
        headers = {
            "Accept": accept,
            "Content-Type": content_type,
            "X-TransactionId": self.application_id + "-" + uuid,
            "X-FromAppId": self.application_id
        }
        if not sdc_user_id:
            headers["USER_ID"] = sdc_user_id
        if not md5:
            headers["Content-MD5"] = md5
        return headers
