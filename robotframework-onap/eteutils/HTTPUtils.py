from six.moves.urllib.parse import urlparse

import urllib
import urllib3


class HTTPUtils:
    """HTTPUtils is common resource for simple http helper keywords."""

    def url_encode_string(self, barestring):
        """URL Encode String takes in a string and converts into 'percent-encoded' string"""
        return urllib.quote_plus(barestring)

    def disable_warnings(self):
        """  Disable the cert warnings when creating sessions for A&AI API Calls """
        urllib3.disable_warnings()

    def url_parse(self, url):
        """  Get pieces of the URL """
        return urlparse.urlparse(url)