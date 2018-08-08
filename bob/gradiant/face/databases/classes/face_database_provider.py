#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
from bob.gradiant.face.databases.classes.all_pad_databases import AllPadDatabases
from bob.gradiant.face.databases.classes.replay_attack import ReplayAttackDatabase
from bob.gradiant.face.databases.classes.replay_mobile import ReplayMobileDatabase
from bob.gradiant.face.databases.classes.msu_mfsd import MsuMfsdDatabase
from bob.gradiant.face.databases.classes.oulu_npu import OuluNpuDatabase
from bob.gradiant.face.databases.classes.uvad import UvadDatabase
from bob.gradiant.face.databases.classes.face_databases_path_correspondences import face_databases_path_correspondences
from bob.gradiant.core import DatabasesPathChecker


def get_database_from_key(key):
    if key == 'all-pad-databases':
        base_paths = {'replay-attack': os.environ[face_databases_path_correspondences['replay-attack']],
                      'replay-mobile': os.environ[face_databases_path_correspondences['replay-mobile']],
                      'msu-mfsd': os.environ[face_databases_path_correspondences['msu-mfsd']],
                      'oulu-npu': os.environ[face_databases_path_correspondences['oulu-npu']]
                      }
        database = AllPadDatabases(base_paths)
    elif key == 'replay-attack':
        database = ReplayAttackDatabase(os.environ[face_databases_path_correspondences['replay-attack']])
    elif key == 'replay-mobile':
        database = ReplayMobileDatabase(os.environ[face_databases_path_correspondences['replay-mobile']])
    elif key == 'msu-mfsd':
        database = MsuMfsdDatabase(os.environ[face_databases_path_correspondences['msu-mfsd']])
    elif key == 'oulu-npu':
        database = OuluNpuDatabase(os.environ[face_databases_path_correspondences['oulu-npu']])
    elif key == 'uvad':
        database = UvadDatabase(os.environ[face_databases_path_correspondences['uvad']])
    else:
        database = None
    return database


def check_enviorment_variable(database_key):
    if not database_key == 'all-pad-databases':
        database_path = face_databases_path_correspondences[database_key]
        if not DatabasesPathChecker.check_if_environment_is_defined_for(database_path):
            raise EnvironmentError(
                "{} must be set in order to run a experiment on the {} database".format(database_path, database_key))
    else:
        for subdatabase_key in ['replay-attack', 'replay-mobile', 'msu-mfsd', 'oulu-npu']:
            subdatabase_path = face_databases_path_correspondences[subdatabase_key]
            if not DatabasesPathChecker.check_if_environment_is_defined_for(subdatabase_path):
                raise EnvironmentError(
                    "{} must be set in order to run a experiment on the {} database".format(subdatabase_path,
                                                                                            database_key))


class FaceDatabaseProvider():

    @staticmethod
    def get(database_key):
        check_enviorment_variable(database_key)
        return get_database_from_key(database_key)
