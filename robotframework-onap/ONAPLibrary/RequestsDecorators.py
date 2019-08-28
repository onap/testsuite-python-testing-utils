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

from robot.api import logger


def log_wrapped(func):
    def _log_wrapped(*args, **kwargs):
        if 'endpoint' in kwargs:
            endpoint = kwargs['endpoint']
            logger.info("Creating session " + endpoint)
        resp = func(*args, **kwargs)
        if 'alias' in kwargs:
            alias = kwargs['alias']
            logger.info("Received response from [" + alias + "]: " + resp.text)
        return resp

    return _log_wrapped


def default_keywords(func):
    def _default_keywords(*args, **kwargs):
        dicts = _keyword_defaults(**kwargs)
        return func(*args, **dicts)

    def _keyword_defaults(**kwargs):
        if 'alias' not in kwargs:
            raise ValueError('named attribute alias required', 'alias')
        if 'endpoint' not in kwargs:
            raise ValueError('named attribute required', 'endpoint')
        if 'data_path' not in kwargs:
            kwargs['data_path'] = None  # default to whatever is in the session
        if 'data' not in kwargs:
            kwargs['data'] = None  # default to empty body
        if 'sdc_user' not in kwargs:
            kwargs['sdc_user'] = None  # default to no user
        if 'accept' not in kwargs:
            kwargs['accept'] = "application/json"  # default to json
        if 'content_type' not in kwargs:
            kwargs['content_type'] = "application/json"  # default to json
        if 'auth' not in kwargs:
            kwargs['auth'] = None  # default to no basic auth
        if 'client_certs' not in kwargs:
            kwargs['client_certs'] = None  # default to no client cert
        if 'files' not in kwargs:
            kwargs['files'] = None   # default to no file
        return kwargs

    return _default_keywords
