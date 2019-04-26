#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import os
import warnings
from bob.gradiant.core import Database, AccessModifier, VideoAccess
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat

CASIA_FASD_PROTOCOLS = ['grandtest']
CASIA_FASD_SUBSETS = ['Train', 'Dev', 'Test']
CASIA_FASD_PAIS = {'real': 0,
                   'print': 1,   # A4 copper paper
                   'replay': 2,  # iPad
                   'mask': 3}    # paper mask

CASIA_FASD_PAIS_CORRESPONDENCE = {'1': CASIA_FASD_PAIS['real'],
                                  '2': CASIA_FASD_PAIS['real'],
                                  '3': CASIA_FASD_PAIS['print'],
                                  '4': CASIA_FASD_PAIS['print'],
                                  '5': CASIA_FASD_PAIS['mask'],
                                  '6': CASIA_FASD_PAIS['mask'],
                                  '7': CASIA_FASD_PAIS['replay'],
                                  '8': CASIA_FASD_PAIS['replay'],
                                  'HR_1': CASIA_FASD_PAIS['real'],
                                  'HR_2': CASIA_FASD_PAIS['print'],
                                  'HR_3': CASIA_FASD_PAIS['mask'],
                                  'HR_4': CASIA_FASD_PAIS['replay']}

CASIA_FASD_COMMON_PAIS = {'1': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                          '2': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                          '3': inter_db_cat.COMMON_PAI_CATEGORISATION['print']['medium_quality'],
                          '4': inter_db_cat.COMMON_PAI_CATEGORISATION['print']['medium_quality'],
                          '5': inter_db_cat.COMMON_PAI_CATEGORISATION['mask']['paper'],
                          '6': inter_db_cat.COMMON_PAI_CATEGORISATION['mask']['paper'],
                          '7': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['medium_quality'],
                          '8': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['medium_quality'],
                          'HR_1': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                          'HR_2': inter_db_cat.COMMON_PAI_CATEGORISATION['print']['medium_quality'],
                          'HR_3': inter_db_cat.COMMON_PAI_CATEGORISATION['mask']['paper'],
                          'HR_4': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['medium_quality']}

CASIA_FASD_CAPTURE_DEVICES = {'usb_camera_1': 0,  # usb_camera_1 (640x480)
                              'usb_camera_2': 1,  # usb_camera_2 (480x640)
                              'sony_nex_5': 2}    # Sony NEX-5 (1280x720)

CASIA_FASD_CAPTURE_DEVICES_CORRESPONDENCE = {'1': CASIA_FASD_CAPTURE_DEVICES['usb_camera_1'],
                                             '2': CASIA_FASD_CAPTURE_DEVICES['usb_camera_2'],
                                             '3': CASIA_FASD_CAPTURE_DEVICES['usb_camera_1'],
                                             '4': CASIA_FASD_CAPTURE_DEVICES['usb_camera_2'],
                                             '5': CASIA_FASD_CAPTURE_DEVICES['usb_camera_1'],
                                             '6': CASIA_FASD_CAPTURE_DEVICES['usb_camera_2'],
                                             '7': CASIA_FASD_CAPTURE_DEVICES['usb_camera_1'],
                                             '8': CASIA_FASD_CAPTURE_DEVICES['usb_camera_2'],
                                             'HR_1': CASIA_FASD_CAPTURE_DEVICES['sony_nex_5'],
                                             'HR_2': CASIA_FASD_CAPTURE_DEVICES['sony_nex_5'],
                                             'HR_3': CASIA_FASD_CAPTURE_DEVICES['sony_nex_5'],
                                             'HR_4': CASIA_FASD_CAPTURE_DEVICES['sony_nex_5']
                                             }

CASIA_FASD_COMMON_CAPTURE_DEVICES = {'1': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality'],
                                     '2': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality'],
                                     '3': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality'],
                                     '4': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality'],
                                     '5': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality'],
                                     '6': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality'],
                                     '7': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality'],
                                     '8': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality'],
                                     'HR_1': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['digital_camera']['high_quality'],
                                     'HR_2': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['digital_camera']['high_quality'],
                                     'HR_3': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['digital_camera']['high_quality'],
                                     'HR_4': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['digital_camera']['high_quality']
                                     }


CASIA_FASD_DEV_USERS = [17, 18, 19, 20]


class CasiaFasdDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.dict_all_accesses = {}
        self.dict_all_labels = {}
        super(CasiaFasdDatabase, self).__init__(base_path, annotation_base_path=annotation_base_path)

    def __str__(self):
        return super(CasiaFasdDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'casia-fasd'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = {'users': 50,
                     'Train videos': 192,
                     'Dev videos': 48,
                     'Test videos': 360}
        return dict_info

    @staticmethod
    def get_protocols():
        return CASIA_FASD_PROTOCOLS

    @staticmethod
    def get_subsets():
        return CASIA_FASD_SUBSETS

    @staticmethod
    def get_capture_devices():
        return CASIA_FASD_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in CASIA_FASD_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        if not self.dict_all_accesses:

            self.dict_all_accesses = {'Train': [],
                                      'Dev': [],
                                      'Test': []}

            for root, dirs, files in os.walk(self.base_path):
                if not dirs:
                    for f in files:
                        if f.lower().endswith('.avi'):
                            basename, extension = os.path.splitext(f)
                            split_path = os.path.normpath(root).split(os.path.sep)
                            subject = int(split_path[-1])
                            if split_path[-2].startswith('train_'):
                                if subject in CASIA_FASD_DEV_USERS:
                                    subset = 'Dev'
                                else:
                                    subset = 'Train'
                            else:
                                subset = 'Test'

                            self.dict_all_accesses[subset].append(
                                VideoAccess(self.base_path, os.path.join(split_path[-2], split_path[-1], basename),
                                            extension, access_modifier=access_modifier,
                                            annotation_base_path=self.annotation_base_path,
                                            database_name=CasiaFasdDatabase.name()
                                            ))

            for subset, list_accesses in self.dict_all_accesses.items():
                list_accesses.sort(key=lambda x: x.name)

        return self.dict_all_accesses

    def get_all_labels(self):
        if not self.dict_all_labels:
            try:
                dict_all_labels_aggregate_db = TestResources.get_aggregated_database_all_dict_labels()
                for subset in dict_all_labels_aggregate_db:
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][CasiaFasdDatabase.name()]

            except IOError:
                warnings.warn("WARNING (CasiaFasdDatabase.get_all_labels): Labels resource file "
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
                subject = int(os.path.basename(os.path.dirname(access.name)))

                dict_all_labels[subset][access.name] = {
                    'pai': CASIA_FASD_PAIS_CORRESPONDENCE[basename],
                    'capture_device': CASIA_FASD_CAPTURE_DEVICES_CORRESPONDENCE[basename],
                    'scenario': CASIA_FASD_PAIS_CORRESPONDENCE[basename],
                    'user': subject - 1,
                    'common_pai': CASIA_FASD_COMMON_PAIS[basename],
                    'common_capture_device': CASIA_FASD_COMMON_CAPTURE_DEVICES[basename],
                    'common_lightning': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled'],
                    'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(access.base_path,
                                                                                                   access.name)),
                }
        return dict_all_labels

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in CASIA_FASD_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in CASIA_FASD protocols [{}]'
                             .format(protocol, CASIA_FASD_PROTOCOLS))

        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict


