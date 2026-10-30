# Copyright (C) 2026 Deutsche Telekom AG. All rights reserved.
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

from unittest import TestCase, mock

import requests
from RequestsLibrary import log as requests_log

import ONAPLibrary  # noqa: F401 - importing the package installs the redaction
from ONAPLibrary.BasicAuthKeywords import BasicAuthKeywords, BasicAuth, redact_authorization, \
    install_requests_log_redaction, _RedactingLogger


class BasicAuthKeywordsTests(TestCase):

    def test_create_basic_auth_masks_password(self):
        auth = BasicAuthKeywords().create_basic_auth("InfraPortalClient", "s3cret")
        self.assertEqual(("InfraPortalClient", "s3cret"), auth)
        self.assertNotIn("s3cret", repr(auth))
        self.assertNotIn("s3cret", str(auth))
        self.assertIn("InfraPortalClient", str(auth))

    def test_basic_auth_is_usable_by_requests(self):
        auth = requests.auth.HTTPBasicAuth(*BasicAuth("user", "s3cret"))
        request = auth(requests.Request("GET", "http://localhost/").prepare())
        self.assertEqual("Basic dXNlcjpzM2NyZXQ=", request.headers["Authorization"])

    def test_redact_authorization(self):
        message = "GET Request : headers={'Accept': '*/*', 'Authorization': 'Basic dXNlcjpzM2NyZXQ='}"
        self.assertEqual("GET Request : headers={'Accept': '*/*', 'Authorization': '***'}",
                         redact_authorization(message))
        self.assertEqual("headers={'proxy-authorization': '***'}",
                         redact_authorization("headers={'proxy-authorization': 'Bearer abc'}"))
        self.assertEqual("no header here", redact_authorization("no header here"))

    def test_package_import_installs_redaction(self):
        self.assertIsInstance(requests_log.logger, _RedactingLogger)
        install_requests_log_redaction()
        self.assertNotIsInstance(requests_log.logger._logger, _RedactingLogger)

    def test_redacting_logger_masks_messages(self):
        wrapped = mock.Mock()
        logger = _RedactingLogger(wrapped)
        logger.info("headers={'Authorization': 'Basic dXNlcjpzM2NyZXQ='}")
        wrapped.info.assert_called_once_with("headers={'Authorization': '***'}")
        self.assertIs(wrapped.LOGLEVEL, logger.LOGLEVEL)
