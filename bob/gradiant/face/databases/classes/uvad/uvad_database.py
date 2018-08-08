#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core import Database, AccessModificator, VideoAccess, TypeDatabase
import glob
import os

UVAD_PROTOCOLS = ['protocol_1']
UVAD_SUBSETS = ['Train', 'Test']
UVAD_CONVENTION = {'real': 0,
                   'highdef': 3}


class UvadDatabase(Database):
    def __init__(self, base_path, annotation_base_path = None):
        self.base_path = base_path
        super(UvadDatabase, self).__init__(base_path, type_database = TypeDatabase.ALL_FILES_TOGETHER, annotation_base_path = annotation_base_path)

    def __str__(self):
        return super(UvadDatabase, self).__str__(name=self.__class__.__name__)

    @property
    def name(self):
        return 'uvad'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = { 'users' : 404,
                      'Train samples' : 2768,
                      'Dev samples' : 0,
                      'Test samples': 2476}
        return dict_info

    @staticmethod
    def get_protocols():
        return UVAD_PROTOCOLS

    @staticmethod
    def get_subsets():
        return UVAD_SUBSETS

    def get_all_accesses(self, access_modificator=AccessModificator()):
        dict_all_accesses = {'Train': self.__get_accesses_from_subset('train', access_modificator), 'Dev': [],
                             'Test': self.__get_accesses_from_subset('test', access_modificator)}
        return dict_all_accesses

    def __get_accesses_from_subset(self, subset, access_modificator=AccessModificator()):
        list_accesses = []
        txt_path = os.path.join(self.base_path, 'release_1', 'protocols', 'experiment_1')
        for txt_file in glob.glob(txt_path+'/*.txt'):
            if not subset in txt_file:
                continue
            with open(txt_file) as my_file:
                for line in my_file.readlines():
                    splitted_line = line.split('/')
                    relative_path = os.path.join(self.base_path, 'release_1', *splitted_line[:-1])
                    basename, extension = splitted_line[-1].split('.')
                    list_accesses.append(VideoAccess(relative_path,
                                                     basename,
                                                     ('.'+extension).rstrip(),
                                                     access_modificator=access_modificator,
                                                     annotation_base_path=self.annotation_base_path))
        list_accesses.sort(key=lambda x: x.name)
        return list_accesses

    def get_ground_truth(self, protocol):
        dict_files = {}

        if protocol not in UVAD_PROTOCOLS:
            return dict_files

        dict_files['Train'] = self.__get_subset_labels('train', protocol)
        dict_files['Dev'] = {}
        dict_files['Test'] = self.__get_subset_labels('test', protocol)
        return dict_files

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in UVAD_CONVENTION.iteritems() if v is not 0}
        return attack_dict

    def __get_subset_labels(self, subset, protocol):
        group_label_dict = {}
        list_accesses = self. __get_accesses_from_subset(subset, AccessModificator())

        for access in list_accesses:
            if '/real/' in access.base_path:
                group_label_dict[os.path.join(access.base_path, access.name)] = 0
            else:
                group_label_dict[os.path.join(access.base_path, access.name)] = 3

        return group_label_dict