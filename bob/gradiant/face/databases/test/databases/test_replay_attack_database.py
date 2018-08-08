#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import unittest

from bob.gradiant.face.databases import ReplayAttackDatabase
from bob.gradiant.core import DatabasesPathChecker


class UnitTestReplayAttackDatabase(unittest.TestCase):
    skip = not DatabasesPathChecker.check_if_environment_is_defined_for("REPLAY_ATTACK_PATH")
    reason = "REPLAY_ATTACK_PATH has not been found. Impossible to run these tests"

    def setUp(self):
        if not self.skip:
            self.path_database = os.environ['REPLAY_ATTACK_PATH']

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: ReplayAttackDatabase('wrong_path')
                          )

    def test_name_static_method(self):
        self.assertEqual(ReplayAttackDatabase.name(), 'replay-attack')

    def test_is_a_collection_of_databases_static_method(self):
        self.assertFalse(ReplayAttackDatabase.is_a_collection_of_databases())

    @unittest.skipIf(skip, reason)
    def test_get_ground_truth_protocol_grandtest(self):
        database = ReplayAttackDatabase(self.path_database)
        dict_ground_truth = database.get_ground_truth('grandtest')

        self.assertEqual(len(dict_ground_truth['Train']), 360)
        self.assertEqual(len(dict_ground_truth['Dev']), 360)
        self.assertEqual(len(dict_ground_truth['Test']), 480)

    @unittest.skipIf(skip, reason)
    def test_get_all_accesses(self):
        database = ReplayAttackDatabase(self.path_database)
        dict_all_accesses = database.get_all_accesses()

        self.assertEqual(len(dict_all_accesses['Train']), 360)
        self.assertEqual(len(dict_all_accesses['Dev']), 360)
        self.assertEqual(len(dict_all_accesses['Test']), 480)

    @unittest.skipIf(skip, reason)
    def test_get_enrolment_accesses(self):
        database = ReplayAttackDatabase(self.path_database)
        list_enrolment_accesses = database.get_enrolment_access()

        self.assertEqual(len(list_enrolment_accesses), 100)
