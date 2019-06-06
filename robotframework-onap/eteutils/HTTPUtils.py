from six.moves.urllib.parse import urlparse
from six.moves import urllib

import urllib3


class HTTPUtils:
    """HTTPUtils is common resource for simple http helper keywords."""

    def url_encode_string(self, barestring):
        """URL Encode String takes in a string and converts it into fully 'percent-encoded' string"""
        return urllib.parse.quote(barestring)

    def disable_warnings(self):
        """  Disable all warnings when creating sessions """
        urllib3.disable_warnings()

    def url_parse(self, url):
        """  Get pieces of the URL """
        return urlparse(url)
