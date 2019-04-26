#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
import warnings
import bob.db.maskattack
from bob.gradiant.core import Database, AccessModifier, VideoAccess
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat

THREEDMAD_PROTOCOLS = ['grandtest']
THREEDMAD_SUBSETS = ['Train', 'Dev', 'Test']
THREEDMAD_SUBSETS_CORRESPONDENCE = {'Train': 'world',
                                    'Dev': 'dev',
                                    'Test': 'test'}
THREEDMAD_PAIS = {'real': 0,
                  'mask': 1}
THREEDMAD_COMMON_PAIS = {'real': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                         'mask': inter_db_cat.COMMON_PAI_CATEGORISATION['mask']['rigid']}

THREEDMAD_CAPTURE_DEVICES = {'kinect': 0}
THREEDMAD_COMMON_CAPTURE_DEVICES = {'kinect': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality']}


class ThreedmadDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        self.base_path = base_path
        self.db = bob.db.maskattack.Database(original_directory=base_path)
        self.dict_all_accesses = {}
        self.dict_all_labels = {}
        super(ThreedmadDatabase, self).__init__(base_path, annotation_base_path=annotation_base_path)

    def __str__(self):
        return super(ThreedmadDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return '3dmad'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = {'users': 17,
                     'Train videos': 105,
                     'Dev videos': 75,
                     'Test videos': 75}
        return dict_info

    @staticmethod
    def get_protocols():
        return THREEDMAD_PROTOCOLS

    @staticmethod
    def get_subsets():
        return THREEDMAD_SUBSETS

    @staticmethod
    def get_capture_devices():
        return THREEDMAD_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in THREEDMAD_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        dict_all_accesses = {'Train': [],
                             'Dev': [],
                             'Test': []}

        for subset, subset_accesses in dict_all_accesses.items():
            for access in self.db.objects(sets=THREEDMAD_SUBSETS_CORRESPONDENCE[subset]):
                path, extension = os.path.splitext(access.videofile())
                subset_accesses.append(VideoAccess(self.base_path,
                                                   path,
                                                   extension,
                                                   access_modifier=access_modifier,
                                                   annotation_base_path=self.annotation_base_path,
                                                   database_name=ThreedmadDatabase.name()))

            subset_accesses.sort(key=lambda x: x.name)

        return dict_all_accesses

    def get_all_labels(self):
        if not self.dict_all_labels:
            try:
                dict_all_labels_aggregate_db = TestResources.get_aggregated_database_all_dict_labels()
                for subset in dict_all_labels_aggregate_db:
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][ThreedmadDatabase.name()]

            except IOError:
                warnings.warn("WARNING (3dmadDatabase.get_all_labels): Labels resource file "
                              "[resources/aggregate_database_all_labels.pickle] not found. "
                              "Extracting all labels from scratch may take a while.")
                self.dict_all_labels = self._extract_all_labels_from_scratch()

        return self.dict_all_labels

    def _extract_all_labels_from_scratch(self):
        dict_all_labels = {'Train': {},
                           'Dev': {},
                           'Test': {}}

        for subset, subset_labels_dict in dict_all_labels.items():
            for obj in self.db.objects(sets=THREEDMAD_SUBSETS_CORRESPONDENCE[subset]):
                basename, extension = os.path.splitext(obj.videofile())
                access_key = basename
                subset_labels_dict[access_key] = {
                    'user': int(obj.client_id)-1,
                    'capture_device': THREEDMAD_CAPTURE_DEVICES['kinect'],
                    'session': int(obj.session),
                    'common_capture_device': THREEDMAD_COMMON_CAPTURE_DEVICES['kinect'],
                    'common_lightning': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled'],
                    'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(self.base_path, basename))
                    }

                if obj.is_real():
                    subset_labels_dict[access_key]['pai'] = THREEDMAD_PAIS['real']
                    subset_labels_dict[access_key]['common_pai'] = THREEDMAD_COMMON_PAIS['real']
                    subset_labels_dict[access_key]['scenario'] = subset_labels_dict[access_key]['pai']

                else:
                    subset_labels_dict[access_key]['pai'] = THREEDMAD_PAIS['mask']
                    subset_labels_dict[access_key]['common_pai'] = THREEDMAD_COMMON_PAIS['mask']
                    subset_labels_dict[access_key]['scenario'] = THREEDMAD_PAIS['mask']

        return dict_all_labels

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in THREEDMAD_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in 3DMAD protocols [{}]'
                             .format(protocol, THREEDMAD_PROTOCOLS))

        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict
