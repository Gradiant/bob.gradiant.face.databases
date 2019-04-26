#!/usr/bin/env python# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import argparse
import os

from bob.gradiant.face.databases import export_database_paths_from_file, show_exported_envs

def has_args(args):
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--file', dest='filename', help='Path to json with database\'s paths')

    args = parser.parse_args()

    if not has_args(args):
        parser.print_help()
    else:
        if not os.path.isfile(args.filename):
            raise IOError("Invalid input: \"{}\"".format(args.filename))

        export_database_paths_from_file(args.filename)
        show_exported_envs()


if __name__ == '__script__':
    main()