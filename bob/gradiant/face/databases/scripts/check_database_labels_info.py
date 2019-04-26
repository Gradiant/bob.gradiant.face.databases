#!/usr/bin/env python# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import argparse
import pickle


def has_args(args):
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-db', '--database', dest='database', help='name of the database')
    parser.add_argument('-f', '--filename', dest='filename', help='output file (.pickle)')

    args = parser.parse_args()

    if not has_args(args):
        parser.print_help()
    else:
        with open(args.filename) as handle:
            loaded_data = pickle.load(handle)
            print("Info for Train subsets (first 20 values)")
            print(loaded_data['Train'][args.database].keys()[:20])


if __name__ == '__script__':
    main()


