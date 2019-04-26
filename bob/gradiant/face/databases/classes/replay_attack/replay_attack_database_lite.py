#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
from bob.gradiant.core import Database, AccessModifier, VideoAccess
import bob.db.replay
import os

REPLAY_LITE_PROTOCOLS = ['grandtest']
REPLAY_LITE_SUBSETS = ['Train', 'Dev', 'Test']
REPLAY_LITE_CONVENTION = {'real' : 0,
                          'print' : 1,
                          'mobile': 2,
                          'highdef': 3}
REPLAY_LITE_USERS = [1, 3, 9]

REPLAY_LITE_DEVICES = {'macbook_webcam': 0}

REPLAY_LITE_LIGHTS = {'controlled': 0,
                 'adverse': 1}


class ReplayAttackDatabaseLite(Database):
    def __init__(self, base_path, annotation_base_path = None):
        self.base_path = base_path
        super(ReplayAttackDatabaseLite, self).__init__(base_path, annotation_base_path = annotation_base_path)
        self.db = bob.db.replay.Database(original_directory=base_path)

    def __str__(self):
        return super(ReplayAttackDatabaseLite, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'replay-attack-lite'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    def get_protocols(self):
        return REPLAY_LITE_PROTOCOLS

    def get_subsets(self):
        return REPLAY_LITE_SUBSETS

    def filter_objects(self, objects):
        return [object for object in objects if object.client_id in REPLAY_LITE_USERS]

    def get_attack_dict(self):
        attack_dict = {k:v for k,v in REPLAY_LITE_CONVENTION.items() if v is not 0}
        return attack_dict

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
            path, extension = os.path.splitext(access.videofile())
            list_accesses.append(VideoAccess(self.base_path,
                                             path,
                                             extension,
                                             access_modifier=access_modifier,
                                             annotation_base_path=self.annotation_base_path,
                                             database_name=ReplayAttackDatabaseLite.name()))

        list_accesses.sort(key=lambda x: x.name)
        return list_accesses

    def get_all_labels(self, protocol):
        dict_all_labels = {'Train': self._get_labels_from_subset('train', protocol),
                           'Dev': self._get_labels_from_subset('devel', protocol),
                           'Test': self._get_labels_from_subset('test', protocol)}
        return dict_all_labels

    def __get_subset_labels(self, subset, protocol):
        group_label_dict = {}

        objects = self.db.objects(groups=subset, protocol=protocol)
        objects = self.filter_objects(objects)
        for obj in objects:
            basename, extension = os.path.splitext(obj.videofile())
            if obj.is_real():
                group_label_dict[basename] = 0
            else:
                group_label_dict[basename] = REPLAY_LITE_CONVENTION[obj.get_attack().attack_device]
        return group_label_dict

    def _get_labels_from_subset(self, subset, protocol):
        subset_labels_dict = {}

        objects = self.db.objects(groups=subset, protocol=protocol)
        objects = self.filter_objects(objects)

        for obj in objects:
            basename, extension = os.path.splitext(obj.videofile())

            subset_labels_dict[basename] = {'client': obj.client_id,
                                            'device': REPLAY_LITE_DEVICES['macbook_webcam'],
                                            'light': REPLAY_LITE_LIGHTS[obj.light]}
            if obj.is_real():
                subset_labels_dict[basename]['pai'] = REPLAY_LITE_CONVENTION['real']

            else:
                subset_labels_dict[basename]['pai'] = REPLAY_LITE_CONVENTION[obj.get_attack().attack_device]

        return subset_labels_dict

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in REPLAY_LITE_PROTOCOLS:
            return gt_dict

        dict_all_labels = self.get_all_labels(protocol)

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict

