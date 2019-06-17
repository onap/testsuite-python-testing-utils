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

from six.moves import urllib
from robot.api.deco import keyword
import urllib3


class HTTPKeywords(object):
    """HTTPKeywords is common resource for simple http helper keywords."""
    def __init__(self):
        super(HTTPKeywords, self).__init__()

    @keyword
    def url_encode_string(self, barestring):
        """URL Encode String takes in a string and converts it into fully 'percent-encoded' string"""
        return urllib.parse.quote(barestring)

    @keyword
    def url_parse(self, url):
        """  Get pieces of the URL """
        return urllib.parse.urlparse(url)

    @keyword
    def disable_warnings(self):
        """  Disable all warnings when creating sessions """
        urllib3.disable_warnings()
