from bob.gradiant.face.databases.classes.aggregate_database.protocols.protocol_utils import get_filter_dataset_by_subset


def get_category_for_common_categorisation(face_resolution_list, cputure_devices_list):
    selected_face_resolution_dict = {}
    for face_resolution_type in face_resolution_list:
        selected_face_resolution_dict[face_resolution_type] = None

    selected_capture_devices = {}
    for capture_device_type in cputure_devices_list:
        selected_capture_devices[capture_device_type] = None

    return [{"category": "common_face_resolution",
             "type": selected_face_resolution_dict},
            {"category": "common_capture_device",
             "type": selected_capture_devices}
            ]


def get_cross_device_and_face_resolution_protocol(face_resolution_train_dev_list,
                                     face_resolution_test_list,
                                     capture_devices_train_dev_list,
                                     capture_devices_test_list,
                                     parsed_datasets):
    protocol = {"Train": {"datasets": get_filter_dataset_by_subset("Train", parsed_datasets),
                          "common_categorisation": get_category_for_common_categorisation(
                              face_resolution_train_dev_list,
                              capture_devices_train_dev_list)
                          },
                "Dev": {"datasets": get_filter_dataset_by_subset("Dev", parsed_datasets),
                        "common_categorisation": get_category_for_common_categorisation(face_resolution_train_dev_list,
                                                                                        capture_devices_train_dev_list)
                        },
                "Test": {"datasets": get_filter_dataset_by_subset("Test", parsed_datasets),
                         "common_categorisation": get_category_for_common_categorisation(face_resolution_test_list,
                                                                                         capture_devices_test_list)
                         }
                }

    return protocol
