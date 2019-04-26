#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest
import os
from bob.gradiant.face.databases import SiwDatabase
from bob.gradiant.core import DatabasesPathChecker


class UnitTestSiwDatabase(unittest.TestCase):
    skip = not DatabasesPathChecker.check_if_environment_is_defined_for("SIW_PATH")
    reason = "SIW_PATH has not been found. Impossible to run these tests"

    def setUp(self):
        if not self.skip:
            self.database = SiwDatabase(os.environ['SIW_PATH'])
        else:
            self.database = SiwDatabase('/home')  # Dummy path
        self.available_common_pais = [0, 2, 3, 5, 6]
        self.available_common_capture_devices = [1, 5]
        self.available_common_lightning = [0, 1, 2]
        self.available_common_face_resolution = [0, 1, 2]

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: SiwDatabase('wrong_path')
                          )

    def test_name_static_method(self):
        self.assertEqual(SiwDatabase.name(), 'siw')

    def test_is_a_collection_of_databases_static_method(self):
        self.assertFalse(SiwDatabase.is_a_collection_of_databases())

    @unittest.skipIf(skip, reason)
    def test_get_all_accesses(self):
        dict_all_accesses = self.database.get_all_accesses()

        self.assertEqual(len(dict_all_accesses['Train']), 2145)
        self.assertEqual(len(dict_all_accesses['Dev']), 272)
        self.assertEqual(len(dict_all_accesses['Test']), 2061)

    def test_get_all_labels(self):
        dict_all_labels = self.database.get_all_labels()

        self.assertEqual(len(dict_all_labels['Train']), 2145)
        self.assertEqual(len(dict_all_labels['Dev']), 272)
        self.assertEqual(len(dict_all_labels['Test']), 2061)

    def test_get_ground_truth_protocol_1(self):
        dict_ground_truth = self.database.get_ground_truth('protocol_1')

        self.assertEqual(len(dict_ground_truth['Train']), 2145)
        self.assertEqual(len(dict_ground_truth['Dev']), 272)
        self.assertEqual(len(dict_ground_truth['Test']), 2061)

    def test_common_labels_are_ok(self):
        dict_all_labels = self.database.get_all_labels()

        for subset, subset_dict in dict_all_labels.items():
            for basename, labels_dict in subset_dict.items():
                self.assertIn(labels_dict['common_pai'], self.available_common_pais)
                self.assertIn(labels_dict['common_capture_device'], self.available_common_capture_devices)
                self.assertIn(labels_dict['common_lightning'], self.available_common_lightning)
                self.assertIn(labels_dict['common_face_resolution'], self.available_common_face_resolution)
