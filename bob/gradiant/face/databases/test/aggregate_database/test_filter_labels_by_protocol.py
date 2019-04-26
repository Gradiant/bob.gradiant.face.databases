#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest

from bob.gradiant.face.databases import AggregateDatabase, get_one_pai_protocol, \
    COMMON_PAI_CATEGORISATION
from bob.gradiant.face.databases.classes.aggregate_database.protocols.capture_device_low_quality_access_type_low_quality \
    import CAPTURE_DEVICE_LOW_QUALITY_ACCESS_TYPE_LOW_QUALITY_PROTOCOL
from bob.gradiant.face.databases.classes.aggregate_database.filter_labels_by_protocol import filter_labels_by_protocol
from bob.gradiant.face.databases.classes.aggregate_database.protocols.unseen_attack import get_unseen_attack_protocol

from bob.gradiant.face.databases.test.test_resources import TestResources


class UnitTestFilterLabelsByProtocol(unittest.TestCase):

    def setUp(self):
        self.dict_all_labels = TestResources.get_aggregated_database_all_dict_labels()
        self.available_protocols = AggregateDatabase.get_available_protocols()

    def test_should_have_the_same_size_of_ground_truth_as_original_size_with_grandtest_protocol(self):
        filtered_labels = filter_labels_by_protocol(self.available_protocols['grandtest'], self.dict_all_labels)
        for subset in self.available_protocols['grandtest'].keys():
            number_accesses_per_subset = 0
            for db in self.dict_all_labels[subset]:
                number_accesses_per_subset += len(self.dict_all_labels[subset][db])
            self.assertEqual(len(filtered_labels[subset]), number_accesses_per_subset)

    def test_should_run_well_with_cross_dataset_protocol(self):
        prefix_protocol = "cross-dataset-test-"
        for name_protocol, protocol in self.available_protocols.items():

            if prefix_protocol in name_protocol:

                filtered_labels = filter_labels_by_protocol(protocol,
                                                            self.dict_all_labels)

                target_database = name_protocol.replace(prefix_protocol, "")
                number_accesses_per_subset = {}

                for subset in protocol.keys():
                    number_accesses_per_subset[subset] = 0
                    for db in self.dict_all_labels[subset]:
                        if subset == 'Test':
                            if db == target_database:
                                number_accesses_per_subset[subset] += len(self.dict_all_labels[subset][db])
                        else:
                            if db != target_database:
                                number_accesses_per_subset[subset] += len(self.dict_all_labels[subset][db])

                self.assertEqual(len(filtered_labels["Train"]), number_accesses_per_subset["Train"])
                self.assertEqual(len(filtered_labels["Dev"]), number_accesses_per_subset["Dev"])
                self.assertEqual(len(filtered_labels["Test"]), number_accesses_per_subset["Test"])

    def test_should_run_well_with_capture_device_low_quality_access_type_low_quality(self):
        allowed_common_pais = {'Train': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                               'Dev': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                               'Test': [0, 1, 4, 7]}

        allowed_common_capture_devices = {'Train': [0, 2],
                                          'Dev': [0, 2],
                                          'Test': [0, 1, 2, 3, 4, 5]}

        filtered_labels = filter_labels_by_protocol(CAPTURE_DEVICE_LOW_QUALITY_ACCESS_TYPE_LOW_QUALITY_PROTOCOL,
                                                    self.dict_all_labels)

        for subset in filtered_labels:
            for basename in filtered_labels[subset]:
                self.assertTrue(filtered_labels[subset][basename]["common_pai"] in allowed_common_pais[subset])
                self.assertTrue(filtered_labels[subset][basename]["common_capture_device"] in allowed_common_capture_devices[subset])

    def test_should_run_well_with_only_print_protocol(self):
        allowed_common_pais = {'Train': [0, 1, 2, 3],
                               'Dev': [0, 1, 2, 3],
                               'Test': [0, 1, 2, 3]}

        categorisation_filter = [{"category": "common_pai",
                                  "type": {"real": None,
                                           "print": None}}]
        new_protocol_dict = {
            "Train": {
                "common_categorisation": categorisation_filter
            },
            "Dev": {
                "common_categorisation": categorisation_filter
            },
            "Test": {
                "common_categorisation": categorisation_filter
            }
        }

        filtered_labels = filter_labels_by_protocol(new_protocol_dict, self.dict_all_labels)

        for subset in filtered_labels:
            for basename in filtered_labels[subset]:
                self.assertTrue(filtered_labels[subset][basename]["common_pai"] in allowed_common_pais[subset])

    def test_should_run_well_with_only_webcam(self):
        allowed_common_capture_devices = {'Train': [0, 1],
                                          'Dev': [0, 1],
                                          'Test': [0, 1]}

        categorisation_filter = [{"category": "common_capture_device",
                                  "type": {"webcam": None}}]
        new_protocol_dict = {
            "Train": {
                "common_categorisation": categorisation_filter
            },
            "Dev": {
                "common_categorisation": categorisation_filter
            },
            "Test": {
                "common_categorisation": categorisation_filter
            }
        }

        filtered_labels = filter_labels_by_protocol(new_protocol_dict, self.dict_all_labels)

        for subset in filtered_labels:
            for basename in filtered_labels[subset]:
                self.assertTrue(filtered_labels[subset][basename]["common_capture_device"]
                                in allowed_common_capture_devices[subset])

    def test_should_run_well_with_lightning_categorisation(self):
        allowed_common_lightning = {'Train': [0],
                                    'Dev': [0],
                                    'Test': [1]}

        new_protocol_dict = {
            "Train": {
                "common_categorisation": [{"category": "common_lightning",
                                           "type": {"controlled": None}}]
            },
            "Dev": {
                "common_categorisation": [{"category": "common_lightning",
                                           "type": {"controlled": None}}]
            },
            "Test": {
                "common_categorisation": [{"category": "common_lightning",
                                           "type": {"adverse": None}}]
            }
        }

        filtered_labels = filter_labels_by_protocol(new_protocol_dict, self.dict_all_labels)

        for subset in filtered_labels:
            for basename in filtered_labels[subset]:
                self.assertTrue(filtered_labels[subset][basename]["common_lightning"]
                                in allowed_common_lightning[subset])

    def test_should_run_well_with_face_resolution_categorisation(self):
        allowed_common_lightning = {'Train': [0],
                                    'Dev': [0],
                                    'Test': [2]}

        new_protocol_dict = {
            "Train": {
                "common_categorisation": [{"category": "common_face_resolution",
                                           "type": {"small_face": None}}]
            },
            "Dev": {
                "common_categorisation": [{"category": "common_face_resolution",
                                           "type": {"small_face": None}}]
            },
            "Test": {
                "common_categorisation": [{"category": "common_face_resolution",
                                           "type": {"big_face": None}}]
            }
        }

        filtered_labels = filter_labels_by_protocol(new_protocol_dict, self.dict_all_labels)

        for subset in filtered_labels:
            for basename in filtered_labels[subset]:
                self.assertTrue(filtered_labels[subset][basename]["common_face_resolution"]
                                in allowed_common_lightning[subset])

    def test_should_run_well_with_one_pai_print(self):
        pai = 'print'
        parsed_datasets = AggregateDatabase.get_parsed_databases()
        protocol = get_one_pai_protocol(parsed_datasets, pai)
        allowed_pai = [0, 1, 2, 3]

        filtered_labels = filter_labels_by_protocol(protocol, self.dict_all_labels)

        for subset in filtered_labels:
            for basename in filtered_labels[subset]:
                common_pai_value = filtered_labels[subset][basename]["common_pai"]
                self.assertTrue(common_pai_value in allowed_pai)

    def test_should_run_well_with_one_pai_replay(self):
        pai = 'replay'
        parsed_datasets = AggregateDatabase.get_parsed_databases()
        protocol = get_one_pai_protocol(parsed_datasets, pai)
        allowed_pai = [0, 4, 5, 6]

        filtered_labels = filter_labels_by_protocol(protocol, self.dict_all_labels)

        for subset in filtered_labels:
            for basename in filtered_labels[subset]:
                common_pai_value = filtered_labels[subset][basename]["common_pai"]
                self.assertTrue(common_pai_value in allowed_pai)

    def test_should_run_well_with_one_pai_mask(self):
        pai = 'mask'
        parsed_datasets = AggregateDatabase.get_parsed_databases()
        protocol = get_one_pai_protocol(parsed_datasets, pai)
        allowed_pai = [0, 7, 8, 9]

        filtered_labels = filter_labels_by_protocol(protocol, self.dict_all_labels)

        for subset in filtered_labels:
            for basename in filtered_labels[subset]:
                common_pai_value = filtered_labels[subset][basename]["common_pai"]
                self.assertTrue(common_pai_value in allowed_pai)

    def test_should_run_well_with_unseen_attack_print(self):
        pai = 'print'
        parsed_datasets = AggregateDatabase.get_parsed_databases()
        available_pais = COMMON_PAI_CATEGORISATION.keys()
        protocol = get_unseen_attack_protocol(parsed_datasets, pai, available_pais)

        allowed_pai = {"Train": [0, 4, 5, 6, 7, 8, 9],
                       "Dev": [0, 4, 5, 6, 7, 8, 9],
                       "Test": [0, 1, 2, 3]
                       }

        filtered_labels = filter_labels_by_protocol(protocol, self.dict_all_labels)

        for subset in filtered_labels:
            for basename in filtered_labels[subset]:
                common_pai_value = filtered_labels[subset][basename]["common_pai"]
                self.assertTrue(common_pai_value in allowed_pai[subset])

    def test_should_run_well_with_unseen_attack_replay(self):
        pai = 'replay'
        parsed_datasets = AggregateDatabase.get_parsed_databases()
        available_pais = COMMON_PAI_CATEGORISATION.keys()
        protocol = get_unseen_attack_protocol(parsed_datasets, pai, available_pais)

        allowed_pai = {"Train": [0, 1, 2, 3, 7, 8, 9],
                       "Dev": [0, 1, 2, 3, 7, 8, 9],
                       "Test": [0, 4, 5, 6]
                       }

        filtered_labels = filter_labels_by_protocol(protocol, self.dict_all_labels)

        for subset in filtered_labels:
            for basename in filtered_labels[subset]:
                common_pai_value = filtered_labels[subset][basename]["common_pai"]
                self.assertTrue(common_pai_value in allowed_pai[subset])

    def test_should_run_well_with_unseen_attack_mask(self):
        pai = 'mask'
        parsed_datasets = AggregateDatabase.get_parsed_databases()
        available_pais = COMMON_PAI_CATEGORISATION.keys()
        protocol = get_unseen_attack_protocol(parsed_datasets, pai, available_pais)

        allowed_pai = {"Train": [0, 1, 2, 3, 4, 5, 6],
                       "Dev": [0, 1, 2, 3, 4, 5, 6],
                       "Test": [0, 7, 8, 9]
                       }

        filtered_labels = filter_labels_by_protocol(protocol, self.dict_all_labels)

        for subset in filtered_labels:
            for basename in filtered_labels[subset]:
                common_pai_value = filtered_labels[subset][basename]["common_pai"]
                self.assertTrue(common_pai_value in allowed_pai[subset])
