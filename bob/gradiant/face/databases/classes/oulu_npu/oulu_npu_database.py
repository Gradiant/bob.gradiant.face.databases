#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
import warnings
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.core import Database, AccessModifier, VideoAccess, TypeDatabase
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat


OULU_PROTOCOLS = ['grandtest',
                  'Protocol_1',
                  'Protocol_2',
                  'Protocol_3_1', 'Protocol_3_2', 'Protocol_3_3', 'Protocol_3_4', 'Protocol_3_5', 'Protocol_3_6',
                  'Protocol_4_1', 'Protocol_4_2', 'Protocol_4_3', 'Protocol_4_4', 'Protocol_4_5', 'Protocol_4_6',
                  'Protocol_4_no_loco']

OULU_SUBSETS = ['Train', 'Dev', 'Test']
OULU_FOLDERS_VIDEO = ['Train_files', 'Dev_files', 'Test_files']
OULU_FOLDERS_CORRESPONDENCE = {'Train_files': 'Train',
                               'Dev_files': 'Dev',
                               'Test_files': 'Test'}
OULU_FOLDERS_REVERSE_CORRESPONDENCE = {'Train': 'Train_files',
                                       'Dev': 'Dev_files',
                                       'Test': 'Test_files'}
OULU_VIDEO_EXTENSION = '.avi'

OULU_NPU_FROM_TEXT_CONVENTION = {'+1': 0,
                                 '-1': 1,
                                 '-2': 2}
OULU_PAIS = {'real': 0,
             'print': 1,   # Canon imagePRESS C6011 (1200x1200 dpi) & Canon PIXMA iX655 (9600x2400 dpi)
             'replay': 2}  # MacBook Retina (13", 2560x1600) & Dell 1905FP (19", 1280x1024)

OULU_PAI_CORRESPONDENCES = {'1': OULU_PAIS['real'],
                            '2': OULU_PAIS['print'],    # Canon imagePRESS C6011 (1200x1200 dpi)
                            '3': OULU_PAIS['print'],    # Canon PIXMA iX655 (9600x2400 dpi)
                            '4': OULU_PAIS['replay'],   # MacBook Retina (13", 2560x1600)
                            '5': OULU_PAIS['replay']}   # Dell 1905FP (19", 1280x1024)

OULU_COMMON_PAIS = {'1': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                    '2': inter_db_cat.COMMON_PAI_CATEGORISATION['print']['high_quality'],
                    '3': inter_db_cat.COMMON_PAI_CATEGORISATION['print']['high_quality'],
                    '4': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['medium_quality'],
                    '5': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['high_quality']}

OULU_CAPTURE_DEVICES = {'samsung_galaxy_s6_edge': 0,
                        'htc_desire_eye': 1,
                        'meizu_x5': 2,
                        'asus_xenfone': 3,
                        'sony_xperia_c5': 4,
                        'oppo_n3': 5}

OULU_CAPTURE_DEVICE_CORRESPONDENCES = {'1': OULU_CAPTURE_DEVICES['samsung_galaxy_s6_edge'],
                                       '2': OULU_CAPTURE_DEVICES['htc_desire_eye'],
                                       '3': OULU_CAPTURE_DEVICES['meizu_x5'],
                                       '4': OULU_CAPTURE_DEVICES['asus_xenfone'],
                                       '5': OULU_CAPTURE_DEVICES['sony_xperia_c5'],
                                       '6': OULU_CAPTURE_DEVICES['oppo_n3']}

OULU_COMMON_CAPTURE_DEVICES = {'1': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['low_quality'],
                               '2': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['high_quality'],
                               '3': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['low_quality'],
                               '4': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['high_quality'],
                               '5': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['high_quality'],
                               '6': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['high_quality']}

OULU_COMMON_LIGHTNING = {'1': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['adverse'],    # session 1
                         '2': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled'], # session 2
                         '3': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['adverse']}    # session 3


class OuluNpuDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.base_path = base_path
        self.dict_all_labels = {}
        super(OuluNpuDatabase, self).__init__(base_path, type_database=TypeDatabase.ALL_FILES_TOGETHER,
                                              annotation_base_path=annotation_base_path)

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
        dict_info = {'users': 55,
                     'Train videos': 1800,
                     'Dev videos': 1350,
                     'Test videos': 1800}
        return dict_info

    @staticmethod
    def get_protocols():
        return OULU_PROTOCOLS

    @staticmethod
    def get_subsets():
        return OULU_SUBSETS

    @staticmethod
    def get_capture_devices():
        return OULU_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in OULU_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        dict_all_accesses = {}
        list_accesses = []
        folders_correspondence = {'Train_files': 'Train',
                                  'Dev_files': 'Dev',
                                  'Test_files': 'Test'}
        for folder in OULU_FOLDERS_VIDEO:
            folder_set = os.path.join(self.base_path, folder)
            list_basename_access = self.__get_list_basename_access_from_folder(folder_set)
            for basename in list_basename_access:
                list_accesses.append(VideoAccess(self.base_path,
                                                 os.path.join(folder, basename),
                                                 OULU_VIDEO_EXTENSION,
                                                 access_modifier=access_modifier,
                                                 annotation_base_path=self.annotation_base_path,
                                                 database_name=OuluNpuDatabase.name()))
            list_accesses.sort(key=lambda x: x.name)
            dict_all_accesses[folders_correspondence[folder]] = list_accesses
            list_accesses = []
        return dict_all_accesses

    @staticmethod
    def __get_list_basename_access_from_folder(folder):
        list_basename_video = []
        for f in os.listdir(folder):
            if f.endswith(OULU_VIDEO_EXTENSION):
                basename = f.rsplit('.')[0]
                list_basename_video.append(basename)
        return list_basename_video

    def get_all_labels(self):
        if not self.dict_all_labels:
            try:
                dict_all_labels_aggregate_db = TestResources.get_aggregated_database_all_dict_labels()
                for subset in dict_all_labels_aggregate_db:
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][OuluNpuDatabase.name()]

            except IOError:
                warnings.warn("WARNING (OuluNpuDatabase.get_all_labels): Labels resource file "
                              "[resources/aggregate_database_all_labels.pickle] not found. "
                              "Extracting all labels from scratch may take a while.")
                self.dict_all_labels = self._extract_all_labels_from_scratch()

        return self.dict_all_labels

    def _extract_all_labels_from_scratch(self):
        dict_all_labels = {'Train': {},
                           'Dev': {},
                           'Test': {}}

        for subset in dict_all_labels:
            folder_set = os.path.join(self.base_path, subset + '_files')
            list_basename_access = self.__get_list_basename_access_from_folder(folder_set)
            for basename in list_basename_access:
                dict_all_labels[subset][os.path.join(OULU_FOLDERS_REVERSE_CORRESPONDENCE[subset], basename)] = \
                    self.__get_labels_from_basename(folder_set, basename)

        return dict_all_labels

    @staticmethod
    def __get_labels_from_basename(folder_set, basename):
        split_labels = basename.split('_')
        labels_dict = {'capture_device': OULU_CAPTURE_DEVICE_CORRESPONDENCES[split_labels[0]],
                       'common_capture_device': OULU_COMMON_CAPTURE_DEVICES[split_labels[0]],
                       'common_lightning': OULU_COMMON_LIGHTNING[split_labels[1]],
                       'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(folder_set, basename)),
                       'pai': OULU_PAI_CORRESPONDENCES[split_labels[3]],
                       'common_pai': OULU_COMMON_PAIS[split_labels[3]],
                       'scenario': int(split_labels[3]) - 1,
                       'session': int(split_labels[1]) - 1,
                       'user': int(split_labels[2]) - 1}
        return labels_dict

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in OULU_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in OULU_NPU protocols [{}]'. format(protocol, OULU_PROTOCOLS))

        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            protocol_subset_basenames = []

            if protocol == 'grandtest':
                folder_set = os.path.join(self.base_path, subset + '_files')
                protocol_subset_basenames = self.__get_list_basename_access_from_folder(folder_set)

            else:
                protocol_files = self.__get_protocol_files_from_protocol_and_subset(subset, protocol)

                for protocol_file in protocol_files:
                    with open(protocol_file, 'r') as infile:
                        data = infile.read()
                        list_lines = data.splitlines()

                    for line in list_lines:
                        split_values = line.split(',')
                        basename = split_values[1]
                        protocol_subset_basenames.append(basename)

            for basename in protocol_subset_basenames:
                key = os.path.join(OULU_FOLDERS_REVERSE_CORRESPONDENCE[subset], basename)
                gt_dict[subset][key] = dict_all_labels[subset][key]['pai']

        return gt_dict

    def __get_protocol_files_from_protocol_and_subset(self, subset, protocol):
        protocol_files = []

        if protocol in ['Protocol_1', 'Protocol_2']:
            protocol_files.append(os.path.join(self.base_path, 'Protocols', protocol, subset + '_2.txt'))

        elif protocol == 'Protocol_4_no_loco':
            for i in range(6):
                protocol_files.append(os.path.join(self.base_path, 'Protocols', 'Protocol_4',
                                                   subset + '_' + str(i + 1) + '.txt'))
        else:
            split_protocol = protocol.rsplit('_', 1)
            protocol = split_protocol[0]
            user = str(split_protocol[-1])
            protocol_files.append(os.path.join(self.base_path, 'Protocols', protocol, subset + '_2_' + user + '.txt'))

        return protocol_files