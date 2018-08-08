#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import os
from bob.gradiant.face.databases import UvadDatabase
from bob.gradiant.core import DatabasesPathChecker


class UnitTestUvadDatabase(unittest.TestCase):
    skip = not DatabasesPathChecker.check_if_environment_is_defined_for("UVAD_PATH")
    reason = "UVAD_PATH has not been found. Impossible to run these tests"

    def setUp(self):
        if not self.skip:
            self.path_database = os.environ['UVAD_PATH']

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: UvadDatabase('wrong_path')
                          )

    @unittest.skipIf(skip, reason)
    def test_name_property(self):
        database = UvadDatabase(self.path_database)
        self.assertEqual(database.name, 'uvad')

    @unittest.skipIf(skip, reason)
    def test_get_ground_truth_protocol_grandtest(self):
        database = UvadDatabase(self.path_database)
        dict_ground_truth = database.get_ground_truth('protocol_1')

        self.assertEquals(len(dict_ground_truth['Train']), 2768)
        self.assertEquals(len(dict_ground_truth['Test']), 2476)

    @unittest.skipIf(skip, reason)
    def test_get_all_accesses(self):
        database = UvadDatabase(self.path_database)
        dict_all_accesses = database.get_all_accesses()

        self.assertEqual(len(dict_all_accesses['Train']), 2768)
        self.assertEqual(len(dict_all_accesses['Test']), 2476)

    @unittest.skipIf(skip, reason)
    def test_load_database_image(self):
        database = UvadDatabase(self.path_database)
        dict_all_accesses = database.get_all_accesses()
        access = dict_all_accesses['Train'][6]  # Random example
        full_path = os.path.join(access.base_path, access.name) + access.extension
        self.assertTrue(os.path.isfile(full_path))
