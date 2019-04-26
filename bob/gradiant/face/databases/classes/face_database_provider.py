#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
from bob.gradiant.face.databases.classes.aggregate_database import AggregateDatabase
from bob.gradiant.face.databases.classes.casia_fasd import CasiaFasdDatabase
from bob.gradiant.face.databases.classes.casia_surf import CasiaSurfDatabase
from bob.gradiant.face.databases.classes.csmad import CsmadDatabase
from bob.gradiant.face.databases.classes.hkbu import HkbuDatabase
from bob.gradiant.face.databases.classes.oulu_npu import OuluNpuDatabase
from bob.gradiant.face.databases.classes.msu_mfsd import MsuMfsdDatabase
from bob.gradiant.face.databases.classes.replay_attack import ReplayAttackDatabase
from bob.gradiant.face.databases.classes.replay_mobile import ReplayMobileDatabase
from bob.gradiant.face.databases.classes.rose_youtu import RoseYoutuDatabase
from bob.gradiant.face.databases.classes.siw import SiwDatabase
from bob.gradiant.face.databases.classes.threedmad import ThreedmadDatabase
from bob.gradiant.face.databases.classes.uvad import UvadDatabase

from bob.gradiant.face.databases.classes.face_databases_path_correspondences import face_databases_path_correspondences
from bob.gradiant.core import DatabasesPathChecker


def get_database_from_key(key):
    if key == 'aggregate-database':
        base_paths = {
                      'casia-fasd': os.environ[face_databases_path_correspondences['casia-fasd']],
                      'casia-surf': os.environ[face_databases_path_correspondences['casia-surf']],
                      'csmad': os.environ[face_databases_path_correspondences['csmad']],
                      'hkbu': os.environ[face_databases_path_correspondences['hkbu']],
                      'msu-mfsd': os.environ[face_databases_path_correspondences['msu-mfsd']],
                      'oulu-npu': os.environ[face_databases_path_correspondences['oulu-npu']],
                      'replay-attack': os.environ[face_databases_path_correspondences['replay-attack']],
                      'replay-mobile': os.environ[face_databases_path_correspondences['replay-mobile']],
                      'rose-youtu': os.environ[face_databases_path_correspondences['rose-youtu']],
                      'siw': os.environ[face_databases_path_correspondences['siw']],
                      '3dmad': os.environ[face_databases_path_correspondences['3dmad']],
                      'uvad': os.environ[face_databases_path_correspondences['uvad']]
                      }
        database = AggregateDatabase(base_paths)
    elif key == 'casia-fasd':
        database = CasiaFasdDatabase(os.environ[face_databases_path_correspondences['casia-fasd']])
    elif key == 'casia-surf':
        database = CasiaSurfDatabase(os.environ[face_databases_path_correspondences['casia-surf']])
    elif key == 'csmad':
        database = CsmadDatabase(os.environ[face_databases_path_correspondences['csmad']])
    elif key == 'hkbu':
        database = HkbuDatabase(os.environ[face_databases_path_correspondences['hkbu']])
    elif key == 'msu-mfsd':
        database = MsuMfsdDatabase(os.environ[face_databases_path_correspondences['msu-mfsd']])
    elif key == 'oulu-npu':
        database = OuluNpuDatabase(os.environ[face_databases_path_correspondences['oulu-npu']])
    elif key == 'replay-attack':
        database = ReplayAttackDatabase(os.environ[face_databases_path_correspondences['replay-attack']])
    elif key == 'replay-mobile':
        database = ReplayMobileDatabase(os.environ[face_databases_path_correspondences['replay-mobile']])
    elif key == 'rose-youtu':
        database = RoseYoutuDatabase(os.environ[face_databases_path_correspondences['rose-youtu']])
    elif key == 'siw':
        database = SiwDatabase(os.environ[face_databases_path_correspondences['siw']])
    elif key == '3dmad':
        database = ThreedmadDatabase(os.environ[face_databases_path_correspondences['3dmad']])
    elif key == 'uvad':
        database = UvadDatabase(os.environ[face_databases_path_correspondences['uvad']])
    else:
        raise KeyError('Database key [{}] does not exist.'.format(key))
    return database


def check_enviorment_variable(database_key):
    if not database_key == 'aggregate-database':
        database_path = face_databases_path_correspondences[database_key]
        if not DatabasesPathChecker.check_if_environment_is_defined_for(database_path):
            raise EnvironmentError(
                "{} must be set in order to run a experiment on the {} database".format(database_path, database_key))
    else:
        for subdatabase_key in ['casia-fasd', 'casia-surf', 'csmad', 'hkbu', 'msu-mfsd', 'oulu-npu', 'replay-attack',
                                'replay-mobile', 'rose-youtu', 'siw', '3dmad', 'uvad']:
            subdatabase_path = face_databases_path_correspondences[subdatabase_key]
            if not DatabasesPathChecker.check_if_environment_is_defined_for(subdatabase_path):
                raise EnvironmentError(
                    "{} must be set in order to run a experiment on the {} database".format(subdatabase_path,
                                                                                            database_key))


class FaceDatabaseProvider:

    def __init__(self):
        pass

    @staticmethod
    def get(database_key):
        check_enviorment_variable(database_key)
        return get_database_from_key(database_key)
