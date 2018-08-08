#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import os
from bob.gradiant.face.databases import MsuMfsdDatabase
from bob.gradiant.core import DatabasesPathChecker


class UnitTestReplayDatabase(unittest.TestCase):
    skip = not DatabasesPathChecker.check_if_environment_is_defined_for("MSU_MFSD_PATH")
    reason = "MSU_MFSD_PATH has not been found. Impossible to run these tests"

    def setUp(self):
        if not self.skip:
            self.path_database = os.environ['MSU_MFSD_PATH']

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: MsuMfsdDatabase('wrong_path')
                          )

    def test_name_static_method(self):
        self.assertEqual(MsuMfsdDatabase.name(), 'msu-mfsd')

    def test_is_a_collection_of_databases_static_method(self):
        self.assertFalse(MsuMfsdDatabase.is_a_collection_of_databases())

    @unittest.skipIf(skip, reason)
    def test_get_ground_truth_protocol_grandtest(self):
        database = MsuMfsdDatabase(self.path_database)
        dict_ground_truth = database.get_ground_truth('grandtest')

        self.assertEqual(len(dict_ground_truth['Train']), 80)
        self.assertEqual(len(dict_ground_truth['Dev']), 80)
        self.assertEqual(len(dict_ground_truth['Test']), 120)

    @unittest.skipIf(skip, reason)
    def test_get_all_accesses(self):
        database = MsuMfsdDatabase(self.path_database)
        dict_all_accesses = database.get_all_accesses()

        self.assertEqual(len(dict_all_accesses['Train']), 80)
        self.assertEqual(len(dict_all_accesses['Dev']), 80)
        self.assertEqual(len(dict_all_accesses['Test']), 120)
