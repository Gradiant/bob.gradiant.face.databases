#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
import warnings
from bob.gradiant.core import Database, AccessModifier, VideoAccess
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat

ROSE_YOUTU_PROTOCOLS = ['grandtest']
ROSE_YOUTU_SUBSETS = ['Train', 'Dev', 'Test']
ROSE_YOUTU_PAIS = {'real': 0,
                   'print': 1,
                   'replay': 2,
                   'mask': 3}

ROSE_YOUTU_SCENARIOS = {'G': 0,   # genuine person.
                        'Ps': 1,  # still printed paper.
                        'Pq': 2,  # quivering printed paper.
                        'Vl': 3,  # video which records a lenovo LCD display.
                        'Vm': 4,  # video which records a Mac LCD display.
                        'Mc': 5,  # paper mask with two eyes and mouth cropped out.
                        'Mf': 6,  # paper mask without cropping.
                        'Mu': 7,  # paper mask with the upper part cut in the middle.
                        'Ml': 8   # paper mask with the lower part cut in the middle.
                        }

ROSE_YOUTU_SCENARIO_PAI_CORRESPONDENCE = {'G': ROSE_YOUTU_PAIS['real'],
                                          'Ps': ROSE_YOUTU_PAIS['print'],
                                          'Pq': ROSE_YOUTU_PAIS['print'],
                                          'Vl': ROSE_YOUTU_PAIS['replay'],
                                          'Vm': ROSE_YOUTU_PAIS['replay'],
                                          'Mc': ROSE_YOUTU_PAIS['mask'],
                                          'Mf': ROSE_YOUTU_PAIS['mask'],
                                          'Mu': ROSE_YOUTU_PAIS['mask'],
                                          'Ml': ROSE_YOUTU_PAIS['mask']}

ROSE_YOUTU_COMMON_PAIS = {'G':  inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                          'Ps': inter_db_cat.COMMON_PAI_CATEGORISATION['print']['low_quality'],
                          'Pq': inter_db_cat.COMMON_PAI_CATEGORISATION['print']['low_quality'],
                          'Vl': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['high_quality'],
                          'Vm': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['high_quality'],
                          'Mc': inter_db_cat.COMMON_PAI_CATEGORISATION['mask']['paper'],
                          'Mf': inter_db_cat.COMMON_PAI_CATEGORISATION['mask']['paper'],
                          'Mu': inter_db_cat.COMMON_PAI_CATEGORISATION['mask']['paper'],
                          'Ml': inter_db_cat.COMMON_PAI_CATEGORISATION['mask']['paper']}


ROSE_YOUTU_CAPTURE_DEVICES = {'HS': 0,  # Hasee smart-phone 640x480
                              'HW': 1,  # Huawei smart-phone 640x480
                              'IP': 2,  # IPad 4 640x480
                              '5s': 3,  # Iphone 5s 1280x720
                              'ZTE': 4}  # ZTE smart-phone 1280x720

ROSE_YOUTU_COMMON_CAPTURE_DEVICES = {'HS': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['low_quality'],
                                     'HW': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['low_quality'],
                                     'IP': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['low_quality'],
                                     '5s': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['high_quality'],
                                     'ZTE': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['high_quality']}

ROSE_YOUTU_GLASSES = {'g': 0,
                      'wg': 1}

ROSE_YOUTU_SPEAKING = {'T': 0,
                       'NT': 1}

ROSE_YOUTU_USERS_PER_SUBSET = {'Train': ['2', '3', '4', '5', '6', '7', '9', '10'],
                               'Dev': ['11', '12'],
                               'Test': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']}


class RoseYoutuDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.dict_all_accesses = {}
        self.dict_all_labels = {}
        super(RoseYoutuDatabase, self).__init__(base_path, annotation_base_path=annotation_base_path)

    def __str__(self):
        return super(RoseYoutuDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'rose-youtu'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = {'users': 20,
                     'Train videos': 1389,
                     'Dev videos': 359,
                     'Test videos': 1749}
        return dict_info

    @staticmethod
    def get_protocols():
        return ROSE_YOUTU_PROTOCOLS

    @staticmethod
    def get_subsets():
        return ROSE_YOUTU_SUBSETS

    @staticmethod
    def get_capture_devices():
        return ROSE_YOUTU_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in ROSE_YOUTU_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        if not self.dict_all_accesses:
            self.dict_all_accesses = {'Train': [],
                                      'Dev': [],
                                      'Test': []}

            for root, dirs, files in os.walk(self.base_path):
                if not dirs:
                    for f in files:
                        basename, extension = os.path.splitext(f)
                        if extension != '.mp4':
                            continue
                        subject = os.path.basename(root)

                        for subset, list_users in ROSE_YOUTU_USERS_PER_SUBSET.items():
                            if subject in list_users:
                                self.dict_all_accesses[subset].append(
                                    VideoAccess(self.base_path, os.path.join(subject, basename), extension,
                                                access_modifier=access_modifier,
                                                annotation_base_path=self.annotation_base_path,
                                                database_name=RoseYoutuDatabase.name()
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
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][RoseYoutuDatabase.name()]

            except IOError:
                warnings.warn("WARNING (RoseYoutuDatabase.get_all_labels): Labels resource file "
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

                dict_all_labels[subset][access.name] = {
                    'pai': ROSE_YOUTU_SCENARIO_PAI_CORRESPONDENCE[split_labels[0]],
                    'scenario': ROSE_YOUTU_SCENARIOS[split_labels[0]],
                    'capture_device': ROSE_YOUTU_CAPTURE_DEVICES[split_labels[2]],
                    'user': int(split_labels[5]) - 2,
                    'speaking': ROSE_YOUTU_SPEAKING[split_labels[1]],
                    'glasses': ROSE_YOUTU_GLASSES[split_labels[3]],
                    'common_pai': ROSE_YOUTU_COMMON_PAIS[split_labels[0]],
                    'common_capture_device': ROSE_YOUTU_COMMON_CAPTURE_DEVICES[split_labels[2]],
                    'common_lightning': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['no_info'],
                    'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(access.base_path,
                                                                                                   access.name))}
        return dict_all_labels

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in ROSE_YOUTU_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in ROSE_YOUTU protocols [{}]'
                             . format(protocol, ROSE_YOUTU_PROTOCOLS))

        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict
