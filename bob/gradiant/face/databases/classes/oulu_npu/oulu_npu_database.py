#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core import Database, AccessModificator, VideoAccess, TypeDatabase
import os

OULU_NPU_PROTOCOLS = ['grandtest',
                      'Protocol_1',
                      'Protocol_2',
                      'Protocol_3_1', 'Protocol_3_2', 'Protocol_3_3', 'Protocol_3_4', 'Protocol_3_5', 'Protocol_3_6',
                      'Protocol_4_1', 'Protocol_4_2', 'Protocol_4_3', 'Protocol_4_4', 'Protocol_4_5', 'Protocol_4_6',
                      'Protocol_4_no_loco']

OULU_NPU_SUBSETS = ['Train', 'Dev', 'Test']
OULU_NPU_FOLDERS_VIDEO = ['Train_files', 'Dev_files', 'Test_files']
OULU_NPU_VIDEO_EXTENSION = '.avi'
OULU_NPU_CONVENTION = {'real': 0,
                       'print1': 1,
                       'print2': 2,
                       'video-replay1': 3,
                       'video-replay2': 4}
OULU_NPU_FROM_TEXT_CONVENTION = {'+1': 0,
                                 '-1': 1,
                                 '-2': 2}

OULU_TAG_CORRESPONDENCES = {'1': 0,
                            '2': 1,
                            '3': 2,
                            '4': 3,
                            '5': 4}
OULU_FOLDERS_CORRESPONDENCE = {'Train_files': 'Train',
                               'Dev_files': 'Dev',
                               'Test_files': 'Test'}


class OuluNpuDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.base_path = base_path
        super(OuluNpuDatabase, self).__init__(base_path, type_database = TypeDatabase.ALL_FILES_TOGETHER, annotation_base_path = annotation_base_path)

    def __str__(self):
        return super(OuluNpuDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'oulu-npu'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = { 'users' : 55,
                      'Train samples' : 1800,
                      'Dev samples': 1350,
                      'Test samples': 1800}
        return dict_info

    @staticmethod
    def get_protocols():
        return OULU_NPU_PROTOCOLS

    @staticmethod
    def get_subsets():
        return OULU_NPU_SUBSETS

    def get_all_accesses(self, access_modificator=AccessModificator()):
        dict_all_accesses = {}
        list_accesses = []
        dict_accesses_by_subset = self.get_accesses_by_subset(access_modificator)
        for subset in dict_accesses_by_subset:
            list_accesses += dict_accesses_by_subset[subset]
        list_accesses.sort(key=lambda x: x.name)
        dict_all_accesses['All'] = list_accesses
        return dict_all_accesses

    def get_accesses_by_subset(self, access_modificator=AccessModificator()):
        dict_accesses_by_subset = {}
        list_accesses = []
        folders_correspondence = {'Train_files': 'Train',
                                  'Dev_files': 'Dev',
                                  'Test_files': 'Test'}
        for folder in OULU_NPU_FOLDERS_VIDEO:
            folder_set = os.path.join(self.base_path, folder)
            list_basename_access = self.__get_list_basename_access_from_folder(folder_set)
            for basename in list_basename_access:
                list_accesses.append(VideoAccess(folder_set,
                                                 basename,
                                                 OULU_NPU_VIDEO_EXTENSION,
                                                 access_modificator=access_modificator,
                                                 annotation_base_path=self.annotation_base_path))
            list_accesses.sort(key=lambda x: x.name)
            dict_accesses_by_subset[folders_correspondence[folder]] = list_accesses
            list_accesses = []
        return dict_accesses_by_subset

    def get_ground_truth(self, protocol):
        dict_files = {}

        if protocol == 'grandtest':
            for folder in OULU_NPU_FOLDERS_VIDEO:
                dict_subset = {}
                folder_set = os.path.join(self.base_path, folder)
                list_basename_access = self.__get_list_basename_access_from_folder(folder_set)
                for basename in list_basename_access:
                    dict_subset[basename] = OULU_TAG_CORRESPONDENCES[basename[-1]]
                dict_files[OULU_FOLDERS_CORRESPONDENCE[folder]] = dict_subset
        elif protocol == 'Protocol_4_no_loco':
            for subset in OULU_NPU_SUBSETS:
                dict_subset = {}
                for i in range(6):
                    filename = os.path.join(self.base_path, 'Protocols', 'Protocol_4', subset + '_' + str(i+1) + '.txt')
                    dict_split = self.__get_dict_files_and_labels_from_filename(filename)
                    dict_subset.update(dict_split)
                dict_files[subset] = dict_subset
        else:
            for subset in OULU_NPU_SUBSETS:
                filename = self.__get_filename_from_protocol(protocol, subset)
                dict_files[subset] = self.__get_dict_files_and_labels_from_filename(filename)

        return dict_files

    def get_attack_dict(self):
        attack_dict = {k: v for k, v in OULU_NPU_CONVENTION.iteritems() if v is not 0}
        return attack_dict

    @staticmethod
    def __get_list_basename_access_from_folder(folder):
        list_basename_video = []
        for file in os.listdir(folder):
            if file.endswith(OULU_NPU_VIDEO_EXTENSION):
                basename = file.rsplit('.')[0]
                list_basename_video.append(basename)
        return list_basename_video

    def __get_filename_from_protocol(self, protocol, subset):
        if protocol in ['Protocol_1', 'Protocol_2']:
            filename = os.path.join(self.base_path,'Protocols',protocol, subset + '_2.txt')
        else:
            split_protocol = protocol.rsplit('_',1)
            protocol = split_protocol[0]
            id = str(split_protocol[-1])
            filename = os.path.join(self.base_path, 'Protocols', protocol, subset + '_2_'+ id + '.txt')
        return filename

    @staticmethod
    def __get_dict_files_and_labels_from_filename(filename):
        dict_labels_and_files = {}
        with open(filename, 'r') as infile:
            data = infile.read()
            list_lines = data.splitlines()
        for line in list_lines:
            split_values = line.split(',')
            label = OULU_NPU_FROM_TEXT_CONVENTION[split_values[0]]
            filename_video = split_values[1]
            dict_labels_and_files[filename_video] = label
        return dict_labels_and_files
