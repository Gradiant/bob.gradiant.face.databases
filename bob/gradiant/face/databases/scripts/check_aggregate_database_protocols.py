#!/usr/bin/env python# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import argparse
import os
import pickle

from tabulate import tabulate

from bob.gradiant.face.databases import json, AggregateDatabase, filter_labels_by_protocol
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


def has_args(args):
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active


def show_aggregate_table():
    databases = {
                 'aggregate-database (grandtest)': AggregateDatabase.info(),
                 }

    table = []
    for db in sorted(databases.keys()):
        database_row = [db, databases[db]['users'], databases[db]["Train videos"],
                        databases[db]["Dev videos"], databases[db]["Test videos"]]
        table.append(database_row)

    headers = ["Database", "Number of Users", "Train videos", "Dev videos", "Test videos"]
    print(tabulate(table, headers, tablefmt="fancy_grid"))


def get_all_dict_labels():
    filename = os.path.join(CURRENT_PATH, "../../../../../resources/aggregate_database_all_labels.pickle")
    with open(filename, 'rb') as handle:
        aggregated_database_all_dict = pickle.load(handle)
    return aggregated_database_all_dict


def show_available_protocols_on_aggregate_database_table(available_protocols):

    dict_all_labels = get_all_dict_labels()
    table = []

    name_protocols = sorted(available_protocols.keys())
    for name_protocol in name_protocols:
        protocol = available_protocols[name_protocol]
        filtered_labels = filter_labels_by_protocol(protocol,
                                                    dict_all_labels)

        database_row = [name_protocol, len(filtered_labels["Train"]), len(filtered_labels["Dev"]), len(filtered_labels["Test"])]
        table.append(database_row)

    headers = ["AggregateDatabase Protocols", "Train videos", "Dev videos", "Test videos"]
    print(tabulate(table, headers, tablefmt="fancy_grid"))


def main():
    available_protocols_list = AggregateDatabase.get_available_protocols().keys()
    available_protocols = AggregateDatabase.get_available_protocols()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-l', '--list', dest='show_list', action='store_true', help='list of available protocols')
    parser.add_argument('-p', '--protocol', dest='protocol',
                        help='It will show you the dict of a available protocol {}'.format(available_protocols_list))
    parser.add_argument('-nsd', '--no-show-datasets', dest='no_show_datasets', action='store_true', help='it will not show dataset info (on the protocol dict)')

    args = parser.parse_args()

    if not has_args(args):
        parser.print_help()
    else:
        if args.show_list:
            show_aggregate_table()
            show_available_protocols_on_aggregate_database_table(available_protocols)
        else:
            if args.protocol not in available_protocols_list:
                raise ValueError("protocol \"{}\" is not available. "
                                 "Try with {}".format(args.protocol,
                                                      available_protocols_list))
            print("{}:".format(args.protocol))
            if args.no_show_datasets:
                for subset in ["Train", "Dev", "Test"]:
                    del available_protocols[args.protocol][subset]["datasets"]
            print(json.dumps(available_protocols[args.protocol], indent=2).replace("null", "None"))


if __name__ == '__script__':
    main()


