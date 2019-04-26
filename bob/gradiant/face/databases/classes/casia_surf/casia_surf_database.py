#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import os
import warnings
from bob.gradiant.core import Database, AccessModifier, FolderAccess
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat
from bob.gradiant.face.databases.classes.casia_surf.casia_subsets_splits import CASIA_DEV_USERS, CASIA_TEST_USERS
CASIA_SURF_PROTOCOLS = ['grandtest', 'intra_testing']
CASIA_SURF_SUBSETS = ['Train', 'Dev', 'Test']
CASIA_SURF_PAIS = {'real': 0,
                   'mask': 1}    # paper mask

CASIA_SURF_PAIS_CORRESPONDENCE = {'real_part': CASIA_SURF_PAIS['real'],
                                  'fake_part': CASIA_SURF_PAIS['mask']}

CASIA_SURF_COMMON_PAIS = {'real_part': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                          'fake_part': inter_db_cat.COMMON_PAI_CATEGORISATION['mask']['paper']}

CASIA_SURF_CAPTURE_DEVICES = {'intel_realsense_sr300': 0}  # Intel RealSense SR300 (1280x720)

CASIA_SURF_COMMON_CAPTURE_DEVICES = {'intel_realsense_sr300': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality']}


class CasiaSurfDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.dict_all_accesses = {}
        self.dict_all_labels = {}
        super(CasiaSurfDatabase, self).__init__(base_path, annotation_base_path=annotation_base_path)

    def __str__(self):
        return super(CasiaSurfDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'casia-surf'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = {'users': 300,
                     'Train videos': 480,
                     'Dev videos': 120,
                     'Test videos': 600}
        return dict_info

    @staticmethod
    def get_protocols():
        return CASIA_SURF_PROTOCOLS

    @staticmethod
    def get_subsets():
        return CASIA_SURF_SUBSETS

    @staticmethod
    def get_capture_devices():
        return CASIA_SURF_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in CASIA_SURF_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        if not self.dict_all_accesses:

            self.dict_all_accesses = {'Train': [],
                                      'Dev': [],
                                      'Test': []}

            for root, dirs, files in os.walk(self.base_path):
                if not dirs:
                    if sum([f.endswith('.jpg') for f in files]):
                        relative_path = os.path.relpath(root, self.base_path)
                        split_path = os.path.normpath(relative_path).split(os.path.sep)

                        # Until March 10th, only Train set is available
                        if split_path[0] == 'Training' and split_path[-1] == 'color':
                            depth_relative_path = relative_path.replace('color', 'depth')
                            ir_relative_path = relative_path.replace('color', 'ir')
                            user = split_path[-3]

                            if user in CASIA_DEV_USERS:
                                subset = 'Dev'
                            elif user in CASIA_TEST_USERS :
                                subset = 'Test'
                            else:
                              subset = 'Train'

                            self.dict_all_accesses[subset].append(
                                FolderAccess(self.base_path, relative_path, '.jpg',
                                             depth_name=depth_relative_path,
                                             infrared_name=ir_relative_path,
                                             access_modifier=access_modifier,
                                             annotation_base_path=self.annotation_base_path,
                                             database_name=CasiaSurfDatabase.name()
                                             ))
            # subset = 'Test'
            # orig_dev_list = [line.rstrip() for line in open(os.path.join(self.base_path,
            #                                                              'val_public_list.txt'))]
            # for line in orig_dev_list:
            #     color_relative_path, depth_relative_path, ir_relative_path = line.split(' ')

            #     self.dict_all_accesses[subset].append(
            #         FolderAccess(self.base_path, color_relative_path, '.jpg',
            #                      depth_name=depth_relative_path,
            #                      infrared_name=ir_relative_path,
            #                      access_modifier=access_modifier,
            #                      annotation_base_path=self.annotation_base_path,
            #                      database_name=CasiaSurfDatabase.name()
            #                      ))

            for subset, list_accesses in self.dict_all_accesses.items():
                list_accesses.sort(key=lambda x: x.name)

        return self.dict_all_accesses

    def get_all_labels(self):
        if not self.dict_all_labels:
            try:
                dict_all_labels_aggregate_db = TestResources.get_aggregated_database_all_dict_labels()
                for subset in dict_all_labels_aggregate_db:
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][CasiaSurfDatabase.name()]

            except IOError:
                warnings.warn("WARNING (CasiaSurfDatabase.get_all_labels): Labels resource file "
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
                relative_path = access.name
                split_path = os.path.normpath(relative_path).split(os.path.sep)
                pai = split_path[1]
                user = split_path[2]

                dict_all_labels[subset][access.name] = {
                    'pai': CASIA_SURF_PAIS_CORRESPONDENCE[pai],
                    'capture_device': CASIA_SURF_CAPTURE_DEVICES['intel_realsense_sr300'],
                    'scenario': CASIA_SURF_PAIS_CORRESPONDENCE[pai],
                    'user': user,
                    'common_pai': CASIA_SURF_COMMON_PAIS[pai],
                    'common_capture_device': CASIA_SURF_COMMON_CAPTURE_DEVICES['intel_realsense_sr300'],
                    'common_lightning': 2,  # no info
                    'common_face_resolution': 0,  # small faces
                    }
        return dict_all_labels

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in CASIA_SURF_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in CASIA_FASD protocols [{}]'
                             .format(protocol, CASIA_SURF_PROTOCOLS))

        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict


