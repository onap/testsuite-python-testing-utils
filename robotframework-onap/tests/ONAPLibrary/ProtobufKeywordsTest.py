from unittest import TestCase

from ONAPLibrary.ProtobufKeywords import ProtobufKeywords


class ProtobufKeywordsTest(TestCase):

    def test(self):
        with open("hvves_msg.raw", "rb") as fileToDo:
            value = fileToDo.read()
        pb = ProtobufKeywords()
        result = pb.compare_file_to_message("hvves_msg.raw", value)
        self.assertTrue(result)

    def test_compare_two(self):
        with open("hvves_msg.raw", "rb") as fileToDo:
            value = fileToDo.read()
        pb = ProtobufKeywords()
        result = pb.compare_two_messages(value, value)
        self.assertTrue(result)

    def test_compare_two_many(self):
        with open("hvves_msg.raw", "rb") as fileToDo:
            value = fileToDo.read()
        pb = ProtobufKeywords()
        result = pb.compare_two_messages(value, value)
        self.assertTrue(result)
        result = pb.compare_two_messages(value, value)
        self.assertTrue(result)
