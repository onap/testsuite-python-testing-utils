from six.moves import urllib
from robot.api.deco import keyword


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
