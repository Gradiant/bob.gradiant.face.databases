#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
from bob.gradiant.face.databases.classes.aggregate_database import AggregateDatabase
from bob.gradiant.face.databases.classes.casia_fasd import CasiaFasdDatabase
from bob.gradiant.face.databases.classes.casia_surf import CasiaSurfDatabase
from bob.gradiant.face.databases.classes.csmad import CsmadDatabase
from bob.gradiant.face.databases.classes.hkbu import HkbuDatabase
from bob.gradiant.face.databases.classes.msu_mfsd import MsuMfsdDatabase
from bob.gradiant.face.databases.classes.oulu_npu import OuluNpuDatabase
from bob.gradiant.face.databases.classes.replay_attack import ReplayAttackDatabase, ReplayAttackDatabaseLite
from bob.gradiant.face.databases.classes.replay_mobile import ReplayMobileDatabase, ReplayMobileDatabaseLite
from bob.gradiant.face.databases.classes.rose_youtu import RoseYoutuDatabase
from bob.gradiant.face.databases.classes.siw import SiwDatabase
from bob.gradiant.face.databases.classes.threedmad import ThreedmadDatabase
from bob.gradiant.face.databases.classes.uvad import UvadDatabase

face_available_databases = [AggregateDatabase.name(),
                            CasiaFasdDatabase.name(),
                            CasiaSurfDatabase.name(),
                            CsmadDatabase.name(),
                            HkbuDatabase.name(),
                            MsuMfsdDatabase.name(),
                            OuluNpuDatabase.name(),
                            ReplayAttackDatabase.name(),
                            ReplayAttackDatabaseLite.name(),
                            ReplayMobileDatabase.name(),
                            ReplayMobileDatabaseLite.name(),
                            RoseYoutuDatabase.name(),
                            SiwDatabase.name(),
                            ThreedmadDatabase.name(),
                            UvadDatabase.name()]

