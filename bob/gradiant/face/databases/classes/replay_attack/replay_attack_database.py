#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import os
import warnings
import bob.db.replay
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.core import Database, AccessModifier, VideoAccess, TypeDatabase
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat

REPLAY_PROTOCOLS = ['grandtest']
REPLAY_SUBSETS = ['Train', 'Dev', 'Test']
REPLAY_SUBSETS_CORRESPONDENCE = {'Train': 'train',
                                 'Dev': 'devel',
                                 'Test': 'test'}
REPLAY_PAIS = {'real': 0,
               'print': 1,   # Triumph-Adler DCC 2520 laser
               'replay': 2}  # iPhone 3GS (3.5", 480x320) & iPad (9", 1024x768)

REPLAY_PAI_CORRESPONDENCES = {'real': REPLAY_PAIS['real'],
                              'print': REPLAY_PAIS['print'],        # Triumph-Adler DCC 2520 laser
                              'mobile': REPLAY_PAIS['replay'],      # iPhone 3GS (3.5", 480x320)
                              'highdef': REPLAY_PAIS['replay']}     # iPad (9", 1024x768)

REPLAY_COMMON_PAIS = {'real': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                      'print': inter_db_cat.COMMON_PAI_CATEGORISATION['print']['low_quality'],
                      'mobile': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['low_quality'],
                      'highdef': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['medium_quality']}

