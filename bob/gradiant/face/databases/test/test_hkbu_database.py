#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
import unittest

from bob.gradiant.face.databases import HkbuDatabase
from bob.gradiant.core import DatabasesPathChecker


class UnitTestHkbuDatabase(unittest.TestCase):
    skip = not DatabasesPathChecker.check_if_environment_is_defined_for("HKBU_PATH")
    reason = "HKBU_PATH has not been found. Impossible to run these tests"

    def setUp(self):
        if not self.skip:
            self.database = HkbuDatabase(os.environ['HKBU_PATH'])
        else:
            self.database = HkbuDatabase('/home')  # Dummy path
        self.available_common_pais = [0, 8]
        self.available_common_capture_devices = [1]
        self.available_common_lightning = [0]
        self.available_common_face_resolution = [0, 1]

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: HkbuDatabase('wrong_path')
                          )

    def test_name_static_method(self):
        self.assertEqual(HkbuDatabase.name(), 'hkbu')

    def test_is_a_collection_of_databases_static_method(self):
        self.assertFalse(HkbuDatabase.is_a_collection_of_databases())

    @unittest.skipIf(skip, reason)
    def test_get_all_accesses(self):
        dict_all_accesses = self.database.get_all_accesses()

        self.assertEqual(len(dict_all_accesses['Train']), 45)
        self.assertEqual(len(dict_all_accesses['Dev']), 35)
        self.assertEqual(len(dict_all_accesses['Test']), 30)

    def test_get_all_labels(self):
        dict_all_labels = self.database.get_all_labels()

        self.assertEqual(len(dict_all_labels['Train']), 45)
        self.assertEqual(len(dict_all_labels['Dev']), 35)
        self.assertEqual(len(dict_all_labels['Test']), 30)

    def test_get_ground_truth_protocol_grandtest(self):
        dict_ground_truth = self.database.get_ground_truth('grandtest')

        self.assertEqual(len(dict_ground_truth['Train']), 45)
        self.assertEqual(len(dict_ground_truth['Dev']), 35)
        self.assertEqual(len(dict_ground_truth['Test']), 30)

    def test_common_labels_are_ok(self):
        dict_all_labels = self.database.get_all_labels()

        for subset, subset_dict in dict_all_labels.items():
            for basename, labels_dict in subset_dict.items():
                self.assertIn(labels_dict['common_pai'], self.available_common_pais)
                self.assertIn(labels_dict['common_capture_device'], self.available_common_capture_devices)
                self.assertIn(labels_dict['common_lightning'], self.available_common_lightning)
                self.assertIn(labels_dict['common_face_resolution'], self.available_common_face_resolution)
