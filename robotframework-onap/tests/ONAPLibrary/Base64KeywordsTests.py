import base64
from unittest import TestCase

from ONAPLibrary.Base64Keywords import Base64Keywords


class Base64KeywordsTests(TestCase):

    def test_base64_encode(self):
        enc = Base64Keywords().base64_encode("string_to_encode")
        enc_base = base64.b64encode("string_to_encode")
        self.assertEqual(enc_base, enc)

    def test_base64_decode(self):
        enc_base = base64.b64encode("string_to_decode")
        enc = Base64Keywords().base64_decode(enc_base)
        self.assertEqual("string_to_decode", enc)