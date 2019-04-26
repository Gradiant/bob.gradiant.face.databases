"""
    It uses every parsed databases on AggregateDatabase and it will be evaluated with a grandtest protocol.
"""
from bob.gradiant.face.databases.classes.aggregate_database.protocols.protocol_utils import get_filter_dataset_by_subset


def get_cross_database_test_protocol(test_database, parsed_databases):
    train_and_dev_datasets = list(filter(lambda database: database != test_database, parsed_databases))
    protocol = {"Train": {"datasets": get_filter_dataset_by_subset("Train",
                                                                   train_and_dev_datasets)},
                "Dev": {"datasets": get_filter_dataset_by_subset("Dev",
                                                                 train_and_dev_datasets)},
                "Test": {"datasets": get_filter_dataset_by_subset("Test",
                                                                  [test_database])}}
    return protocol
