#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
import glob
import warnings
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.core import Database, AccessModifier, VideoAccess, TypeDatabase
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat

UVAD_PROTOCOLS = ['grandtest']
UVAD_SUBSETS = ['Train', 'Test']
UVAD_PAIS = {'real': 0,
             'replay': 1}

UVAD_PAI_CORRESPONDENCE = {'real': UVAD_PAIS['real'],
                           'attack': UVAD_PAIS['replay']}

UVAD_MONITORS = {'None': 0,
                 'monitor1': 1,  # LG E1941 (1366x768)
                 'monitor2': 2,  # Samsung 930 (1280x1024)
                 'monitor3': 3,  # LG E2250V (1920x1080)
                 'monitor4': 4,  # Samsung P2270 (1920 x 1080)
                 'monitor5': 5,  # LG W2252TQ (1680X1050)
                 'monitor6': 6,  # Samsung 2232BWPlus (1680 x 1050)
                 'monitor7': 7}  # Philips 226V3LSB (1920 x 1080)

UVAD_COMMON_PAIS = {'real': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                    'monitor1': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['medium_quality'],
                    'monitor2': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['medium_quality'],
                    'monitor3': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['high_quality'],
                    'monitor4': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['high_quality'],
                    'monitor5': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['medium_quality'],
                    'monitor6': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['medium_quality'],
                    'monitor7': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['high_quality']}

UVAD_CAPTURE_DEVICES = {'cybershot_dsc_hx1': 0,
                        'canon_powershot_sx1': 1,
                        'nikon_coolpix_p100': 2,
                        'kodak_z981': 3,
                        'olympus_sp_800UZ': 4,
                        'panasonic_fz35': 5}

UVAD_COMMON_DEVICE_CORRESPONDENCE = {'canon': UVAD_CAPTURE_DEVICES['canon_powershot_sx1'],
                                     'kodac': UVAD_CAPTURE_DEVICES['kodak_z981'],
                                     'nikon': UVAD_CAPTURE_DEVICES['nikon_coolpix_p100'],
                                     'olympus': UVAD_CAPTURE_DEVICES['olympus_sp_800UZ'],
                                     'panasonic': UVAD_CAPTURE_DEVICES['panasonic_fz35'],
                                     'sony': UVAD_CAPTURE_DEVICES['cybershot_dsc_hx1']}

UVAD_COMMON_DEVICES = {'canon': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['digital_camera']['high_quality'],
                       'kodac': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['digital_camera']['high_quality'],
                       'nikon': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['digital_camera']['high_quality'],
                       'olympus': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['digital_camera']['high_quality'],
                       'panasonic': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['digital_camera']['high_quality'],
                       'sony': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['digital_camera']['high_quality'], }


class UvadDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.base_path = base_path
        self.dict_all_accesses = {}
        self.dict_all_labels = {}
        super(UvadDatabase, self).__init__(base_path, type_database=TypeDatabase.ALL_FILES_TOGETHER,
                                           annotation_base_path=annotation_base_path)

    def __str__(self):
        return super(UvadDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'uvad'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = {'users': 404,
                     'Train videos': 4124,
                     'Dev videos': 1020,
                     'Test videos': 5144}
        return dict_info

    @staticmethod
    def get_protocols():
        return UVAD_PROTOCOLS

    @staticmethod
    def get_subsets():
        return UVAD_SUBSETS

    @staticmethod
    def get_capture_devices():
        return UVAD_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in UVAD_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        if not self.dict_all_accesses:
            self.dict_all_accesses = {'Train':[],
                                      'Dev': [],
                                      'Test': []}

            dict_videos = {}
            for root, dirs, files in os.walk(self.base_path):
                if not dirs:
                    for f in files:
                        if f.lower().endswith(('.mp4', '.mov')):
                            basename, ext = os.path.splitext(f)
                            if basename not in dict_videos:
                                dict_videos[basename] = []
                            dict_videos[basename].append(os.path.join(root, f))

            for subset, subset_accesses in self.dict_all_accesses.items():
                txt_file = os.path.join(self.base_path, 'release_1', 'protocols', 'grandtest', subset + '.txt')
                with open(txt_file) as my_file:
                    for line in my_file.readlines():
                        user, video1, video2 = line.rstrip().split(' ')
                        basename1, _ = os.path.splitext(video1)
                        basename2, _ = os.path.splitext(video2)

                        for basename in [basename1, basename2]:
                            for full_access_path in dict_videos[basename]:
                                extension = os.path.basename(full_access_path).split('.')[1]
                                relative_path = os.path.relpath(full_access_path, self.base_path).replace('.' + extension, '')

                                subset_accesses.append(VideoAccess(os.path.join(self.base_path),
                                                                   relative_path,
                                                                   ('.' + extension).rstrip(),
                                                                   access_modifier=access_modifier,
                                                                   annotation_base_path=self.annotation_base_path,
                                                                   database_name=UvadDatabase.name()))
                subset_accesses.sort(key=lambda x: x.name)

        return self.dict_all_accesses

    def get_all_labels(self):
        if not self.dict_all_labels:
            try:
                dict_all_labels_aggregate_db = TestResources.get_aggregated_database_all_dict_labels()
                for subset in dict_all_labels_aggregate_db:
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][UvadDatabase.name()]

            except IOError:
                warnings.warn("WARNING (UvadDatabase.get_all_labels): Labels resource file "
                              "[resources/aggregate_database_all_labels.pickle] not found. "
                              "Extracting all labels from scratch may take a while.")
                self.dict_all_labels = self._extract_all_labels_from_scratch()

        return self.dict_all_labels

    def _extract_all_labels_from_scratch(self):
        dict_all_labels = {'Train': {},
                           'Dev': {},
                           'Test': {}}

        dict_all_accesses = self.get_all_accesses()

        for subset, list_accesses in dict_all_accesses.items():
            for access in list_accesses:

                full_path = os.path.join(access.base_path, access.name)
                split_path = os.path.normpath(os.path.dirname(full_path)).split(os.path.sep)

                if split_path[-2] in UVAD_PAI_CORRESPONDENCE:
                    dict_all_labels[subset][access.name] = {
                        'pai': UVAD_PAI_CORRESPONDENCE['real'],
                        'scenario': UVAD_PAI_CORRESPONDENCE[split_path[-2]],
                        'monitor': UVAD_MONITORS['None'],
                        'capture_device': UVAD_COMMON_DEVICE_CORRESPONDENCE[split_path[-1]],
                        'user': 0,
                        'common_pai': UVAD_COMMON_PAIS['real'],
                        'common_capture_device': UVAD_COMMON_DEVICES[split_path[-1]],
                        'common_lightning': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['no_info'],
                        'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(full_path)),
                        }
                else:
                    dict_all_labels[subset][access.name] = {
                        'pai': UVAD_PAI_CORRESPONDENCE[split_path[-4]],
                        'scenario': UVAD_PAI_CORRESPONDENCE[split_path[-4]],
                        'capture_device': UVAD_COMMON_DEVICE_CORRESPONDENCE[split_path[-2]],
                        'user': 0,
                        'monitor': UVAD_MONITORS[split_path[-1]],
                        'common_pai': UVAD_COMMON_PAIS[split_path[-1]],
                        'common_capture_device': UVAD_COMMON_DEVICES[split_path[-2]],
                        'common_lightning': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['no_info'],
                        'common_face_resolution': 0  # most of UVAD videos have small IED (see histograms)
                        #'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(full_path))
                        }
        return dict_all_labels

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in UVAD_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in UVAD protocols [{}]'.format(protocol, UVAD_PROTOCOLS))

        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict
