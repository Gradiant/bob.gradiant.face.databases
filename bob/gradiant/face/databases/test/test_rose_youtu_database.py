#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest
import os
from bob.gradiant.face.databases import RoseYoutuDatabase
from bob.gradiant.core import DatabasesPathChecker


class UnitTestRoseYoutuDatabase(unittest.TestCase):
    skip = not DatabasesPathChecker.check_if_environment_is_defined_for("ROSE_YOUTU_PATH")
    reason = "ROSE_YOUTU_PATH has not been found. Impossible to run these tests"

    def setUp(self):
        if not self.skip:
            self.database = RoseYoutuDatabase(os.environ['ROSE_YOUTU_PATH'])
        else:
            self.database = RoseYoutuDatabase('/home')  # Dummy path
        self.available_common_pais = [0, 1, 6, 7]
        self.available_common_capture_devices = [2, 3]
        self.available_common_lightning = [2]
        self.available_common_face_resolution = [0, 1, 2]

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: RoseYoutuDatabase('wrong_path')
                          )

    def test_name_static_method(self):
        self.assertEqual(RoseYoutuDatabase.name(), 'rose-youtu')

    def test_is_a_collection_of_databases_static_method(self):
        self.assertFalse(RoseYoutuDatabase.is_a_collection_of_databases())

    @unittest.skipIf(skip, reason)
    def test_get_all_accesses(self):
        dict_all_accesses = self.database.get_all_accesses()

        self.assertEqual(len(dict_all_accesses['Train']), 1389)
        self.assertEqual(len(dict_all_accesses['Dev']), 359)
        self.assertEqual(len(dict_all_accesses['Test']), 1749)

    def test_get_all_labels(self):
        dict_all_labels = self.database.get_all_labels()

        self.assertEqual(len(dict_all_labels['Train']), 1389)
        self.assertEqual(len(dict_all_labels['Dev']), 359)
        self.assertEqual(len(dict_all_labels['Test']), 1749)

    def test_get_ground_truth_protocol_grandtest(self):
        dict_ground_truth = self.database.get_ground_truth('grandtest')

        self.assertEqual(len(dict_ground_truth['Train']), 1389)
        self.assertEqual(len(dict_ground_truth['Dev']), 359)
        self.assertEqual(len(dict_ground_truth['Test']), 1749)

    def test_common_labels_are_ok(self):
        dict_all_labels = self.database.get_all_labels()
        for subset, subset_dict in dict_all_labels.items():
            for basename, labels_dict in subset_dict.items():
                self.assertIn(labels_dict['common_pai'], self.available_common_pais)
                self.assertIn(labels_dict['common_capture_device'], self.available_common_capture_devices)
                self.assertIn(labels_dict['common_lightning'], self.available_common_lightning)
                self.assertIn(labels_dict['common_face_resolution'], self.available_common_face_resolution)
