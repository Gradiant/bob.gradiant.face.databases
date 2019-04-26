#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
from bob.gradiant.core import Database, AccessModifier, VideoAccess, RotationRule
import bob.db.replaymobile
import os

REPLAYMOBILE_LITE_PROTOCOLS = ['grandtest']
REPLAYMOBILE_LITE_SUBSETS = ['Train', 'Dev', 'Test']
REPLAYMOBILE_LITE_VIDEO_EXTENSION = '.mov'
REPLAYMOBILE_LITE_CONVENTION = {'real': 0,
                                'print': 1,
                                'mattescreen': 2}

REPLAYMOBILE_LITE_DEVICES = {'mobile': 0,
                             'tablet': 1}

REPLAYMOBILE_LITE_LIGHTS = {'lighton': 0,
                            'controlled': 0,
                            'direct': 0,
                            'lateral': 0,
                            'diffuse': 0,
                            'adverse': 1,
                            'lightoff': 1}
LITE_USERS = [1, 5, 2]


class ReplayMobileDatabaseLite(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.base_path = base_path
        super(ReplayMobileDatabaseLite, self).__init__(base_path, annotation_base_path=annotation_base_path)
        self.db = bob.db.replaymobile.Database(original_directory=base_path)

    def __str__(self):
        return super(ReplayMobileDatabaseLite, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'replay-mobile-lite'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    def get_protocols(self):
        return REPLAYMOBILE_LITE_PROTOCOLS

    def get_subsets(self):
        return REPLAYMOBILE_LITE_SUBSETS

    def get_attack_dict(self):
        attack_dict = {k: v for k, v in REPLAYMOBILE_LITE_CONVENTION.items() if v is not 0}
        return attack_dict

    def filter_objects(self, objects):
        return [object for object in objects if object.client_id in LITE_USERS]

    def get_all_accesses(self, access_modifier=AccessModifier()):
        dict_all_accesses = {}
        dict_all_accesses['Train'] = self.__get_accesses_from_subset('train', access_modifier)
        dict_all_accesses['Dev'] = self.__get_accesses_from_subset('devel', access_modifier)
        dict_all_accesses['Test'] = self.__get_accesses_from_subset('test', access_modifier)
        return dict_all_accesses

    def __get_accesses_from_subset(self, subset, access_modifier):
        list_accesses = []
        objects = self.db.objects(groups=subset)
        objects = self.filter_objects(objects)
        for access in objects:
            rotation_rule = self.get_rotation_rule(access)
            path, extension = os.path.splitext(access.videofile())
            list_accesses.append(VideoAccess(self.base_path,
                                             path,
                                             extension,
                                             access_modifier=access_modifier,
                                             rotation_rule=rotation_rule,
                                             annotation_base_path=self.annotation_base_path,
                                             database_name=ReplayMobileDatabaseLite.name()))

        list_accesses.sort(key=lambda x: x.name)
        return list_accesses

    def get_rotation_rule(self, access):
        if access.is_mobile():
            rotation_rule = RotationRule.ROTATION_90
        else:
            rotation_rule = RotationRule.ROTATION_270
        return rotation_rule

    def get_all_labels(self, protocol):
        dict_all_labels = {'Train': self._get_labels_from_subset('train', protocol),
                           'Dev': self._get_labels_from_subset('devel', protocol),
                           'Test': self._get_labels_from_subset('test', protocol)}
        return dict_all_labels

    def _get_labels_from_subset(self, subset, protocol):
        subset_labels_dict = {}
        objects = self.db.objects(groups=subset)
        objects = self.filter_objects(objects)

        for obj in objects:
            basename, extension = os.path.splitext(obj.videofile())

            subset_labels_dict[basename] = {'client': obj.client_id,
                                            'device': REPLAYMOBILE_LITE_DEVICES[obj.device],
                                            'light': REPLAYMOBILE_LITE_LIGHTS[obj.light]}

            if obj.is_real():
                subset_labels_dict[basename]['pai'] = REPLAYMOBILE_LITE_CONVENTION['real']

            else:
                PAI = obj.get_attack().attack_device  # print or mattescreen
                support = obj.get_attack().attack_support  # hand or fixed
                sample_type = obj.get_attack().sample_type  # video or photo

                if PAI == 'print' and support == 'hand' and sample_type == 'photo':
                    subset_labels_dict[basename]['pai'] = REPLAYMOBILE_LITE_CONVENTION['print_hand_photo']

                elif PAI == 'print' and support == 'fixed' and sample_type == 'photo':
                    subset_labels_dict[basename]['pai'] = REPLAYMOBILE_LITE_CONVENTION['print_fixed_photo']

                elif PAI == 'mattescreen' and support == 'fixed' and sample_type == 'photo':
                    subset_labels_dict[basename]['pai'] = REPLAYMOBILE_LITE_CONVENTION['mattescreen_fixed_photo']

                elif PAI == 'mattescreen' and support == 'fixed' and sample_type == 'video':
                    subset_labels_dict[basename]['pai'] = REPLAYMOBILE_LITE_CONVENTION['mattescreen_fixed_video']

                else:
                    subset_labels_dict[basename]['pai'] = None

        return subset_labels_dict

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in REPLAYMOBILE_LITE_PROTOCOLS:
            return gt_dict

        dict_all_labels = self.get_all_labels(protocol)

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict
