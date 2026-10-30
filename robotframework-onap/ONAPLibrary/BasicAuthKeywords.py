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

import re

from robot.api.deco import keyword

REDACTED = "***"
_AUTHORIZATION_VALUE = re.compile(r"""((?:proxy-)?authorization['"]?\s*:\s*['"])[^'"]*""", re.IGNORECASE)


class BasicAuth(tuple):
    """(username, password) pair whose string forms do not reveal the password.

    Robot logs every ``${var}=`` assignment at INFO, so a plain list built with
    ``Create List`` puts the password into log.html.
    """

    def __new__(cls, username, password):
        return super(BasicAuth, cls).__new__(cls, (username, password))

    def __repr__(self):
        return "BasicAuth(%r, %r)" % (self[0], REDACTED)

    __str__ = __repr__


def redact_authorization(message):
    """Mask the value of Authorization headers in a log message."""
    return _AUTHORIZATION_VALUE.sub(r"\1" + REDACTED, message)


class _RedactingLogger(object):
    """Proxy for robot.api.logger that masks Authorization headers."""

    def __init__(self, logger):
        self._logger = logger

    def __getattr__(self, name):
        attribute = getattr(self._logger, name)
        if name not in ("write", "trace", "debug", "info", "warn", "error", "console"):
            return attribute

        def log(msg, *args, **kwargs):
            return attribute(redact_authorization(msg), *args, **kwargs)
        return log


def install_requests_log_redaction():
    """Make RequestsLibrary stop logging Authorization headers.

    RequestsLibrary logs every prepared request, including the Authorization
    header that requests derives from the session auth, at INFO.
    """
    from RequestsLibrary import log as requests_log
    if not isinstance(requests_log.logger, _RedactingLogger):
        requests_log.logger = _RedactingLogger(requests_log.logger)


class BasicAuthKeywords(object):
    """Keywords for credentials that must not end up in the Robot logs."""

    def __init__(self):
        super(BasicAuthKeywords, self).__init__()

    @keyword
    def create_basic_auth(self, username, password):
        """Returns a username/password pair usable as ``auth=`` that is logged with the password masked."""
        return BasicAuth(username, password)
