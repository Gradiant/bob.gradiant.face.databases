#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest
import os
from bob.gradiant.face.databases import AggregateDatabase
from bob.gradiant.core import DatabasesPathChecker


class UnitTestAggregateDatabase(unittest.TestCase):
    skip = not DatabasesPathChecker.check_if_environment_is_defined_for("CSMAD_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("CASIA_FASD_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("CASIA_SURF_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("HKBU_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("MSU_MFSD_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("OULU_NPU_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("REPLAY_ATTACK_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("REPLAY_MOBILE_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("ROSE_YOUTU_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("SIW_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("THREEDMAD_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("UVAD_PATH")

    reason = "REPLAY_ATTACK_PATH, REPLAY_MOBILE_PATH, MSU_MFSD_PATH, HKBU_PATH,OULU_NPU_PATH, ROSE_YOUTU_PATH, SIW_PATH," \
             "THREEDMAD_PATH, CASIA_FASD_PATH, CASIA_SURF_PATH, CSMAD_PATH, UVAD_PATH have not been found. Impossible to run these tests "

    def setUp(self):
        if not self.skip:
            self.base_paths = {
                '3dmad': os.environ['THREEDMAD_PATH'],
                'casia-fasd': os.environ['CASIA_FASD_PATH'],
                'casia-surf': os.environ['CASIA_SURF_PATH'],
                'csmad': os.environ['CSMAD_PATH'],
                'hkbu': os.environ['HKBU_PATH'],
                'msu-mfsd': os.environ['MSU_MFSD_PATH'],
                'oulu-npu': os.environ['OULU_NPU_PATH'],
                'replay-attack': os.environ['REPLAY_ATTACK_PATH'],
                'replay-mobile': os.environ['REPLAY_MOBILE_PATH'],
                'rose-youtu': os.environ['ROSE_YOUTU_PATH'],
                'siw': os.environ['SIW_PATH'],
                'uvad': os.environ['UVAD_PATH'],
            }

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: AggregateDatabase('wrong_path')
                          )

    def test_name_static_method(self):
        self.assertEqual(AggregateDatabase.name(), 'aggregate-database')

    def test_is_a_collection_of_databases_static_method(self):
        self.assertTrue(AggregateDatabase.is_a_collection_of_databases())

    @unittest.skipIf(skip, reason)
    def test_should_add_new_custom_protocol_correctly(self):
        database = AggregateDatabase(self.base_paths)
        database.set_new_custom_protocol({"new_protocol": {"Train": None, "Test": None, "Dev": None}})
        self.assertTrue("new_protocol" in database.protocols)

    @unittest.skipIf(skip, reason)
    def test_get_all_accesses(self):
        database = AggregateDatabase(self.base_paths)
        dict_all_accesses = database.get_all_accesses()

        self.assertEqual(len(dict_all_accesses['All']), 28134)

    @unittest.skipIf(skip, reason)
    def test_get_all_labels(self):
        database = AggregateDatabase(self.base_paths)
        dict_all_labels = database.get_all_labels()
        grandtest_results = {'Train': 11125, 'Dev': 4215, 'Test': 12794}

        for subset, subset_labels in dict_all_labels.items():
            number_accesses_per_subset = 0
            for db, db_labels_dict in subset_labels.items():
                number_accesses_per_subset += len(db_labels_dict)
            self.assertEqual(grandtest_results[subset], number_accesses_per_subset)

    @unittest.skipIf(skip, reason)
    def test_get_ground_truth_protocol_grandtest(self):
        database = AggregateDatabase(self.base_paths)
        dict_ground_truth = database.get_ground_truth('grandtest')

        self.assertEqual(len(dict_ground_truth['Train']), 11125)
        self.assertEqual(len(dict_ground_truth['Dev']), 4215)
        self.assertEqual(len(dict_ground_truth['Test']), 12794)

    # @unittest.skipIf(skip, reason)
    # def test_get_ground_truth_protocol_only_print(self):
    #     database = AggregateDatabase(self.base_paths)
    #
    #     categorisation_filter = [{"category": "common_pai",
    #                               "type": {"real": None,
    #                                        "print": None}}]
    #     new_protocol_dict = {
    #         "Train": {
    #             "common_categorisation": categorisation_filter
    #         },
    #         "Dev": {
    #             "common_categorisation": categorisation_filter
    #         },
    #         "Test": {
    #             "common_categorisation": categorisation_filter
    #         }
    #     }
    #
    #     database.set_new_custom_protocol({"test_protocol": new_protocol_dict})
    #     dict_ground_truth = database.get_ground_truth('test_protocol')
    #
    #     self.assertEqual(len(dict_ground_truth['Train']), 3660)
    #     self.assertEqual(len(dict_ground_truth['Dev']), 1652)
    #     self.assertEqual(len(dict_ground_truth['Test']), 3602)
    #
    # @unittest.skipIf(skip, reason)
    # def test_get_ground_truth_protocol_only_webcams(self):
    #     database = AggregateDatabase(self.base_paths)
    #
    #     categorisation_filter = [{"category": "common_capture_device",
    #                               "type": {"webcam": None}}]
    #     new_protocol_dict = {
    #         "Train": {
    #             "common_categorisation": categorisation_filter
    #         },
    #         "Dev": {
    #             "common_categorisation": categorisation_filter
    #         },
    #         "Test": {
    #             "common_categorisation": categorisation_filter
    #         }
    #     }
    #
    #     database.set_new_custom_protocol({"test_protocol": new_protocol_dict})
    #     dict_ground_truth = database.get_ground_truth('test_protocol')
    #
    #     self.assertEqual(len(dict_ground_truth['Train']), 1738)
    #     self.assertEqual(len(dict_ground_truth['Dev']), 750)
    #     self.assertEqual(len(dict_ground_truth['Test']), 1885)
