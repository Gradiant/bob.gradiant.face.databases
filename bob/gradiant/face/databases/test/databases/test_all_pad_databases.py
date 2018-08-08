#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import os
from bob.gradiant.face.databases import AllPadDatabases
from bob.gradiant.core import DatabasesPathChecker


class UnitTestAllPadDatabases(unittest.TestCase):
    skip = not DatabasesPathChecker.check_if_environment_is_defined_for("REPLAY_ATTACK_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("REPLAY_MOBILE_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("MSU_MFSD_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("OULU_NPU_PATH") and \
           not DatabasesPathChecker.check_if_environment_is_defined_for("UVAD_PATH")
    reason = "REPLAY_ATTACK_PATH, REPLAY_MOBILE_PATH, MSU_MFSD_PATH, OULU_NPU_PATH and UVAD_PATH have not been found. Impossible to run these tests"

    def setUp(self):
        if not self.skip:
            self.base_paths = {'replay-attack': os.environ['REPLAY_ATTACK_PATH'],
                               'replay-mobile': os.environ['REPLAY_MOBILE_PATH'],
                               'msu-mfsd': os.environ['MSU_MFSD_PATH'],
                               'oulu-npu': os.environ['OULU_NPU_PATH'],
                               'uvad': os.environ['UVAD_PATH']
                               }

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: AllPadDatabases('wrong_path')
                          )

    def test_name_static_method(self):
        self.assertEqual(AllPadDatabases.name(), 'all-pad-databases')

    def test_is_a_collection_of_databases_static_method(self):
        self.assertTrue(AllPadDatabases.is_a_collection_of_databases())

    @unittest.skipIf(skip, reason)
    def test_get_ground_truth_protocol_grandtest(self):
        database = AllPadDatabases(self.base_paths)
        dict_ground_truth = database.get_ground_truth('grandtest')

        self.assertEqual(len(dict_ground_truth['Train']), 2552)
        self.assertEqual(len(dict_ground_truth['Dev']), 2206)
        self.assertEqual(len(dict_ground_truth['Test']), 2702)

    @unittest.skipIf(skip, reason)
    def test_get_all_accesses(self):
        database = AllPadDatabases(self.base_paths)
        dict_all_accesses = database.get_all_accesses()

        self.assertEqual(len(dict_all_accesses['All']), 2552 + 2206 + 2702)


