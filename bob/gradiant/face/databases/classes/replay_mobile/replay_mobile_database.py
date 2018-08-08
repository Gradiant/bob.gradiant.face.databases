#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core import Database, AccessModificator, VideoAccess, RotationRule
import bob.db.replaymobile
import os


REPLAYMOBILE_PROTOCOLS = ['grandtest']
REPLAYMOBILE_SUBSETS = ['Train', 'Dev', 'Test']
REPLAYMOBILE_VIDEO_EXTENSION = '.mov'
REPLAYMOBILE_CONVENTION = {'real': 0,
                           'print': 1,
                           'mattescreen': 2}


class ReplayMobileDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.base_path = base_path
        self.db = bob.db.replaymobile.Database(original_directory=base_path)
        super(ReplayMobileDatabase, self).__init__(base_path, annotation_base_path = annotation_base_path)

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
                     'Train samples': len(db.objects(groups='train', protocol='grandtest')),
                     'Dev samples': len(db.objects(groups='devel', protocol='grandtest')),
                     'Test samples': len(db.objects(groups='test', protocol='grandtest'))}
        return dict_info

    def get_protocols(self):
        return REPLAYMOBILE_PROTOCOLS

    def get_subsets(self):
        return REPLAYMOBILE_SUBSETS

    def get_all_accesses(self, access_modificator=AccessModificator()):
        dict_all_accesses = {'Train': self.__get_accesses_from_subset('train', access_modificator),
                             'Dev': self.__get_accesses_from_subset('devel', access_modificator),
                             'Test': self.__get_accesses_from_subset('test', access_modificator)}
        return dict_all_accesses

    def get_enrolment_access(self, access_modificator=AccessModificator()):
        list_accesses = []
        objects = self.db.objects(cls='enroll')
        for access in objects:
            rotation_rule = self.get_rotation_rule(access)
            path, extension = os.path.splitext(access.videofile())
            list_accesses.append(VideoAccess(self.base_path,
                                             path,
                                             extension,
                                             access_modificator=access_modificator,
                                             rotation_rule = rotation_rule,
                                             annotation_base_path = self.annotation_base_path))

        list_accesses.sort(key=lambda x: x.name)
        return list_accesses

    def __get_accesses_from_subset(self, subset, access_modificator):
        list_accesses = []
        objects = self.db.objects(groups=subset)
        for access in objects:
            rotation_rule = self.get_rotation_rule(access)
            path, extension = os.path.splitext(access.videofile())
            list_accesses.append(VideoAccess(self.base_path,
                                             path,
                                             extension,
                                             access_modificator=access_modificator,
                                             rotation_rule = rotation_rule,
                                             annotation_base_path = self.annotation_base_path))

        list_accesses.sort(key=lambda x: x.name)
        return list_accesses

    @staticmethod
    def get_rotation_rule(access):
        if access.is_mobile():
            rotation_rule = RotationRule.ROTATION_90
        else:
            rotation_rule = RotationRule.ROTATION_270
        return rotation_rule

    def get_ground_truth(self, protocol):
        dict_files = {}

        if protocol not in REPLAYMOBILE_PROTOCOLS:
            return dict_files

        dict_files['Train'] = self.__get_subset_labels('train', protocol)
        dict_files['Dev'] = self.__get_subset_labels('devel', protocol)
        dict_files['Test'] = self.__get_subset_labels('test', protocol)

        return dict_files

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in REPLAYMOBILE_CONVENTION.iteritems() if v is not 0}
        return attack_dict

    def __get_subset_labels(self, subset, protocol):
        group_label_dict = {}
        for e in self.db.objects(groups=subset, protocol=protocol):
            basename, extension = os.path.splitext(e.videofile())
            if e.is_real():
                group_label_dict[basename] = 0
            else:
                group_label_dict[basename] = REPLAYMOBILE_CONVENTION[e.get_attack().attack_device]
        return group_label_dict