REPLAY_CAPTURE_DEVICES = {'macbook': 0}
REPLAY_COMMON_CAPTURE_DEVICES = {'macbook': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality']}

REPLAY_SCENARIOS = {'real': 0,
                    'print_hand_photo': 1,
                    'print_fixed_photo': 2,
                    'mobile_hand_photo': 3,
                    'mobile_fixed_photo': 4,
                    'mobile_hand_video': 5,
                    'mobile_fixed_video': 6,
                    'highdef_hand_photo': 7,
                    'highdef_fixed_photo': 8,
                    'highdef_hand_video': 9,
                    'highdef_fixed_video': 10}

REPLAY_LIGHTS = {'controlled': 0,
                 'adverse': 1}


class ReplayAttackDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        super(ReplayAttackDatabase, self).__init__(base_path, annotation_base_path=annotation_base_path)
        self.db = bob.db.replay.Database(original_directory=base_path)
        self.dict_all_labels = {}

    def __str__(self):
        return super(ReplayAttackDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'replay-attack'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        db = bob.db.replay.Database()
        dict_info = {'users': 50,
                     'Train videos': 360,
                     'Dev videos': 360,
                     'Test videos': 480}
        return dict_info

    @staticmethod
    def get_protocols():
        return REPLAY_PROTOCOLS

    @staticmethod
    def get_subsets():
        return REPLAY_SUBSETS

    @staticmethod
    def get_capture_devices():
        return REPLAY_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in REPLAY_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        dict_all_accesses = {'Train': [],
                             'Dev':  [],
                             'Test':  []}

        for subset, subset_accesses in dict_all_accesses.items():
            objects = self.db.objects(groups=REPLAY_SUBSETS_CORRESPONDENCE[subset])
            for access in objects:
                path, extension = os.path.splitext(access.videofile())
                subset_accesses.append(VideoAccess(self.base_path,
                                                   path,
                                                   extension,
                                                   access_modifier=access_modifier,
                                                   annotation_base_path=self.annotation_base_path,
                                                   database_name=ReplayAttackDatabase.name()))

            subset_accesses.sort(key=lambda x: x.name)

        return dict_all_accesses

    def get_enrolment_access(self, access_modifier=AccessModifier()):
        list_accesses = []
        objects = self.db.objects(cls='enroll')

        for access in objects:
            path, extension = os.path.splitext(access.videofile())
            list_accesses.append(VideoAccess(self.base_path,
                                             path,
                                             extension,
                                             access_modifier=access_modifier,
                                             annotation_base_path=self.annotation_base_path))

        list_accesses.sort(key=lambda x: x.name)
        return list_accesses

    def get_all_labels(self):
        if not self.dict_all_labels:
            try:
                dict_all_labels_aggregate_db = TestResources.get_aggregated_database_all_dict_labels()
                for subset in dict_all_labels_aggregate_db:
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][ReplayAttackDatabase.name()]

            except IOError:
                warnings.warn("WARNING (ReplayAttackDatabase.get_all_labels): Labels resource file "
                              "[resources/aggregate_database_all_labels.pickle] not found. "
                              "Extracting all labels from scratch may take a while.")
                self.dict_all_labels = self._extract_all_labels_from_scratch()

        return self.dict_all_labels

    def _extract_all_labels_from_scratch(self):
        dict_all_labels = {'Train': {},
                           'Dev': {},
                           'Test': {}}

        for subset, subset_labels_dict in dict_all_labels.items():
            for obj in self.db.objects(groups=REPLAY_SUBSETS_CORRESPONDENCE[subset], protocol='grandtest'):
                basename, extension = os.path.splitext(obj.videofile())

                subset_labels_dict[basename] = {
                    'capture_device': REPLAY_CAPTURE_DEVICES['macbook'],
                    'user': int(obj.client_id)-1,
                    'light': REPLAY_LIGHTS[obj.light],
                    'common_capture_device': REPLAY_COMMON_CAPTURE_DEVICES['macbook'],
                    'common_lightning': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION[obj.light],
                    'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(self.base_path,
                                                                                                   basename))}
                if obj.is_real():
                    subset_labels_dict[basename]['pai'] = REPLAY_PAI_CORRESPONDENCES['real']
                    subset_labels_dict[basename]['common_pai'] = REPLAY_COMMON_PAIS['real']
                    subset_labels_dict[basename]['scenario'] = REPLAY_SCENARIOS['real']
                else:
                    pai = obj.get_attack().attack_device        # print, mobile or highdef
                    support = obj.get_attack().attack_support   # hand or fixed
                    sample_type = obj.get_attack().sample_type  # video or photo

                    subset_labels_dict[basename]['pai'] = REPLAY_PAI_CORRESPONDENCES[pai]
                    subset_labels_dict[basename]['common_pai'] = REPLAY_COMMON_PAIS[pai]
                    subset_labels_dict[basename]['scenario'] = self._get_scenario(pai, support, sample_type)

        return dict_all_labels

    @staticmethod
    def _get_scenario(pai, support, sample_type):
        scenario = -1

        if pai == 'print':
                if support == 'hand' and sample_type == 'photo':
                    scenario = REPLAY_SCENARIOS['print_hand_photo']

                elif support == 'fixed' and sample_type == 'photo':
                    scenario = REPLAY_SCENARIOS['print_fixed_photo']

        elif pai == 'mobile':
            if support == 'hand':
                if sample_type == 'photo':
                    scenario = REPLAY_SCENARIOS['mobile_hand_photo']
                elif sample_type == 'video':
                    scenario = REPLAY_SCENARIOS['mobile_hand_video']

            elif support == 'fixed':
                if sample_type == 'photo':
                    scenario = REPLAY_SCENARIOS['mobile_fixed_photo']
                elif sample_type == 'video':
                    scenario = REPLAY_SCENARIOS['mobile_fixed_video']

        elif pai == 'highdef':
            if support == 'hand':
                if sample_type == 'photo':
                    scenario = REPLAY_SCENARIOS['highdef_hand_photo']
                elif sample_type == 'video':
                    scenario = REPLAY_SCENARIOS['highdef_hand_video']

            elif support == 'fixed':
                if sample_type == 'photo':
                    scenario = REPLAY_SCENARIOS['highdef_fixed_photo']
                elif sample_type == 'video':
                    scenario = REPLAY_SCENARIOS['highdef_fixed_video']

        return scenario

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in REPLAY_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in REPLAY_ATTACK protocols [{}]'.format(protocol,
                                                                                                  REPLAY_PROTOCOLS))
        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']
        return gt_dict
