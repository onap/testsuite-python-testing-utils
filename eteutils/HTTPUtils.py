import urllib

class HTTPUtils:
    """HTTPUtils is common resource for simple http helper keywords."""
    
    def url_encode_string(self, barestring):
        """URL Encode String takes in a string and converts into 'percent-encoded' string"""
        return urllib.quote_plus(barestring) 