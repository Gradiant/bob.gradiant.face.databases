from bob.gradiant.face.databases.classes.aggregate_database.protocols.protocol_utils import get_filter_dataset_by_subset


def get_train_and_dev_categorisation(leave_out_device, available_common_capture_device_types):
    train_and_dev_types_device = list(filter(lambda device: device != leave_out_device, available_common_capture_device_types))
    type_dict = {}
    for device in train_and_dev_types_device:
        type_dict[device] = None
    return [{"category": "common_capture_device",
             "type": type_dict}]


def get_test_categorisation(device):
    return [{"category": "common_capture_device",
             "type": {device: None}}]


def get_cross_device_test_protocol(device, parsed_datasets, available_common_capture_device_types):
    train_and_dev_categorisation = get_train_and_dev_categorisation(device, available_common_capture_device_types)
    test_categorisation = get_test_categorisation(device)
    protocol = {"Train": {"datasets": get_filter_dataset_by_subset("Train", parsed_datasets),
                          "common_categorisation": train_and_dev_categorisation
                          },
                "Dev": {"datasets": get_filter_dataset_by_subset("Dev", parsed_datasets),
                        "common_categorisation": train_and_dev_categorisation
                        },
                "Test": {"datasets": get_filter_dataset_by_subset("Test", parsed_datasets),
                         "common_categorisation": test_categorisation
                         }
                }
    return protocol
