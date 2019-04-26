#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import os
import warnings
from bob.gradiant.core import Database, AccessModifier, FolderAccess
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat

CSMAD_PROTOCOLS = ['grandtest']
CSMAD_SUBSETS = ['Train', 'Dev', 'Test']
CSMAD_PAIS = {'real': 0,
              'mask': 1}

CSMAD_PAIS_CORRESPONDENCE = {'gen': CSMAD_PAIS['real'],
                             'genglasses': CSMAD_PAIS['real'],
                             'atk': CSMAD_PAIS['mask']}

CSMAD_COMMON_PAIS = {'gen': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                     'genglasses': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                     'atk': inter_db_cat.COMMON_PAI_CATEGORISATION['mask']['silicone']}

CSMAD_CAPTURE_DEVICES = {'intel_realsense_sr300': 0}  # 1080p

CSMAD_COMMON_CAPTURE_DEVICES = {
    'intel_realsense_sr300': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['high_quality']}

CSMAD_COMMON_LIGHTNING = {'i0': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled'],
                          # flourescent ceiling light only
                          'i1': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['adverse'],
                          # halogen lamp illuminating from the left of the subject only
                          'i2': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['adverse'],
                          # halogen lamp illuminating from the right only
                          'i3': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION[
                              'controlled'], }  # both halogen lamps illuminating from both sides simultaneously

CSMAD_USERS_PER_SUBSET = {'Train': ['B', 'C', 'J', 'K', 'L'],
                          'Dev': ['A', 'D', 'G', 'H', 'I'],
                          'Test': ['E', 'F', 'M', 'N']}


class CsmadDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.dict_all_accesses = {}
        self.dict_all_labels = {}
        super(CsmadDatabase, self).__init__(base_path, annotation_base_path=annotation_base_path)

    def __str__(self):
        return super(CsmadDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'csmad'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = {'users': 14,
                     'Train videos': 93,
                     'Dev videos': 80,
                     'Test videos': 73}
        return dict_info

    @staticmethod
    def get_protocols():
        return CSMAD_PROTOCOLS

    @staticmethod
    def get_subsets():
        return CSMAD_SUBSETS

    @staticmethod
    def get_capture_devices():
        return CSMAD_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in CSMAD_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        if not self.dict_all_accesses:
            self.dict_all_accesses = {'Train': [],
                                      'Dev': [],
                                      'Test': []}

            for root, dirs, files in os.walk(self.base_path):
                if not dirs:
                    if sum([f.endswith('.jpg') for f in files]):
                        split_path = os.path.normpath(root).split(os.path.sep)
                        relative_path = os.path.relpath(root, self.base_path)
                        user = split_path[-2]

                        for subset, list_users in CSMAD_USERS_PER_SUBSET.items():
                            if user in list_users:
                                self.dict_all_accesses[subset].append(
                                    FolderAccess(self.base_path, relative_path, '.jpg',
                                                 access_modifier=access_modifier,
                                                 annotation_base_path=self.annotation_base_path,
                                                 database_name=CsmadDatabase.name()
                                                 )
                                )
            for subset, list_accesses in self.dict_all_accesses .items():
                list_accesses.sort(key=lambda x: x.name)

        return self.dict_all_accesses

    def get_all_labels(self):
        if not self.dict_all_labels:
            try:
                dict_all_labels_aggregate_db = TestResources.get_aggregated_database_all_dict_labels()
                for subset in dict_all_labels_aggregate_db:
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][CsmadDatabase.name()]

            except IOError:
                warnings.warn("WARNING (CsmadDatabase.get_all_labels): Labels resource file "
                              "[resources/aggregate_database_all_labels.pickle] not found. "
                              "Extracting all labels from scratch may take a while.")
                self.dict_all_labels = self._extract_all_labels_from_scratch()

        return self.dict_all_labels

    def _extract_all_labels_from_scratch(self):
        dict_all_labels = {'Train': {},
                           'Dev': {},
                           'Test': {}}

        dict_all_accesses = self.get_all_accesses()

        for subset, list_accesses in dict_all_accesses.items():
            for access in list_accesses:
                basename = os.path.basename(access.name)
                split_labels = basename.split('_')
                user = split_labels[2]
                lightning = split_labels[-2]

                dict_all_labels[subset][access.name] = {
                    'pai': CSMAD_PAIS_CORRESPONDENCE[split_labels[1]],
                    'capture_device': CSMAD_CAPTURE_DEVICES['intel_realsense_sr300'],
                    'scenario': CSMAD_PAIS_CORRESPONDENCE[split_labels[1]],
                    'user': user,
                    'common_pai': CSMAD_COMMON_PAIS[split_labels[1]],
                    'common_capture_device': CSMAD_COMMON_CAPTURE_DEVICES['intel_realsense_sr300'],
                    'common_lightning': CSMAD_COMMON_LIGHTNING[lightning],
                    'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(access.base_path,
                                                                                                   access.name)),
                    }
        return dict_all_labels

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in CSMAD_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in CSMAD protocols [{}]'.format(protocol, CSMAD_PROTOCOLS))

        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict
