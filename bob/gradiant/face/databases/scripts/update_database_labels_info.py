#!/usr/bin/env python# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import argparse
import pickle
import os

from bob.gradiant.face.databases import export_database_paths_from_file, show_exported_envs, get_database_from_key


def has_args(args):
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PICKLE_FILENAME = os.path.join(CURRENT_PATH, "../../../../../resources/aggregate_database_all_labels.pickle")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-db', '--database', dest='database', help='name of the database')
    args = parser.parse_args()

    if not has_args(args):
        parser.print_help()
    else:
        if os.path.isfile(PICKLE_FILENAME):
            os.remove(PICKLE_FILENAME)
            print("Old file \"{}\" was deleted".format(PICKLE_FILENAME))

        database = get_database_from_key(args.database)
        dict_all_labels = database.get_all_labels()

        with open(PICKLE_FILENAME, 'wb') as handle:
            pickle.dump(dict_all_labels, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print("Saved all labels in {}".format(PICKLE_FILENAME))


if __name__ == '__script__':
    main()