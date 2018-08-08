#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core import Database, AccessModificator, VideoAccess
import bob.db.msu_mfsd_mod
import os

MSU_MFSD_PROTOCOLS = ['grandtest']
MSU_MFSD_SUBSETS = ['Train', 'Dev', 'Test']
MSU_MFSD_CONVENTION = {'real': 0,
                       'print': 1,
                       'video_hd': 2,
                       'video_mobile': 3}


class MsuMfsdDatabase(Database):
    def __init__(self, base_path, annotation_base_path = None):
        super(MsuMfsdDatabase, self).__init__(base_path, annotation_base_path = annotation_base_path)
        self.db = bob.db.msu_mfsd_mod.Database(original_directory=base_path)

    def __str__(self):
        return super(MsuMfsdDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'msu-mfsd'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        db = bob.db.msu_mfsd_mod.Database()
        dict_info = { 'users' : 35,
                      'Train samples' : len(db.objects(group='train')),
                      'Dev samples': len(db.objects(group='devel')),
                      'Test samples': len(db.objects(group='test'))}
        return dict_info

    @staticmethod
    def get_protocols():
        return MSU_MFSD_PROTOCOLS

    def get_subsets(self):
        return MSU_MFSD_SUBSETS

    def get_all_accesses(self, access_modificator=AccessModificator()):
        dict_all_accesses = {}
        dict_all_accesses['Train'] = self.__get_accesses_from_subset('train', access_modificator)
        dict_all_accesses['Dev'] = self.__get_accesses_from_subset('devel', access_modificator)
        dict_all_accesses['Test'] = self.__get_accesses_from_subset('test', access_modificator)
        return dict_all_accesses

    def __get_accesses_from_subset(self, subset, access_modificator):
        list_accesses = []
        objects = self.db.objects(group=subset)
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

        if protocol not in MSU_MFSD_PROTOCOLS:
            return dict_files

        dict_files['Train'] = self.__get_subset_labels('train')
        dict_files['Dev'] = self.__get_subset_labels('devel')
        dict_files['Test'] = self.__get_subset_labels('test')

        return dict_files

    def get_attack_dict(self):
        attack_dict = {k: v for k, v in MSU_MFSD_CONVENTION.iteritems() if v is not 0}
        return attack_dict

    def __get_subset_labels(self, subset):
        group_label_dict = {}
        for obj in self.db.objects(group=subset):
            basename, extension = os.path.splitext(obj.videofile())
            if obj.is_real():
                group_label_dict[basename] = 0
            else:
                group_label_dict[basename] = MSU_MFSD_CONVENTION[obj.instrument]
        return group_label_dict
