#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest

from bob.gradiant.face.databases import DummyDatabase


class UnitTestDummyDatabase(unittest.TestCase):

    def setUp(self):
        self.database = DummyDatabase(".")

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: DummyDatabase('wrong_path')
                          )

    def test_name_static_method(self):
        self.assertEqual(DummyDatabase.name(), 'dummy-database')

    def test_is_a_collection_of_databases_static_method(self):
        self.assertFalse(DummyDatabase.is_a_collection_of_databases())

    def test_get_all_accesses(self):
        dict_all_accesses = self.database.get_all_accesses()

        self.assertEqual(len(dict_all_accesses['Train']), 10)
        self.assertEqual(len(dict_all_accesses['Dev']), 10)
        self.assertEqual(len(dict_all_accesses['Test']), 10)

    def test_get_all_labels(self):
        dict_all_labels = self.database.get_all_labels()

        self.assertEqual(len(dict_all_labels['Train']), 10)
        self.assertEqual(len(dict_all_labels['Dev']), 10)
        self.assertEqual(len(dict_all_labels['Test']), 10)

    def test_get_ground_truth_protocol_grandtest(self):
        dict_ground_truth = self.database.get_ground_truth('grandtest')

        self.assertEqual(len(dict_ground_truth['Train']), 10)
        self.assertEqual(len(dict_ground_truth['Dev']), 10)
        self.assertEqual(len(dict_ground_truth['Test']), 10)
