#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

from bob.gradiant.core import Database, AccessModificator
from bob.gradiant.face.databases.classes.replay_attack import ReplayAttackDatabase
from bob.gradiant.face.databases.classes.replay_mobile import ReplayMobileDatabase
from bob.gradiant.face.databases.classes.msu_mfsd import MsuMfsdDatabase
from bob.gradiant.face.databases.classes.oulu_npu import OuluNpuDatabase

ALL_PROTOCOLS = ['grandtest']
ALL_SUBSETS = ['Train', 'Dev', 'Test']
ALL_CONVENTION = {'real': 0,
                  'print': 1,
                  'print1': 1,
                  'print2': 1,
                  'mobile': 2,
                  'highdef': 3,
                  'mattescreen': 4,
                  'video_hd': 5,
                  'video_mobile': 6,
                  'video-replay': 7,
                  'video-replay1': 7,
                  'video-replay2': 7
                  }
DATABASE_PROTOCOLS = {
    'replay-attack': 'grandtest',
    'replay-mobile': 'grandtest',
    'msu-mfsd': 'grandtest',
    'oulu-npu': 'grandtest'
}


class AllPadDatabases(Database):
    def __init__(self, base_path):
        if not isinstance(base_path, dict):
            raise IOError('For AllDatabase a dict with every base paths are required')
        super(AllPadDatabases, self).__init__(base_path['replay-attack']) #only for fit the interfacegit
        self.included_databases = {
            'replay-attack': ReplayAttackDatabase(base_path['replay-attack']),
            'replay-mobile': ReplayMobileDatabase(base_path['replay-mobile']),
            'msu-mfsd': MsuMfsdDatabase(base_path['msu-mfsd']),
            'oulu-npu': OuluNpuDatabase(base_path['oulu-npu'])
        }

    def __str__(self):
        return super(AllPadDatabases, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'all-pad-databases'

    @staticmethod
    def is_a_collection_of_databases():
        return True

    @staticmethod
    def info():
        list_of_dicts = [ReplayAttackDatabase.info(), ReplayMobileDatabase.info(), MsuMfsdDatabase.info(), OuluNpuDatabase.info()]
        dict_info = {'users' : sum([x['users'] for x in list_of_dicts]),
                     'Train samples': sum([x['Train samples'] for x in list_of_dicts]),
                     'Dev samples': sum([x['Dev samples'] for x in list_of_dicts]),
                     'Test samples': sum([x['Test samples'] for x in list_of_dicts]),
                    }
        return dict_info

    @staticmethod
    def get_protocols():
        return ALL_PROTOCOLS

    @staticmethod
    def get_subsets():
        return ALL_SUBSETS

    def get_all_accesses(self, access_modificator=AccessModificator()):
        dict_all_accesses = {'All': []}

        for database in self.included_databases.itervalues():
            dict_all_accesses_one_database = database.get_all_accesses(access_modificator)
            for key in dict_all_accesses_one_database.keys():
                dict_all_accesses['All'] += dict_all_accesses_one_database[key]

        return dict_all_accesses

    def get_ground_truth(self, protocol):
        dict_files = {}

        if protocol not in ALL_PROTOCOLS:
            return dict_files

        dict_files['Train'] = self.__get_subset_labels('Train')
        dict_files['Dev'] = self.__get_subset_labels('Dev')
        dict_files['Test'] = self.__get_subset_labels('Test')

        return dict_files

    def get_attack_dict(self):
        attack_dict = {k: v for k, v in ALL_CONVENTION.iteritems() if v is not 0}
        return attack_dict

    def __get_subset_labels(self, subset):
        group_label_dict = {}

        for name, db in self.included_databases.iteritems():
            sub_db_gt = db.get_ground_truth(DATABASE_PROTOCOLS[name])[subset]
            sub_db_gt = {k: self.__translate_subdb_attack(db.get_attack_dict(), v) for k, v in sub_db_gt.iteritems()}
            group_label_dict.update(sub_db_gt)

        return group_label_dict

    def __translate_subdb_attack(self, convention, attack):

        if attack == 0:
            return 0

        for k, v in convention.iteritems():
            if v == attack:
                db_key = k
                break

        return ALL_CONVENTION[db_key]