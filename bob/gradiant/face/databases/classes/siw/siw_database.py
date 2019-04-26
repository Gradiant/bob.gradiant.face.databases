#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
import warnings
from bob.gradiant.core import Database, AccessModifier, VideoAccess
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat

SIW_PROTOCOLS = ['protocol_1']
SIW_SUBSETS = ['Train', 'Dev', 'Test']
SIW_PAIS = {'real': 0,
            'print': 1,
            'replay': 2}

SIW_PAI_CORRESPONDENCE = {'1': SIW_PAIS['real'],
                          '2': SIW_PAIS['print'],
                          '3': SIW_PAIS['replay']}

SIW_CAPTURE_DEVICES = {'canon_eos_t6': 0,
                       'logitech_c920_webcam': 1}

SIW_COMMON_CAPTURE_DEVICES = {'1': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['digital_camera']['high_quality'],
                              '2': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['high_quality']}

SIW_CAPTURE_DEVICE_CORRESPONDENCE = {'1': SIW_CAPTURE_DEVICES['canon_eos_t6'],
                                     '2': SIW_CAPTURE_DEVICES['logitech_c920_webcam']}

SIW_USERS_PER_SUBSET = {'Train': range(1, 166),
                        'Dev': [150, 151, 152, 155, 156, 157, 159, 160, 162, 163, 164, 165],
                        'Test': range(1, 166)}


class SiwDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.dict_all_accesses = {}
        self.dict_all_labels = {}
        super(SiwDatabase, self).__init__(base_path, annotation_base_path=annotation_base_path)

    def __str__(self):
        return super(SiwDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'siw'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = {'users': 165,
                     'Train videos': 2145,
                     'Dev videos': 272,
                     'Test videos': 2061}
        return dict_info

    @staticmethod
    def get_protocols():
        return SIW_PROTOCOLS

    @staticmethod
    def get_subsets():
        return SIW_SUBSETS

    @staticmethod
    def get_capture_devices():
        return SIW_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in SIW_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        if not self.dict_all_accesses:
            self.dict_all_accesses = {'Train': [],
                                      'Dev': [],
                                      'Test': []}

            for root, dirs, files in os.walk(self.base_path):
                if not dirs:
                    for f in files:
                        if f.lower().endswith(('.mov', '.mp4')):
                            basename, extension = os.path.splitext(f)
                            split_path = os.path.normpath(root).split(os.path.sep)
                            relative_path = os.path.join(*split_path[-3:])
                            subject = int(basename.split('-')[0])
                            original_subset = split_path[-3]

                            if original_subset == 'Train' and subject in SIW_USERS_PER_SUBSET['Dev']:
                                subset = 'Dev'
                            else:
                                subset = original_subset

                            self.dict_all_accesses[subset].append(
                                VideoAccess(self.base_path,
                                            os.path.join(relative_path, basename),
                                            extension,
                                            access_modifier=access_modifier,
                                            annotation_base_path=self.annotation_base_path,
                                            database_name=SiwDatabase.name()))

            for subset, list_accesses in self.dict_all_accesses.items():
                list_accesses.sort(key=lambda x: x.name)

        return self.dict_all_accesses

    def get_all_labels(self):
        if not self.dict_all_labels:
            try:
                dict_all_labels_aggregate_db = TestResources.get_aggregated_database_all_dict_labels()
                for subset in dict_all_labels_aggregate_db:
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][SiwDatabase.name()]

            except IOError:
                warnings.warn("WARNING (SiwDatabase.get_all_labels): Labels resource file "
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
                subject, sensor, type, medium, session = basename.split('-')

                dict_all_labels[subset][access.name] = {
                    'pai': SIW_PAI_CORRESPONDENCE[type],
                    'scenario': self.__get_scenario(type, medium, session),
                    'capture_device': SIW_CAPTURE_DEVICE_CORRESPONDENCE[sensor],
                    'user': int(subject) - 1,
                    'medium': int(medium),
                    'common_pai': self.__get_common_pai(type, medium, session),
                    'common_capture_device': SIW_COMMON_CAPTURE_DEVICES[sensor],
                    'common_lightning': self.__get_common_lightning(type, medium),
                    'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(access.base_path,
                                                                                                   access.name))
                    }
        return dict_all_labels

    @staticmethod
    def __get_common_pai(type, medium, session):
        common_pai = -1

        if type == '1':    # real
            common_pai = inter_db_cat.COMMON_PAI_CATEGORISATION['real']

        elif type == '2':  # print
            if session == '1':  # Glossy paper
                common_pai = inter_db_cat.COMMON_PAI_CATEGORISATION['print']['high_quality']
            elif session == '2':  # Matt paper
                common_pai = inter_db_cat.COMMON_PAI_CATEGORISATION['print']['medium_quality']

        elif type == '3':  # replay
            if medium == '1':    # iPad Pro (12.9", 2732x2048)
                common_pai = inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['high_quality']

            elif medium == '2':  # iPhone7 Plus (5.5", 1920x1080)
                common_pai = inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['high_quality']

            elif medium == '3':  # Samsung Galaxy S8 (5.8", 2960x144)
                common_pai = inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['high_quality']

            elif medium == '4':  # Asus MB168B (15.6", 1366x768)
                common_pai = inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['medium_quality']

        return common_pai

    @staticmethod
    def __get_scenario(type, medium, session):
        if type == '1':
            if medium == '1':
                if session == '1':
                    scenario = 0
                else:
                    scenario = 1
            else:
                if session == '1':
                    scenario = 2
                else:
                    scenario = 3

        elif type == '2':
            if medium == '1':
                if session == '1':
                    scenario = 4
                else:
                    scenario = 5
            else:
                if session == '1':
                    scenario = 6
                else:
                    scenario = 7

        elif type == '3':
            if medium == '1':
                scenario = 8

            elif medium == '2':
                scenario = 9

            elif medium == '3':
                scenario = 10

            elif medium == '4':
                scenario = 11

            else:
                scenario = None
        else:
            scenario = None

        return scenario

    @staticmethod
    def __get_common_lightning(type, medium):

        if type == '1':    # real
            if medium == '1':
                common_lightning = inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled']
            else:
                common_lightning = inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['adverse']

        else:
            common_lightning = inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['no_info']

        return common_lightning

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in SIW_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in SIW protocols [{}]'.format(protocol, SIW_PROTOCOLS))

        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict
