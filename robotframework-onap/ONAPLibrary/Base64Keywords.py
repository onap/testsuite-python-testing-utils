from robot.api.deco import keyword
import base64


class Base64Keywords(object):
    """ Utilities useful for generating UUIDs """

    def __init__(self):
        super(Base64Keywords, self).__init__()

    @keyword
    def base64_encode(self, string_to_encode):
        """generate a base64 encoded string"""
        return base64.b64encode(string_to_encode.encode("utf-8"))

    @keyword
    def base64_decode(self, string_to_decode):
        """decode a base64 encoded string"""
        return base64.b64decode(string_to_decode.encode("utf-8"))
