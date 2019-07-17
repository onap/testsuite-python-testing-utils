from ONAPLibrary.VESProtobuf import *
from ONAPLibrary.JSONKeywords import JSONKeywords
from robot.api.deco import keyword


class ProtobufKeywords(object):
    """ Utilities useful for Protobuf manipulation """

    def __init__(self):
        super(ProtobufKeywords, self).__init__()
        self.vpf = VESProtobuf()

    @keyword
    def compare_file_to_message(self, file_name, message):
        with open(file_name, "rb") as file_to_do:
            return self.compare_two_messages(file_to_do.read(), message)

    def compare_two_messages(self, left, right):
        left_json = self.vpf.binary_to_json(left)
        right_json = self.vpf.binary_to_json(right)
        return JSONKeywords().json_equals(left_json, right_json)
