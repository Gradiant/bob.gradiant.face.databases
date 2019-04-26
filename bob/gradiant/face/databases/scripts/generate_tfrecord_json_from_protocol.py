#!/usr/bin/env python# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import argparse
import os
import json
from bob.gradiant.face.databases import get_database_from_key, face_databases_path_correspondences


def has_args(args):
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active


def get_all_basepaths(database):
    all_basepath = []
    for db in database.included_databases.keys():
        all_basepath.append(os.environ[face_databases_path_correspondences[db]])
    return all_basepath


def purge_access_list(access_list, all_basepaths, extension):
    purged_list = []
    for access_path in access_list:
        for basepath in all_basepaths:
            full_path = os.path.join(basepath, access_path)+"."+extension
            if os.path.isfile(full_path):
                purged_list.append(full_path)
                break
    return purged_list


def save_output_dict(output_dict, path_to_save):
    with open(path_to_save, 'w') as ofile:
        json.dump(output_dict, ofile, indent=2, sort_keys=True)


def print_sumary_info(subset, original_list, purged_list):
    print("SUBSET: "+subset)
    print("     Original size: " + str(len(original_list)))
    print("     Found elements: " + str(len(purged_list)))


def set_databases_env_path(base_path):
    for key, value in face_databases_path_correspondences.items():
        os.environ[value] = os.path.join(base_path, key)


def create_new_protocol_dict(no_include, available_databases):
    for db in no_include:
        available_databases.remove(db)
    protocol = {'Train': {'datasets': []},
                'Dev': {'datasets': []},
                'Test': {'datasets': []}}
    for db in available_databases:
        protocol['Train']['datasets'].append({'name': db, 'subsets': ['Train']})
        protocol['Dev']['datasets'].append({'name': db, 'subsets': ['Dev']})
        protocol['Test']['datasets'].append({'name': db, 'subsets': ['Test']})
    return protocol


def main():

    available_databases = face_databases_path_correspondences.keys()

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-p', '--protocol', dest='protocol', help='name of the protocol', required=True)
    parser.add_argument('-e', '--extension', dest='extension', help='extension of tfrecords', default="tfrecord")
    parser.add_argument('-b', '--base-path', dest='base_path', help='Base path of the folder that contains all the databases. Not required')
    parser.add_argument('-n', '--no-include', dest='no_include', nargs='+', help='List of databases that will not be included')
    parser.add_argument('-f', '--json-name', dest='json_name', help='full path for the output json file', default="./tfrecord_experiment.json")
    parser.add_argument('-db', '--database', dest='database', help='Required database', default='aggregate-database',
                        choices=['aggregate-database','casia-fasd', 'casia-surf', 'csmad', 'hkbu', 'msu-mfsd', 'oulu-npu', 'replay-attack','replay-mobile', 'rose-youtu', 'siw', '3dmad', 'uvad'])
    args = parser.parse_args()

    if not has_args(args):
        parser.print_help()

    output_dict = {}
    output_dict["name"] = "{}.{}".format(args.database,args.protocol)
    output_dict["type"] = 'tf_records'
    output_dict["classes_to_ids"] = {"mask": 3, "screen": 2, "print": 1, "real": 0}

    if args.base_path is not None:
        set_databases_env_path(args.base_path)

    database = get_database_from_key(args.database)

    if args.no_include is not None:
        new_protocol = {args.protocol: create_new_protocol_dict(args.no_include, available_databases)}
        database.set_new_custom_protocol(new_protocol)

    protocols = database.get_protocols()
    if not args.protocol in protocols:
        raise RuntimeError("Selected protocol is not available")
    print("")
    print("*************** INFO *****************")
    print("")
    print("PROTOCOL: " + args.protocol)

    dict_gt = database.get_ground_truth(args.protocol)
    if args.database == 'aggregate-database':
        all_basepaths = get_all_basepaths(database)
    else:
        all_basepaths = [ os.environ[face_databases_path_correspondences[args.database]] ]
    for subset_name, gt in dict_gt.items():
        access_list = gt.keys()
        purged_list = purge_access_list(access_list, all_basepaths, args.extension)
        if subset_name == "Train":
            output_dict["n_train"] = len(purged_list)
            output_dict["train_tf_records"] = purged_list
        elif subset_name == "Dev":
            output_dict["n_eval"] = len(purged_list)
            output_dict["eval_tf_records"] = purged_list
        else:
            continue
        print_sumary_info(subset_name, access_list, purged_list)

    save_output_dict(output_dict, args.json_name)


if __name__ == '__script__':
    main()

