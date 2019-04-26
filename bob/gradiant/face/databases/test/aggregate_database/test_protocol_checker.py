#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2018+ Gradiant, Vigo, Spain
import unittest


from bob.gradiant.face.databases import protocol_checker


class UnitTestProtocolChecker(unittest.TestCase):

    def test_should_throw_an_exception_when_the_expected_three_subsets_are_not_defined(self):
        protocol = {'Train': None,
                    'Dev': None}
        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_throw_an_exception_when_there_are_more_subsets_than_expected(self):
        protocol = {'Train': None,
                    'Dev': None,
                    'Test': None,
                    'OtherSubset': None}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_throw_an_exception_when_there_are_more_subsets_than_expected(self):
        protocol = {'Train': None,
                    'Dev': None,
                    'Test': None,
                    'OtherSubset': None}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_not_throw_any_exception_when_is_declared_as_default_protocol(self):
        protocol = {'Train': None,
                    'Dev': None,
                    'Test': None}

        protocol_checker(protocol)

    def test_should_throw_an_exception_when_datasets_is_not_a_list(self):
        wrong_subset_settings = {
            'datasets': 'not_a_list',
            'common_categorization': []
        }
        protocol = {'Train': wrong_subset_settings,
                    'Dev': wrong_subset_settings,
                    'Test': wrong_subset_settings}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_throw_an_exception_when_common_categorization_is_not_a_list(self):
        wrong_subset_settings = {
            'datasets': [],
            'common_categorization': 'not_a_list'
        }
        protocol = {'Train': wrong_subset_settings,
                    'Dev': wrong_subset_settings,
                    'Test': wrong_subset_settings}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_not_throw_an_exception_when_datasets_and_common_categorization_is_none(self):
        not_defined_subset_settings = {
            'datasets': None,
            'common_categorization': None
        }
        protocol = {'Train': not_defined_subset_settings,
                    'Dev': not_defined_subset_settings,
                    'Test': not_defined_subset_settings}

        protocol_checker(protocol)

    def test_should_throw_an_exception_when_set_database_is_not_defined_as_a_dict_with_name_and_subset(self):
        not_defined_dataset_subset_settings = {
            'datasets': ['not-defined-well'],
            'common_categorization': None
        }
        protocol = {'Train': not_defined_dataset_subset_settings,
                    'Dev': not_defined_dataset_subset_settings,
                    'Test': not_defined_dataset_subset_settings}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_throw_an_exception_when_subset_info_is_wrong_formatted(self):
        not_defined_dataset_subset_settings = {
            'datasets': [{"bad_format": [], 'subsets': []}],
            'common_categorization': None
        }
        protocol = {'Train': not_defined_dataset_subset_settings,
                    'Dev': not_defined_dataset_subset_settings,
                    'Test': not_defined_dataset_subset_settings}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_throw_an_exception_when_subset_info_is_well_formatted_but_with_invalid_dataset_name(self):
        not_defined_dataset_subset_settings = {
            'datasets': [{"name": 'invalid-dataset', 'subsets': ['Train']}],
            'common_categorization': None
        }
        protocol = {'Train': not_defined_dataset_subset_settings,
                    'Dev': not_defined_dataset_subset_settings,
                    'Test': not_defined_dataset_subset_settings}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_throw_an_exception_when_subset_info_is_well_formatted_but_with_invalid_subset_value(self):
        not_defined_dataset_subset_settings = {
            'datasets': [{"name": 'replay-mobile', 'subsets': ['invalid_subset']}],
            'common_categorization': None
        }
        protocol = {'Train': not_defined_dataset_subset_settings,
                    'Dev': not_defined_dataset_subset_settings,
                    'Test': not_defined_dataset_subset_settings}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_not_throw_an_exception_when_subset_is_well_formatted_and_with_valid_values(self):
        well_defined_dataset_subset_settings = {
            'datasets': [{"name": 'replay-mobile', 'subsets': ['Train']}],
            'common_categorization': None
        }
        protocol = {'Train': well_defined_dataset_subset_settings,
                    'Dev': well_defined_dataset_subset_settings,
                    'Test': well_defined_dataset_subset_settings}

        protocol_checker(protocol)

    def test_should_throw_an_exception_when_common_categorization_is_wrong_formatted(self):
        not_defined_common_categorization_subset_settings = {
            'datasets': [{"name": 'replay-mobile', 'subsets': ['Train']}],
            'common_categorization': ['not-defined-well']
        }
        protocol = {'Train': not_defined_common_categorization_subset_settings,
                    'Dev': not_defined_common_categorization_subset_settings,
                    'Test': not_defined_common_categorization_subset_settings}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_throw_an_exception_when_common_categorization_is_wrong_formatted_with_invalid_key(self):
        not_defined_common_categorization_subset_settings = {
            'datasets': [{"name": 'replay-mobile', 'subsets': ['Train']}],
            'common_categorization': [{"bad_format": "", 'type': {}}],
        }
        protocol = {'Train': not_defined_common_categorization_subset_settings,
                    'Dev': not_defined_common_categorization_subset_settings,
                    'Test': not_defined_common_categorization_subset_settings}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_throw_an_exception_when_common_categorization_info_is_well_formatted_but_with_invalid_category_name(self):
        not_defined_common_categorization_subset_settings = {
            'datasets': [{"name": 'replay-mobile', 'subsets': ['Train']}],
            'common_categorization': [{"category": "no_valid_name", 'type': {}}],
        }
        protocol = {'Train': not_defined_common_categorization_subset_settings,
                    'Dev': not_defined_common_categorization_subset_settings,
                    'Test': not_defined_common_categorization_subset_settings}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_throw_an_exception_when_common_categorization_info_is_well_formatted_but_with_invalid_type_name(self):
        not_defined_common_categorization_subset_settings = {
            'datasets': [{"name": 'replay-mobile', 'subsets': ['Train']}],
            'common_categorization': [{"category": "common_capture_device", 'type': {"no_valid_name": []}}],
        }
        protocol = {'Train': not_defined_common_categorization_subset_settings,
                    'Dev': not_defined_common_categorization_subset_settings,
                    'Test': not_defined_common_categorization_subset_settings}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_should_throw_an_exception_when_common_categorization_info_is_well_formatted_but_with_invalid_sub_type_name(self):
        not_defined_common_categorization_subset_settings = {
            'datasets': [{"name": 'replay-mobile', 'subsets': ['Train']}],
            'common_categorization': [{"category": "common_capture_device", 'type': {'webcam': ["no_valid_name"]}}],
        }
        protocol = {'Train': not_defined_common_categorization_subset_settings,
                    'Dev': not_defined_common_categorization_subset_settings,
                    'Test': not_defined_common_categorization_subset_settings}

        self.assertRaises(ValueError, lambda: protocol_checker(protocol))

    def test_not_should_throw_an_exception_when_datasets_and_common_categorization_is_well_formatted_with_valid_values(self):
        not_defined_common_categorization_subset_settings = {
            'datasets': [{"name": 'replay-mobile', 'subsets': ['Train']}],
            'common_categorization': [{"category": "common_capture_device", 'type': {'webcam': ["low_quality"]}}],
        }
        protocol = {'Train': not_defined_common_categorization_subset_settings,
                    'Dev': not_defined_common_categorization_subset_settings,
                    'Test': not_defined_common_categorization_subset_settings}

        protocol_checker(protocol)
