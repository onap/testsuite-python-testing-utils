from unittest import TestCase


from vcpeutils.SoUtils import *


class SoUtilsTest(TestCase):

    def test(self):
        input_dict = dict()
        SoUtils.add_related_instance(input_dict, "test", "test2")
        results = dict()
        results['relatedInstanceList'] = [{"relatedInstance": {"instanceId": "test", "modelInfo": "test2"}}]
        self.assertDictContainsSubset(results, input_dict)
