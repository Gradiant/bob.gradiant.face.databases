#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

from bob.gradiant.core import Database, AccessModificator, VideoAccess
import bob.db.replay
import os

REPLAY_PROTOCOLS = ['grandtest']
REPLAY_SUBSETS = ['Train', 'Dev', 'Test']
REPLAY_CONVENTION = {'real': 0,
                     'print': 1,
                     'mobile': 2,
                     'highdef': 3}


class ReplayAttackDatabase(Database):
    def __init__(self, base_path, annotation_base_path = None):
        super(ReplayAttackDatabase, self).__init__(base_path, annotation_base_path = annotation_base_path)
        self.db = bob.db.replay.Database(original_directory=base_path)

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
        dict_info = { 'users' : 50,
                      'Train samples' : len(db.objects(groups='train', protocol ='grandtest')),
                      'Dev samples': len(db.objects(groups='devel', protocol='grandtest')),
                      'Test samples': len(db.objects(groups='test', protocol='grandtest'))}
        return dict_info

    @staticmethod
    def get_protocols():
        return REPLAY_PROTOCOLS

    @staticmethod
    def get_subsets():
        return REPLAY_SUBSETS

    def get_all_accesses(self, access_modificator=AccessModificator()):
        dict_all_accesses = {'Train': self.__get_accesses_from_subset('train', access_modificator),
                             'Dev': self.__get_accesses_from_subset('devel', access_modificator),
                             'Test': self.__get_accesses_from_subset('test', access_modificator)}
        return dict_all_accesses

    def get_enrolment_access(self, access_modificator=AccessModificator()):
        list_accesses = []
        objects = self.db.objects(cls='enroll')

        for access in objects:
            path, extension = os.path.splitext(access.videofile())
            list_accesses.append(VideoAccess(self.base_path,
                                             path,
                                             extension,
                                             access_modificator=access_modificator,
                                             annotation_base_path=self.annotation_base_path))

        list_accesses.sort(key=lambda x: x.name)
        return list_accesses

    def __get_accesses_from_subset(self, subset, access_modificator):
        list_accesses = []

        objects = self.db.objects(groups=subset)
        for access in objects:
            path, extension = os.path.splitext(access.videofile())
            list_accesses.append(VideoAccess(self.base_path,
                                             path,
                                             extension,
                                             access_modificator=access_modificator,
                                             annotation_base_path=self.annotation_base_path))

        list_accesses.sort(key=lambda x: x.name)
        return list_accesses

    def get_ground_truth(self, protocol):
        dict_files = {}

        if protocol not in REPLAY_PROTOCOLS:
            return dict_files

        dict_files['Train'] = self.__get_subset_labels('train', protocol)
        dict_files['Dev'] = self.__get_subset_labels('devel', protocol)
        dict_files['Test'] = self.__get_subset_labels('test', protocol)

        return dict_files

    def get_attack_dict(self):
        attack_dict = {k:v for k, v in REPLAY_CONVENTION.iteritems() if v is not 0}
        return attack_dict

    def __get_subset_labels(self, subset, protocol):
        group_label_dict = {}
        for obj in self.db.objects(groups=subset, protocol=protocol):
            basename, extension = os.path.splitext(obj.videofile())
            if obj.is_real():
                group_label_dict[basename] = 0
            else:
                group_label_dict[basename] = REPLAY_CONVENTION[obj.get_attack().attack_device]

        return group_label_dict
