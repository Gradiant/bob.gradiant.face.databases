#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
import warnings
from bob.gradiant.core import Database, AccessModifier, VideoAccess
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat

HKBU_PROTOCOLS = ['grandtest']
HKBU_SUBSETS = ['Train', 'Dev', 'Test']
HKBU_PAIS = {'real': 0,
             'mask': 1}

HKBU_SUBJECTS_PER_SUBSET = {'Train': [1, 2, 3],
                            'Dev': [4, 5, 8],
                            'Test': [6, 7]}

HKBU_CAPTURE_DEVICES = {'logitech_c920': 0}
HKBU_COMMON_CAPTURE_DEVICES = {'logitech_c920': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['high_quality']}


class HkbuDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.dict_all_accesses = {}
        self.dict_all_labels = {}
        super(HkbuDatabase, self).__init__(base_path, annotation_base_path=annotation_base_path)

    def __str__(self):
        return super(HkbuDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'hkbu'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = {'users': 8,
                     'Train videos': 45,
                     'Dev videos': 35,
                     'Test videos': 30}
        return dict_info

    @staticmethod
    def get_protocols():
        return HKBU_PROTOCOLS

    @staticmethod
    def get_subsets():
        return HKBU_SUBSETS

    @staticmethod
    def get_capture_devices():
        return HKBU_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in HKBU_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        if not self.dict_all_accesses:
            self.dict_all_accesses = {'Train': [],
                                      'Dev': [],
                                      'Test': []}

            for root, dirs, files in os.walk(self.base_path):
                if not dirs:
                    for f in files:
                        if f.lower().endswith('.mp4'):
                            basename, extension = os.path.splitext(f)
                            subject = int(basename.split('_')[0])

                            relative_path = os.path.join(os.path.relpath(root, self.base_path), basename)

                            for subset, list_users in HKBU_SUBJECTS_PER_SUBSET.items():
                                if subject in list_users:
                                    self.dict_all_accesses[subset].append(
                                        VideoAccess(self.base_path, relative_path, extension,
                                                    access_modifier=access_modifier,
                                                    annotation_base_path=self.annotation_base_path,
                                                    database_name=HkbuDatabase.name()
                                                    )
                                    )
            for subset, list_accesses in self.dict_all_accesses.items():
                list_accesses.sort(key=lambda x: x.name)

        return self.dict_all_accesses

    def get_all_labels(self):
        if not self.dict_all_labels:
            try:
                dict_all_labels_aggregate_db = TestResources.get_aggregated_database_all_dict_labels()
                for subset in dict_all_labels_aggregate_db:
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][HkbuDatabase.name()]

            except IOError:
                warnings.warn("WARNING (HkbuDatabase.get_all_labels): Labels resource file "
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
                subject = int(split_labels[0])
                session = int(split_labels[1])
                if session == 3:
                    pai = HKBU_PAIS['mask']
                    common_pai = inter_db_cat.COMMON_PAI_CATEGORISATION['mask']['rigid']
                else:
                    pai = HKBU_PAIS['real']
                    common_pai = inter_db_cat.COMMON_PAI_CATEGORISATION['real']

                dict_all_labels[subset][access.name] = {
                    'pai': pai,
                    'capture_device': HKBU_CAPTURE_DEVICES['logitech_c920'],
                    'scenario': pai,
                    'user': subject - 1,
                    'session': session - 1,
                    'common_pai': common_pai,
                    'common_capture_device': HKBU_COMMON_CAPTURE_DEVICES['logitech_c920'],
                    'common_lightning': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled'],
                    'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(access.base_path,
                                                                                                   access.name))
                    }
        return dict_all_labels

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in HKBU_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in HKBU protocols [{}]'.format(protocol, HKBU_PROTOCOLS))

        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict
