#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import warnings
import copy
from bob.gradiant.core import Database, AccessModifier

from bob.gradiant.face.databases.classes.aggregate_database.parsed_databases import AGGREGATE_SUBSETS

from bob.gradiant.face.databases.classes.aggregate_database.protocol_checker import protocol_checker
from bob.gradiant.face.databases.classes.aggregate_database.filter_labels_by_protocol import filter_labels_by_protocol
from bob.gradiant.face.databases.classes.aggregate_database.protocols.cross_conditions import \
    get_cross_conditions_optimal_protocol, get_cross_conditions_adverse_protocol
from bob.gradiant.face.databases.classes.aggregate_database.protocols.cross_device import get_cross_device_test_protocol
from bob.gradiant.face.databases.classes.aggregate_database.protocols.cross_device_and_face_resolution import \
    get_cross_device_and_face_resolution_protocol
from bob.gradiant.face.databases.classes.aggregate_database.protocols.cross_face_resolution import \
    get_cross_face_resolution_protocol
from bob.gradiant.face.databases.classes.aggregate_database.protocols.grandtest import get_grandtest_protocol
from bob.gradiant.face.databases.classes.aggregate_database.protocols.cross_dataset import \
    get_cross_database_test_protocol
from bob.gradiant.face.databases.classes.aggregate_database.protocols.one_pai import get_one_pai_protocol

from bob.gradiant.face.databases.classes.casia_fasd import CasiaFasdDatabase
from bob.gradiant.face.databases.classes.casia_surf import CasiaSurfDatabase
from bob.gradiant.face.databases.classes.csmad import CsmadDatabase
from bob.gradiant.face.databases.classes.hkbu import HkbuDatabase
from bob.gradiant.face.databases.classes.msu_mfsd import MsuMfsdDatabase
from bob.gradiant.face.databases.classes.replay_attack import ReplayAttackDatabase
from bob.gradiant.face.databases.classes.replay_mobile import ReplayMobileDatabase
from bob.gradiant.face.databases.classes.rose_youtu import RoseYoutuDatabase
from bob.gradiant.face.databases.classes.oulu_npu import OuluNpuDatabase
from bob.gradiant.face.databases.classes.siw import SiwDatabase
from bob.gradiant.face.databases.classes.threedmad import ThreedmadDatabase
from bob.gradiant.face.databases.classes.uvad import UvadDatabase

from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat
from bob.gradiant.face.databases.test.test_resources import TestResources

ALL_DATABASE_PROTOCOLS = {'casia-fasd': 'grandtest',
                          'casia-surf': 'grandtest',
                          'csmad': 'grandtest',
                          'hkbu': 'grandtest',
                          'msu-mfsd': 'grandtest',
                          'oulu-npu': 'grandtest',
                          'replay-attack': 'grandtest',
                          'replay-mobile': 'grandtest',
                          'rose-youtu': 'grandtest',
                          'siw': 'protocol_1',
                          '3dmad': 'grandtest',
                          'uvad': 'grandtest'}


