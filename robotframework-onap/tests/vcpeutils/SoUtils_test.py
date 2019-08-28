from unittest import TestCase


from vcpeutils.SoUtils import SoUtils


class SoUtilsTest(TestCase):
    def test(self):
        input_dict = dict()
        SoUtils.add_related_instance(input_dict, "test", "test2")
        results = dict()
        results['relatedInstanceList'] = [{"relatedInstance": {"instanceId": "test", "modelInfo": "test2"}}]
        self.assertEqual(results, self.extract_dict_a_from_b(results,input_dict))

    @staticmethod
    def extract_dict_a_from_b(a, b):
        return dict([(k, b[k]) for k in a.keys() if k in b.keys()])
