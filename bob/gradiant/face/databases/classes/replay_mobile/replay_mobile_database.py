#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
import warnings
import bob.db.replaymobile
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.core import Database, AccessModifier, VideoAccess, RotationRule
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat

REPLAY_MOBILE_PROTOCOLS = ['grandtest']
REPLAY_MOBILE_SUBSETS = ['Train', 'Dev', 'Test']
REPLAY_MOBILE_SUBSETS_CORRESPONDENCE = {'Train': 'train',
                                        'Dev': 'devel',
                                        'Test': 'test'}
REPLAY_MOBILE_VIDEO_EXTENSION = '.mov'

REPLAY_MOBILE_PAIS = {'real': 0,
                      'print': 1,   # A4 Konica Minolta laser (1200 x 600 dpi)
                      'replay': 2}  # Philips 227ELH (21.5" 1920x1080)

REPLAY_MOBILE_PAI_CORRESPONDENCES = {'real': REPLAY_MOBILE_PAIS['real'],
                                     'print': REPLAY_MOBILE_PAIS['print'],
                                     'mattescreen': REPLAY_MOBILE_PAIS['replay']}

REPLAY_MOBILE_COMMON_PAIS = {'real': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                             'print': inter_db_cat.COMMON_PAI_CATEGORISATION['print']['low_quality'],
                             'mattescreen': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['high_quality']}

REPLAY_MOBILE_CAPTURE_DEVICES = {'ipad_mini2': 0,  # ipad_mini2 (5MP)
                                 'lg_g47': 1}      # lg_g47 (16 MP)

REPLAY_MOBILE_CAPTURE_DEVICE_CORRESPONDENCES = {'mobile': REPLAY_MOBILE_CAPTURE_DEVICES['ipad_mini2'],
                                                'tablet': REPLAY_MOBILE_CAPTURE_DEVICES['lg_g47']}

REPLAY_MOBILE_COMMON_CAPTURE_DEVICES = {'mobile': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['high_quality'],
                                        'tablet': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['tablet']['low_quality']}

REPLAY_MOBILE_SCENARIOS = {'real': 0,
                           'print_hand_photo': 1,
                           'print_fixed_photo': 2,
                           'mattescreen_fixed_photo': 3,
                           'mattescreen_fixed_video': 4}

REPLAY_MOBILE_LIGHTS = {'lighton': 0,
                        'controlled': 0,
                        'direct': 0,
                        'lateral': 0,
                        'diffuse': 0,
                        'adverse': 1,
                        'lightoff': 1}

REPLAY_MOBILE_COMMON_LIGHTNING = {'lighton':  inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled'],
                                  'controlled':  inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled'],
                                  'direct':  inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled'],
                                  'lateral':  inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled'],
                                  'diffuse':  inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled'],
                                  'adverse':  inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['adverse'],
                                  'lightoff':  inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['adverse']}


class ReplayMobileDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.base_path = base_path
        self.dict_all_labels = {}
        self.db = bob.db.replaymobile.Database(original_directory=base_path)
        super(ReplayMobileDatabase, self).__init__(base_path, annotation_base_path=annotation_base_path)

    def __str__(self):
        return super(ReplayMobileDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'replay-mobile'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        db = bob.db.replaymobile.Database()
        dict_info = {'users': 40,
                     'Train videos': len(db.objects(groups='train', protocol='grandtest')),
                     'Dev videos': len(db.objects(groups='devel', protocol='grandtest')),
                     'Test videos': len(db.objects(groups='test', protocol='grandtest'))}
        return dict_info

    @staticmethod
    def get_protocols():
        return REPLAY_MOBILE_PROTOCOLS

    @staticmethod
    def get_subsets():
        return REPLAY_MOBILE_SUBSETS

    @staticmethod
    def get_capture_devices():
        return REPLAY_MOBILE_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in REPLAY_MOBILE_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        dict_all_accesses = {'Train': [],
                             'Dev': [],
                             'Test': []}

        for subset, subset_accesses in dict_all_accesses.items():
            objects = self.db.objects(groups=REPLAY_MOBILE_SUBSETS_CORRESPONDENCE[subset])
            for access in objects:
                rotation_rule = self.get_rotation_rule(access)
                path, extension = os.path.splitext(access.videofile())
                subset_accesses.append(VideoAccess(self.base_path,
                                                   path,
                                                   extension,
                                                   access_modifier=access_modifier,
                                                   rotation_rule=rotation_rule,
                                                   annotation_base_path=self.annotation_base_path,
                                                   database_name=ReplayMobileDatabase.name()))
            subset_accesses.sort(key=lambda x: x.name)

        return dict_all_accesses

    def get_enrolment_access(self, access_modifier=AccessModifier()):
        list_accesses = []
        objects = self.db.objects(cls='enroll')
        for access in objects:
            rotation_rule = self.get_rotation_rule(access)
            path, extension = os.path.splitext(access.videofile())
            list_accesses.append(VideoAccess(self.base_path,
                                             path,
                                             extension,
                                             access_modifier=access_modifier,
                                             rotation_rule=rotation_rule,
                                             annotation_base_path=self.annotation_base_path,
                                             database_name=ReplayMobileDatabase.name()))

        list_accesses.sort(key=lambda x: x.name)
        return list_accesses

    @staticmethod
    def get_rotation_rule(access):
        if access.is_mobile():
            rotation_rule = RotationRule.ROTATION_90
        else:
            rotation_rule = RotationRule.ROTATION_270
        return rotation_rule

    def get_all_labels(self):
        if not self.dict_all_labels:
            try:
                dict_all_labels_aggregate_db = TestResources.get_aggregated_database_all_dict_labels()
                for subset in dict_all_labels_aggregate_db:
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][ReplayMobileDatabase.name()]

            except IOError:
                warnings.warn("WARNING (ReplayMobileDatabase.get_all_labels): Labels resource file "
                              "[resources/aggregate_database_all_labels.pickle] not found. "
                              "Extracting all labels from scratch may take a while.")
                self.dict_all_labels = self._extract_all_labels_from_scratch()

        return self.dict_all_labels

    def _extract_all_labels_from_scratch(self):
        dict_all_labels = {'Train': {},
                           'Dev': {},
                           'Test': {}}

        for subset, subset_labels_dict in dict_all_labels.items():
            for obj in self.db.objects(groups=REPLAY_MOBILE_SUBSETS_CORRESPONDENCE[subset], protocol='grandtest'):
                basename, extension = os.path.splitext(obj.videofile())

                subset_labels_dict[basename] = {
                    'user': int(obj.client_id) - 1,
                    'light': REPLAY_MOBILE_LIGHTS[obj.light],
                    'capture_device': REPLAY_MOBILE_CAPTURE_DEVICE_CORRESPONDENCES[obj.device],
                    'common_capture_device': REPLAY_MOBILE_COMMON_CAPTURE_DEVICES[obj.device],
                    'common_lightning': REPLAY_MOBILE_COMMON_LIGHTNING[obj.light],
                    'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(self.base_path, basename)),
                    }

                if obj.is_real():
                    subset_labels_dict[basename]['pai'] = REPLAY_MOBILE_PAI_CORRESPONDENCES['real']
                    subset_labels_dict[basename]['common_pai'] = REPLAY_MOBILE_COMMON_PAIS['real']
                    subset_labels_dict[basename]['scenario'] = REPLAY_MOBILE_SCENARIOS['real']

                else:
                    pai = obj.get_attack().attack_device        # print or mattescreen
                    support = obj.get_attack().attack_support   # hand or fixed
                    sample_type = obj.get_attack().sample_type  # video or photo

                    subset_labels_dict[basename]['pai'] = REPLAY_MOBILE_PAI_CORRESPONDENCES[pai]
                    subset_labels_dict[basename]['common_pai'] = REPLAY_MOBILE_COMMON_PAIS[pai]
                    subset_labels_dict[basename]['scenario'] = self._get_common_scenario(basename, support, sample_type)

        return dict_all_labels

    @staticmethod
    def _get_common_scenario(pai, support, sample_type):
        scenario = -1

        if pai == 'print':
            if support == 'hand' and sample_type == 'photo':
                scenario = REPLAY_MOBILE_SCENARIOS['print_hand_photo']

            elif support == 'fixed' and sample_type == 'photo':
                scenario = REPLAY_MOBILE_SCENARIOS['print_fixed_photo']

        elif pai == 'mattescreen':
            if support == 'fixed' and sample_type == 'photo':
                scenario = REPLAY_MOBILE_SCENARIOS['mattescreen_fixed_photo']

            elif support == 'fixed' and sample_type == 'video':
                scenario = REPLAY_MOBILE_SCENARIOS['mattescreen_fixed_video']

        return scenario

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in REPLAY_MOBILE_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in REPLAY_MOBILE protocols [{}]'
                             .format(protocol, REPLAY_MOBILE_PROTOCOLS))

        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict
