import base64
from unittest import TestCase

from ONAPLibrary.Base64Keywords import Base64Keywords


class Base64KeywordsTests(TestCase):

    def test_base64_encode(self):
        enc = Base64Keywords().base64_encode("string_to_encode")
        enc_base = base64.b64encode("string_to_encode".encode("utf-8"))
        self.assertEqual(enc_base, enc)

    def test_base64_decode(self):
        enc = Base64Keywords().base64_decode('c3RyaW5nX3RvX2RlY29kZQ==')
        self.assertEqual("string_to_decode", enc.decode("utf-8"))
