from unittest import TextTestRunner
from unittest import TestLoader
from unittest import TestSuite

# import your test modules
from tests.vcpeutils.SoUtils_test import SoUtilsTest
from tests.ONAPLibrary.ProtobufKeywordsTest import ProtobufKeywordsTest


# initialize the test suite
loader = TestLoader()
suite = TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromTestCase(ProtobufKeywordsTest))
suite.addTests(loader.loadTestsFromTestCase(SoUtilsTest))

# initialize a runner, pass it your suite and run it
runner = TextTestRunner(verbosity=3)
result = runner.run(suite)
