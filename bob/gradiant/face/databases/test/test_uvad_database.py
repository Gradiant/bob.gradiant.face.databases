#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest
import os
from bob.gradiant.face.databases import UvadDatabase
from bob.gradiant.core import DatabasesPathChecker


class UnitTestUvadDatabase(unittest.TestCase):
    skip = not DatabasesPathChecker.check_if_environment_is_defined_for("UVAD_PATH")
    reason = "UVAD_PATH has not been found. Impossible to run these tests"

    def setUp(self):
        if not self.skip:
            self.database = UvadDatabase(os.environ['UVAD_PATH'])
        else:
            self.database = UvadDatabase('/home')  # Dummy path
        self.available_common_pais = [0, 1, 5, 6]
        self.available_common_capture_devices = [5]
        self.available_common_lightning = [2]
        self.available_common_face_resolution = [0, 1]

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: UvadDatabase('wrong_path')
                          )

    def test_name_static_method(self):
        self.assertEqual(UvadDatabase.name(), 'uvad')

    def test_is_a_collection_of_databases_static_method(self):
        self.assertFalse(UvadDatabase.is_a_collection_of_databases())

    @unittest.skipIf(skip, reason)
    def test_get_all_accesses(self):
        dict_all_accesses = self.database.get_all_accesses()

        self.assertEqual(len(dict_all_accesses['Train']), 4124)
        self.assertEqual(len(dict_all_accesses['Dev']), 1020)
        self.assertEqual(len(dict_all_accesses['Test']), 5144)

    def test_get_all_labels(self):
        dict_all_labels = self.database.get_all_labels()

        self.assertEqual(len(dict_all_labels['Train']), 4124)
        self.assertEqual(len(dict_all_labels['Dev']), 1020)
        self.assertEqual(len(dict_all_labels['Test']), 5144)

    def test_get_ground_truth_protocol_1(self):
        dict_gt = self.database.get_ground_truth('grandtest')

        self.assertEqual(len(dict_gt['Train']), 4124)
        self.assertEqual(len(dict_gt['Dev']), 1020)
        self.assertEqual(len(dict_gt['Test']), 5144)

    def test_common_labels_are_ok(self):
        dict_all_labels = self.database.get_all_labels()

        for subset, subset_dict in dict_all_labels.items():
            for basename, labels_dict in subset_dict.items():
                self.assertIn(labels_dict['common_pai'], self.available_common_pais)
                self.assertIn(labels_dict['common_capture_device'], self.available_common_capture_devices)
                self.assertIn(labels_dict['common_lightning'], self.available_common_lightning)
                self.assertIn(labels_dict['common_face_resolution'], self.available_common_face_resolution)
