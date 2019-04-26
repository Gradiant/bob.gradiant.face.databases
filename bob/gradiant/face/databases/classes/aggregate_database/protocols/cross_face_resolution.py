from bob.gradiant.face.databases.classes.aggregate_database.protocols.protocol_utils import get_filter_dataset_by_subset


def get_category_for_common_face_resolution(selected_face_resolution_types):
    selected_face_resolution_dict = {}
    for face_resolution_type in selected_face_resolution_types:
        selected_face_resolution_dict[face_resolution_type] = None
    return [{"category": "common_face_resolution",
            "type": selected_face_resolution_dict}]


def get_cross_face_resolution_protocol(train_dev_list, test_list, parsed_datasets):
    protocol = {"Train": {"datasets": get_filter_dataset_by_subset("Train", parsed_datasets),
                          "common_categorisation": get_category_for_common_face_resolution(train_dev_list)
                          },
                "Dev": {"datasets": get_filter_dataset_by_subset("Dev", parsed_datasets),
                        "common_categorisation": get_category_for_common_face_resolution(train_dev_list)
                        },
                "Test": {"datasets": get_filter_dataset_by_subset("Test", parsed_datasets),
                         "common_categorisation": get_category_for_common_face_resolution(test_list)
                         }
                }

    return protocol
