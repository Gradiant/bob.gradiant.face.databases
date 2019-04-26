#!/usr/bin/env python# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-r', '--replay-attack', type=str, dest='REPLAY_ATTACK_PATH', help='Path to replayattack database', default='/media/data/databases/BBDD/AntiSpoofing/replay-attack/Movies')
    parser.add_argument('-rm', '--replay-mobile', type=str, dest='REPLAY_MOBILE_PATH', help='Path to replaymobile database', default='/media/data/databases/BBDD/AntiSpoofing/replay-mobile/database')
    parser.add_argument('-msu', '--msu-mfsd', type=str, dest='MSU_MFSD_PATH', help='Path to msu-mfsd database', default='/media/data/databases/BBDD/AntiSpoofing/MSU_MFSD/MSU-MFSD/scene01')
    parser.add_argument('-oulu', '--oulu-npu', type=str, dest='OULU_NPU_PATH', help='Path to msu-mfsd database', default='/media/data/databases/BBDD/AntiSpoofing/OULU_NPU')
    parser.add_argument('-uvad', '--uvad', type=str, dest='UVAD_PATH', help='Path to uvad database', default='/media/data/databases/BBDD/AntiSpoofing/UVAD')

    args, unknown = parser.parse_known_args()

    dict_correspondences = {'REPLAY_ATTACK_PATH': args.REPLAY_ATTACK_PATH,
                            'REPLAY_MOBILE_PATH': args.REPLAY_MOBILE_PATH,
                            'MSU_MFSD_PATH': args.MSU_MFSD_PATH,
                            'OULU_NPU_PATH': args.OULU_NPU_PATH,
                            'UVAD_PATH': args.UVAD_PATH}

    command_line_args = ""
    print("\n>> Setting databases ...")
    for database_path in ['REPLAY_ATTACK_PATH', 'REPLAY_MOBILE_PATH', 'MSU_MFSD_PATH', 'OULU_NPU_PATH', 'UVAD_PATH']:
        command_line_args += " " + dict_correspondences[database_path]
    print(command_line_args)
    subprocess.call("bob/gradiant/face/databases/scripts/face_databases_setup_environ.sh" + command_line_args, shell=True)


if __name__ == '__script__':
    main()