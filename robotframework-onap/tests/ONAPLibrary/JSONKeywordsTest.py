# Copyright 2019 Samsung Electronics Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from unittest import TestCase

from ONAPLibrary.JSONKeywords import JSONKeywords


class JSONKeywordsTest(TestCase):
    content_empty_string = '{}'
    content_empty_dict = {}
    content1_string = '{"foo": "bar"}'
    content1_dict = {"foo": u"bar"}
    content1b_string = '{"foo": "quuz"}'
    content1b_dict = {"foo": u"quuz"}
    content2_string = '{"baz": "quuz"}'
    content2_dict = {"baz": u"quuz"}
    content_big_string = '{"foo": "bar", "baz": "quuz"}'
    content_big_dict = {"foo": u"bar", "baz": u"quuz"}

    def setUp(self):
        self.jk = JSONKeywords()

    # equality - corner cases
    def test_json_empty_strings_equality(self):
        left_json_string = JSONKeywordsTest.content_empty_string
        right_json_string = JSONKeywordsTest.content_empty_string
        self.assertTrue(self.jk.json_equals(left_json_string, right_json_string))

    def test_json_empty_objects_equality(self):
        left_json_object = JSONKeywordsTest.content_empty_dict
        right_json_object = JSONKeywordsTest.content_empty_dict
        self.assertTrue(self.jk.json_equals(left_json_object, right_json_object))

    # equality - type conversions
    def test_json_strings_equality(self):
        left_json_string = JSONKeywordsTest.content1_string
        right_json_string = JSONKeywordsTest.content1_string
        self.assertTrue(self.jk.json_equals(left_json_string, right_json_string))

    def test_json_objects_equality(self):
        left_json_object = JSONKeywordsTest.content1_dict
        right_json_object = JSONKeywordsTest.content1_dict
        self.assertTrue(self.jk.json_equals(left_json_object, right_json_object))

    def test_json_string_object_equality(self):
        left_json_string = JSONKeywordsTest.content1_string
        right_json_object = JSONKeywordsTest.content1_dict
        self.assertTrue(self.jk.json_equals(left_json_string, right_json_object))

    def test_json_object_string_equality(self):
        left_json_object = JSONKeywordsTest.content1_dict
        right_json_string = JSONKeywordsTest.content1_string
        self.assertTrue(self.jk.json_equals(left_json_object, right_json_string))

    # equality - difference detection
    def test_json_strings_inequality(self):
        left_json_string = JSONKeywordsTest.content1_string
        right_json_string = JSONKeywordsTest.content2_string
        self.assertFalse(self.jk.json_equals(left_json_string, right_json_string))

    def test_json_objects_inequality(self):
        left_json_object = JSONKeywordsTest.content1_dict
        right_json_object = JSONKeywordsTest.content2_dict
        self.assertFalse(self.jk.json_equals(left_json_object, right_json_object))

    def test_json_string_object_inequality(self):
        left_json_string = JSONKeywordsTest.content1_string
        right_json_object = JSONKeywordsTest.content2_dict
        self.assertFalse(self.jk.json_equals(left_json_string, right_json_object))

    def test_json_object_string_inequality(self):
        left_json_object = JSONKeywordsTest.content1_dict
        right_json_string = JSONKeywordsTest.content2_string
        self.assertFalse(self.jk.json_equals(left_json_object, right_json_string))

    # subsets - corner cases
    def test_json_empty_strings_subset(self):
        left_json_string = JSONKeywordsTest.content_empty_string
        right_json_string = JSONKeywordsTest.content_empty_string
        self.assertTrue(self.jk.json_should_contain_sub_json(left_json_string, right_json_string))

    def test_json_empty_objects_subset(self):
        left_json_object = JSONKeywordsTest.content_empty_dict
        right_json_object = JSONKeywordsTest.content_empty_dict
        self.assertTrue(self.jk.json_should_contain_sub_json(left_json_object, right_json_object))

    # subsets - type conversions
    def test_json_strings_subset(self):
        left_json_string = JSONKeywordsTest.content1_string
        right_json_string = JSONKeywordsTest.content1_string
        self.assertTrue(self.jk.json_should_contain_sub_json(left_json_string, right_json_string))

    def test_json_objects_subset(self):
        left_json_object = JSONKeywordsTest.content1_dict
        right_json_object = JSONKeywordsTest.content1_dict
        self.assertTrue(self.jk.json_should_contain_sub_json(left_json_object, right_json_object))

    def test_json_string_object_subset(self):
        left_json_string = JSONKeywordsTest.content1_string
        right_json_object = JSONKeywordsTest.content1_dict
        self.assertTrue(self.jk.json_should_contain_sub_json(left_json_string, right_json_object))

    def test_json_object_string_subset(self):
        left_json_object = JSONKeywordsTest.content1_dict
        right_json_string = JSONKeywordsTest.content1_string
        self.assertTrue(self.jk.json_should_contain_sub_json(left_json_object, right_json_string))

    # subsets - inclusion
    def test_json_strings_proper_subset(self):
        left_json_string = JSONKeywordsTest.content_big_string
        right_json_string = JSONKeywordsTest.content1_string
        self.assertTrue(self.jk.json_should_contain_sub_json(left_json_string, right_json_string))

    def test_json_objects_proper_subset(self):
        left_json_object = JSONKeywordsTest.content_big_dict
        right_json_object = JSONKeywordsTest.content1_dict
        self.assertTrue(self.jk.json_should_contain_sub_json(left_json_object, right_json_object))

    def test_json_string_object_proper_subset(self):
        left_json_string = JSONKeywordsTest.content_big_string
        right_json_object = JSONKeywordsTest.content1_dict
        self.assertTrue(self.jk.json_should_contain_sub_json(left_json_string, right_json_object))

    def test_json_object_string_proper_subset(self):
        left_json_object = JSONKeywordsTest.content_big_dict
        right_json_string = JSONKeywordsTest.content1_string
        self.assertTrue(self.jk.json_should_contain_sub_json(left_json_object, right_json_string))

    # subsets - intersection
    def test_json_strings_intersection(self):
        left_json_string = JSONKeywordsTest.content1_string
        right_json_string = JSONKeywordsTest.content_big_string
        self.assertFalse(self.jk.json_should_contain_sub_json(left_json_string, right_json_string))

    def test_json_objects_intersection(self):
        left_json_object = JSONKeywordsTest.content1_dict
        right_json_object = JSONKeywordsTest.content_big_dict
        self.assertFalse(self.jk.json_should_contain_sub_json(left_json_object, right_json_object))

    def test_json_string_object_intersection(self):
        left_json_string = JSONKeywordsTest.content1_dict
        right_json_object = JSONKeywordsTest.content_big_string
        self.assertFalse(self.jk.json_should_contain_sub_json(left_json_string, right_json_object))

    def test_json_object_string_intersection(self):
        left_json_object = JSONKeywordsTest.content1_string
        right_json_string = JSONKeywordsTest.content_big_dict
        self.assertFalse(self.jk.json_should_contain_sub_json(left_json_object, right_json_string))

    # subsets - exclusion
    def test_json_strings_exclusion(self):
        left_json_string = JSONKeywordsTest.content1_string
        right_json_string = JSONKeywordsTest.content2_string
        self.assertFalse(self.jk.json_equals(left_json_string, right_json_string))

    def test_json_objects_exclusion(self):
        left_json_object = JSONKeywordsTest.content1_dict
        right_json_object = JSONKeywordsTest.content2_dict
        self.assertFalse(self.jk.json_equals(left_json_object, right_json_object))

    def test_json_string_object_exclusion(self):
        left_json_string = JSONKeywordsTest.content1_string
        right_json_object = JSONKeywordsTest.content2_dict
        self.assertFalse(self.jk.json_equals(left_json_string, right_json_object))

    def test_json_object_string_exclusion(self):
        left_json_object = JSONKeywordsTest.content1_dict
        right_json_string = JSONKeywordsTest.content2_string
        self.assertFalse(self.jk.json_equals(left_json_object, right_json_string))

    # subsets - value change detection
    def test_json_strings_changed_value(self):
        left_json_string = JSONKeywordsTest.content1_string
        right_json_string = JSONKeywordsTest.content1b_string
        self.assertFalse(self.jk.json_equals(left_json_string, right_json_string))

    def test_json_objects_changed_value(self):
        left_json_object = JSONKeywordsTest.content1_dict
        right_json_object = JSONKeywordsTest.content1b_dict
        self.assertFalse(self.jk.json_equals(left_json_object, right_json_object))

    def test_json_string_object_changed_value(self):
        left_json_string = JSONKeywordsTest.content1_string
        right_json_object = JSONKeywordsTest.content1b_dict
        self.assertFalse(self.jk.json_equals(left_json_string, right_json_object))

    def test_json_object_string_changed_value(self):
        left_json_object = JSONKeywordsTest.content1_dict
        right_json_string = JSONKeywordsTest.content1b_string
        self.assertFalse(self.jk.json_equals(left_json_object, right_json_string))
