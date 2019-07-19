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
from RequestsLibrary import RequestsLibrary
from robot.api import logger
import hashlib
from ONAPLibrary.Base64Keywords import Base64Keywords


class RequestsHelper(object):
    """ non keyword methods related to Requests library """

    def __init__(self):
        super(RequestsHelper, self).__init__()
        self.uuid = UUIDKeywords()
        self.application_id = "robot-ete"
        self.requests = RequestsLibrary()

    def create_headers(self, sdc_user_id=None, accept="application/json", content_type="application/json", md5=None):
        """Create the headers that are used by onap"""
        uuid = self.uuid.generate_uuid4()
        headers = {
            "Accept": accept,
            "Content-Type": content_type,
            "X-TransactionId": self.application_id + "-" + uuid,
            "X-FromAppId": self.application_id
        }
        if sdc_user_id is not None:
            headers["USER_ID"] = sdc_user_id
        if md5 is not None:
            headers["Content-MD5"] = md5
        return headers

    def get_request(self, alias, endpoint, data_path, sdc_user=None, accept="application/json", auth=None):
        """Runs a get request"""
        logger.info("Creating session" + endpoint)
        self.requests.create_session(alias, endpoint, auth=auth)
        headers = self.create_headers(sdc_user_id=sdc_user, accept=accept)
        resp = self.requests.get_request(alias, data_path, headers=headers)
        logger.info("Received response from [" + alias + "]: " + resp.text)
        return resp

    def post_request(self, alias, endpoint, data_path, data, sdc_user=None, files=None, accept="application/json",
                     content_type="application/json", auth=None):
        """Runs a post request"""
        logger.info("Creating session" + endpoint)
        if data is not None:
            md5 = hashlib.md5()
            md5.update(data)
            md5checksum = Base64Keywords().base64_encode(md5.hexdigest())
        else:
            md5checksum = None
        self.requests.create_session(alias,  endpoint, auth=auth)
        headers = self.create_headers(sdc_user_id=sdc_user, accept=accept, content_type=content_type, md5=md5checksum)
        resp = self.requests.post_request(alias,  data_path, files=files, data=data, headers=headers)
        logger.info("Received response from [" + alias + "]: " + resp.text)
        return resp

    def put_request(self, alias, endpoint, data_path, data, sdc_user=None, accept="application/json", auth=None):
        """Runs a put request"""
        logger.info("Creating session" + endpoint)
        self.requests.create_session(alias,  endpoint, auth=auth)
        headers = self.create_headers(sdc_user_id=sdc_user, accept=accept)
        resp = self.requests.put_request(alias,  data_path, data=data, headers=headers)
        logger.info("Received response from [" + alias + "]: " + resp.text)
        return resp

    def delete_request(self, alias, endpoint, data_path, data=None, sdc_user=None, accept="application/json", auth=None):
        """Runs a delete request"""
        logger.info("Creating session" + endpoint)
        self.requests.create_session(alias, endpoint, auth=auth)
        headers = self.create_headers(sdc_user_id=sdc_user, accept=accept)
        resp = self.requests.delete_request(alias, data_path, data=data, headers=headers)
        logger.info("Received response from [" + alias + "]: " + resp.text)
        return resp
