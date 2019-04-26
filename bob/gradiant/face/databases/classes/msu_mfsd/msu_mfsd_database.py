#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
import warnings
import bob.db.msu_mfsd_mod
from bob.gradiant.core import Database, AccessModifier, VideoAccess
from bob.gradiant.face.databases.test.test_resources import TestResources
from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat

MSU_MFSD_PROTOCOLS = ['grandtest']
MSU_MFSD_SUBSETS = ['Train', 'Dev', 'Test']
MSU_MFSD_SUBSETS_CORRESPONDENCE = {'Train': 'train',
                                   'Dev': 'devel',
                                   'Test': 'test'}
MSU_MFSD_PAIS = {'real': 0,
                 'print': 1,   # HP Color Laserjet CP6015xh (1200x600 dpi)
                 'replay': 2}  # iPhone 5S (4", 1136x640) & iPad Air (9.7", 2048x1536)

MSU_MFSD_SCENARIOS = {'real': 0,
                      'print': 1,         # HP Color Laserjet CP6015xh (1200x600 dpi)
                      'video_mobile': 2,  # iPhone 5S (4", 1136x640)
                      'video_hd': 3}      # iPad Air (9.7", 2048x1536)

MSU_MFSD_PAI_SCENARIO_CORRESPONDENCE = {'real': MSU_MFSD_PAIS['real'],
                                        'print': MSU_MFSD_PAIS['print'],
                                        'video_hd': MSU_MFSD_PAIS['replay'],
                                        'video_mobile': MSU_MFSD_PAIS['replay']}

MSU_MFSD_COMMON_PAIS = {'real': inter_db_cat.COMMON_PAI_CATEGORISATION['real'],
                        'print': inter_db_cat.COMMON_PAI_CATEGORISATION['print']['low_quality'],
                        'video_hd': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['medium_quality'],
                        'video_mobile': inter_db_cat.COMMON_PAI_CATEGORISATION['replay']['high_quality']}

MSU_MFSD_CAPTURE_DEVICES = {'laptop': 0,  # macbook_air_webcam
                            'mobile': 1}  # nexus_5

MSU_MFSD_COMMON_CAPTURE_DEVICES = {'laptop': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['webcam']['low_quality'],
                                   'mobile': inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION['mobile']['low_quality']}


class MsuMfsdDatabase(Database):
    def __init__(self, base_path, annotation_base_path=None):
        super(MsuMfsdDatabase, self).__init__(base_path, annotation_base_path=annotation_base_path)
        self.db = bob.db.msu_mfsd_mod.Database(original_directory=base_path)
        self.dict_all_labels = {}

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
        dict_info = {'users': 35,
                     'Train videos': 80,
                     'Dev videos': 80,
                     'Test videos': 120}
        return dict_info

    @staticmethod
    def get_protocols():
        return MSU_MFSD_PROTOCOLS

    @staticmethod
    def get_subsets():
        return MSU_MFSD_SUBSETS

    @staticmethod
    def get_capture_devices():
        return MSU_MFSD_CAPTURE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = {k: v for k, v in MSU_MFSD_PAIS.items() if v is not 0}
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        dict_all_accesses = {'Train': [],
                             'Dev': [],
                             'Test': []}

        for subset, subset_accesses in dict_all_accesses.items():
            objects = self.db.objects(group=MSU_MFSD_SUBSETS_CORRESPONDENCE[subset])
            for access in objects:
                path, extension = os.path.splitext(access.videofile())
                subset_accesses.append(VideoAccess(self.base_path,
                                                   path,
                                                   extension,
                                                   access_modifier=access_modifier,
                                                   annotation_base_path=self.annotation_base_path,
                                                   database_name=MsuMfsdDatabase.name()))

            subset_accesses.sort(key=lambda x: x.name)

        return dict_all_accesses

    def get_all_labels(self):
        if not self.dict_all_labels:
            try:
                dict_all_labels_aggregate_db = TestResources.get_aggregated_database_all_dict_labels()
                for subset in dict_all_labels_aggregate_db:
                    self.dict_all_labels[subset] = dict_all_labels_aggregate_db[subset][MsuMfsdDatabase.name()]

            except IOError:
                warnings.warn("WARNING (MsuMfsdDatabase.get_all_labels): Labels resource file "
                              "[resources/aggregate_database_all_labels.pickle] not found. "
                              "Extracting all labels from scratch may take a while.")
                self.dict_all_labels = self._extract_all_labels_from_scratch()

        return self.dict_all_labels

    def _extract_all_labels_from_scratch(self):
        dict_all_labels = {'Train': {},
                           'Dev': {},
                           'Test': {}}

        for subset, subset_labels_dict in dict_all_labels.items():
            for obj in self.db.objects(group=MSU_MFSD_SUBSETS_CORRESPONDENCE[subset]):
                basename, extension = os.path.splitext(obj.videofile())

                subset_labels_dict[basename] = {
                    'user': int(obj.get_client_id()),
                    'capture_device': MSU_MFSD_CAPTURE_DEVICES[obj.get_quality()],
                    'common_capture_device': MSU_MFSD_COMMON_CAPTURE_DEVICES[obj.get_quality()],
                    'common_lightning': inter_db_cat.COMMON_LIGHTNING_CATEGORISATION['controlled'],
                    'common_face_resolution': inter_db_cat.get_common_face_resolution(os.path.join(self.base_path, basename)),
                    }

                if obj.is_real():
                    subset_labels_dict[basename]['pai'] = MSU_MFSD_PAIS['real']
                    subset_labels_dict[basename]['common_pai'] = MSU_MFSD_COMMON_PAIS['real']
                    subset_labels_dict[basename]['scenario'] = MSU_MFSD_SCENARIOS['real']
                else:
                    subset_labels_dict[basename]['pai'] = MSU_MFSD_PAI_SCENARIO_CORRESPONDENCE[obj.get_instrument()]
                    subset_labels_dict[basename]['common_pai'] = MSU_MFSD_COMMON_PAIS[obj.get_instrument()]
                    subset_labels_dict[basename]['scenario'] = MSU_MFSD_SCENARIOS[obj.get_instrument()]

        return dict_all_labels

    def get_ground_truth(self, protocol):
        gt_dict = {}

        if protocol not in MSU_MFSD_PROTOCOLS:
            raise ValueError('Protocol [{}] not available in MSU_MFSD protocols [{}]'. format(protocol,
                                                                                              MSU_MFSD_PROTOCOLS))
        dict_all_labels = self.get_all_labels()

        for subset in dict_all_labels:
            gt_dict[subset] = {}
            for basename in dict_all_labels[subset]:
                gt_dict[subset][basename] = dict_all_labels[subset][basename]['pai']

        return gt_dict
