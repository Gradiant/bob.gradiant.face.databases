#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import unittest

from bob.gradiant.face.databases import OuluNpuDatabase
from bob.gradiant.core import DatabasesPathChecker


class UnitTestOuluNpuDatabase(unittest.TestCase):
    skip = not DatabasesPathChecker.check_if_environment_is_defined_for("OULU_NPU_PATH")
    reason = "OULU_NPU_PATH has not been found. Impossible to run these tests"

    def setUp(self):
        if not self.skip:
            self.path_database = os.environ['OULU_NPU_PATH']

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: OuluNpuDatabase('wrong_path')
                          )

    def test_name_static_method(self):
        self.assertEqual(OuluNpuDatabase.name(), 'oulu-npu')

    def test_is_a_collection_of_databases_static_method(self):
        self.assertFalse(OuluNpuDatabase.is_a_collection_of_databases())

    @unittest.skipIf(skip, reason)
    def test_get_ground_truth_protocol_1(self):
        database = OuluNpuDatabase(self.path_database)
        dict_ground_truth = database.get_ground_truth('Protocol_1')

        self.assertEqual(len(dict_ground_truth['Train']),1200)
        self.assertEqual(len(dict_ground_truth['Dev']), 900)
        self.assertEqual(len(dict_ground_truth['Test']), 600)

    @unittest.skipIf(skip, reason)
    def test_get_ground_truth_protocol_2(self):
        database = OuluNpuDatabase(self.path_database)
        dict_ground_truth = database.get_ground_truth('Protocol_2')

        self.assertEqual(len(dict_ground_truth['Train']), 1080)
        self.assertEqual(len(dict_ground_truth['Dev']), 810)
        self.assertEqual(len(dict_ground_truth['Test']), 1080)

    @unittest.skipIf(skip, reason)
    def test_get_ground_truth_protocol_3(self):
        database = OuluNpuDatabase(self.path_database)

        for i in range(6):
            protocol_tag = 'Protocol_3_'+str(i+1)

            dict_ground_truth = database.get_ground_truth(protocol_tag)

            self.assertEqual(len(dict_ground_truth['Train']), 1500)
            self.assertEqual(len(dict_ground_truth['Dev']), 1125)
            self.assertEqual(len(dict_ground_truth['Test']), 300)

    @unittest.skipIf(skip, reason)
    def test_get_ground_truth_protocol_4(self):
        database = OuluNpuDatabase(self.path_database)

        for i in range(6):
            protocol_tag = 'Protocol_4_'+str(i+1)
            dict_ground_truth = database.get_ground_truth(protocol_tag)
            self.assertEqual(len(dict_ground_truth['Train']), 600)
            self.assertEqual(len(dict_ground_truth['Dev']), 450)
            self.assertEqual(len(dict_ground_truth['Test']), 60)

    @unittest.skipIf(skip, reason)
    def test_get_ground_truth_protocol_4_no_loco(self):
        database = OuluNpuDatabase(self.path_database)
        dict_ground_truth = database.get_ground_truth('Protocol_4_no_loco')

        self.assertEqual(len(dict_ground_truth['Train']), 720)
        self.assertEqual(len(dict_ground_truth['Dev']), 540)
        self.assertEqual(len(dict_ground_truth['Test']), 360)

    @unittest.skipIf(skip, reason)
    def test_get_ground_truth_protocol_grandtest(self):
        database = OuluNpuDatabase(self.path_database)
        dict_ground_truth = database.get_ground_truth('grandtest')

        self.assertEqual(len(dict_ground_truth['Train']), 1800)
        self.assertEqual(len(dict_ground_truth['Dev']), 1350)
        self.assertEqual(len(dict_ground_truth['Test']), 1800)

    @unittest.skipIf(skip, reason)
    def test_get_all_accesses(self):
        database = OuluNpuDatabase(self.path_database)
        dict_all_accesses = database.get_all_accesses()

        self.assertEqual(len(dict_all_accesses['All']), 1800 + 1350 + 1800)

