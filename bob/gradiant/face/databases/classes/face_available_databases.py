#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.face.databases.classes.all_pad_databases import AllPadDatabases
from bob.gradiant.face.databases.classes.replay_attack import ReplayAttackDatabase, ReplayAttackDatabaseLite
from bob.gradiant.face.databases.classes.replay_mobile import ReplayMobileDatabase, ReplayMobileDatabaseLite
from bob.gradiant.face.databases.classes.msu_mfsd import MsuMfsdDatabase
from bob.gradiant.face.databases.classes.oulu_npu import OuluNpuDatabase

face_available_databases = [AllPadDatabases.name(),
                            ReplayAttackDatabase.name(),
                            ReplayAttackDatabaseLite.name(),
                            ReplayMobileDatabase.name(),
                            ReplayMobileDatabaseLite.name(),
                            MsuMfsdDatabase.name(),
                            OuluNpuDatabase.name()]