class AggregateDatabase(Database):

    def __init__(self, base_path):
        if not isinstance(base_path, dict):
            raise IOError('For AggregateDatabase a dict with every base paths are required')
        super(AggregateDatabase, self).__init__(base_path['replay-attack'])  # only for fit the interface

        self.included_databases = {
            'casia-fasd': CasiaFasdDatabase(base_path['casia-fasd']),
            'casia-surf': CasiaSurfDatabase(base_path['casia-surf']),
            'csmad': CsmadDatabase(base_path['csmad']),
            'hkbu': HkbuDatabase(base_path['hkbu']),
            'msu-mfsd': MsuMfsdDatabase(base_path['msu-mfsd']),
            'oulu-npu': OuluNpuDatabase(base_path['oulu-npu']),
            'replay-attack': ReplayAttackDatabase(base_path['replay-attack']),
            'replay-mobile': ReplayMobileDatabase(base_path['replay-mobile']),
            'rose-youtu': RoseYoutuDatabase(base_path['rose-youtu']),
            'siw': SiwDatabase(base_path['siw']),
            '3dmad': ThreedmadDatabase(base_path['3dmad']),
            'uvad': UvadDatabase(base_path['uvad'])}

        self.set_dict_all_labels()
        self.protocols = AggregateDatabase.get_available_protocols()

    def set_new_custom_protocol(self, new_protocol_dict):
        """
        Example:

         new_protocol_dict = {"name-protocol": PROTOCOL}

         e.g grandtest

         new_protocol_dict = {"grandtest": {"Train": None, "Dev": None, "Test": Nones}

        :param new_protocol_dict:
        :return:
        """
        for name_protocol, protocol in new_protocol_dict.items():
            protocol_checker(protocol)
            self.protocols[name_protocol] = protocol

    def __str__(self):
        return super(AggregateDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'aggregate-database'

    @staticmethod
    def get_parsed_databases():
        return list(ALL_DATABASE_PROTOCOLS)

    @staticmethod
    def get_available_protocols():

        parsed_databases = AggregateDatabase.get_parsed_databases()
        available_protocols = {"grandtest": get_grandtest_protocol()}
        for device in ['webcam', 'mobile', "digital_camera"]:
            name_protocol = "cross-device-test-{}".format(device).replace("_", "-").replace("mobile", "mobile-tablet")
            available_protocols[name_protocol] = get_cross_device_test_protocol(device,
                                                                                parsed_databases,
                                                                                inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION)

        for database in AggregateDatabase.get_parsed_databases():
            name_protocol = "cross-dataset-test-{}".format(database)
            available_protocols[name_protocol] = get_cross_database_test_protocol(database, parsed_databases)

        name_template_cross_face_res = "cross-face-resolution-train-{}-test-{}-faces"
        available_protocols[name_template_cross_face_res.format("small-and-medium",
                                                                "big")] = get_cross_face_resolution_protocol(
            ["small_face",
             "medium_face"],
            ["big_face"],
            parsed_databases)
        available_protocols[name_template_cross_face_res.format("big-and-medium",
                                                                "small")] = get_cross_face_resolution_protocol(
            ["big_face",
             "medium_face"],
            ["small_face"],
            parsed_databases)

        available_protocols["cross-conditions-optimal"] = get_cross_conditions_optimal_protocol(parsed_databases)
        available_protocols["cross-conditions-adverse"] = get_cross_conditions_adverse_protocol(parsed_databases)

        available_pais = list(inter_db_cat.COMMON_PAI_CATEGORISATION)
        for pai in available_pais:
            if pai == "real":
                continue
            available_protocols["one-pai-{}".format(pai)] = get_one_pai_protocol(parsed_databases, pai)

            # TODO: Review it. It seems filtering is not working as expected
            # available_protocols["unseen-attack-{}".format(pai)] = get_unseen_attack_protocol(parsed_databases,
            #                                                                                 pai,
            #                                                                                 available_pais)

        # Ad-hoc protocol
        available_protocols["cross-device-and-face-resolution"] = \
            get_cross_device_and_face_resolution_protocol(["small_face", "medium_face"],
                                                          ["big_face"],
                                                          ["webcam", "digital_camera"],
                                                          ["tablet", "mobile"],
                                                          parsed_databases)
        return available_protocols

    @staticmethod
    def is_a_collection_of_databases():
        return True

    @staticmethod
    def info():
        list_of_dicts = [CasiaFasdDatabase.info(), CsmadDatabase.info(), HkbuDatabase.info(),
                         MsuMfsdDatabase.info(), OuluNpuDatabase.info(), ReplayAttackDatabase.info(),
                         ReplayMobileDatabase.info(), RoseYoutuDatabase.info(), SiwDatabase.info(),
                         ThreedmadDatabase.info(), UvadDatabase.info()]

        dict_info = {'users': sum([x['users'] for x in list_of_dicts]),
                     'Train videos': sum([x['Train videos'] for x in list_of_dicts]),
                     'Dev videos': sum([x['Dev videos'] for x in list_of_dicts]),
                     'Test videos': sum([x['Test videos'] for x in list_of_dicts]),
                     }
        return dict_info

    def get_protocols(self):
        return list(self.protocols)

    @staticmethod
    def get_subsets():
        return AGGREGATE_SUBSETS

    @staticmethod
    def get_capture_devices():
        capture_devices_dict = {}

        for capt_device, subtypes in inter_db_cat.COMMON_CAPTURE_DEVICE_CATEGORISATION.items():
            for subtype, label in subtypes.items():
                capture_devices_dict['{}_{}'.format(capt_device, subtype)] = label

        return capture_devices_dict

    @staticmethod
    def get_attack_dict():
        attack_dict = {}

        for pai, subtypes in inter_db_cat.COMMON_PAI_CATEGORISATION.items():
            if pai == 'real':
                attack_dict['real'] = inter_db_cat.COMMON_PAI_CATEGORISATION['real']
            else:
                for subtype, label in subtypes.items():
                    attack_dict['{}_{}'.format(pai, subtype)] = label

        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        dict_all_accesses = {'All': []}

        for database in iter(self.included_databases.values()):
            dict_all_accesses_one_database = database.get_all_accesses(access_modifier)
            for subset in dict_all_accesses_one_database:
                subset_accesses = dict_all_accesses_one_database[subset]
                for access in subset_accesses:
                    access.database_name = database.name()
                dict_all_accesses['All'] += subset_accesses
        return dict_all_accesses

    def get_all_labels(self):
        copy_dict_all_labels = copy.deepcopy(self.dict_all_labels)
        return copy_dict_all_labels

    def set_dict_all_labels(self):
        try:
            self.dict_all_labels = TestResources.get_aggregated_database_all_dict_labels()

        except IOError:
            warnings.warn("WARNING (AggregateDatabase.get_all_labels): Labels resource file "
                          "[resources/aggregate_database_all_labels.pickle] not found. "
                          "Extracting all labels from scratch may take a while.")

            self.dict_all_labels = {'Train': {},
                                    'Dev': {},
                                    'Test': {}}

            for name, db in self.included_databases.items():
                dict_all_labels_one_database = db.get_all_labels()
                for subset in dict_all_labels_one_database:
                    self.dict_all_labels[subset][name] = dict_all_labels_one_database[subset]

    def get_ground_truth(self, protocol_key):
        if protocol_key not in list(self.protocols):
            raise ValueError('Protocol [{}] not available in AggregateDatabase protocols [{}]'
                             .format(protocol_key, list(self.protocols)))
        gt_dict = {}
        dict_all_labels = self.get_all_labels()

        protocol = self.protocols[protocol_key]
        filtered_labels = filter_labels_by_protocol(protocol, dict_all_labels)

        for subset in filtered_labels:
            gt_dict[subset] = {}
            for basename in filtered_labels[subset]:
                gt_dict[subset][basename] = filtered_labels[subset][basename]["common_pai"]

        return gt_dict
