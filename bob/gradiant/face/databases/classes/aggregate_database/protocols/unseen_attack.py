from bob.gradiant.face.databases.classes.aggregate_database.protocols.protocol_utils import get_filter_dataset_by_subset


def get_category_from_a_pai_train_dev(leave_out_selected_pai, available_pais):
    train_and_dev_pai = list(filter(lambda pai: pai != leave_out_selected_pai, available_pais))
    pai_dict = {}
    for pai in train_and_dev_pai:
        pai_dict[pai] = None

    return [{"category": "common_pai",
             "type": pai_dict
             }
            ]


def get_category_from_a_pai_test(selected_pai):
    return [{"category": "common_pai",
             "type": {"real": None,
                      selected_pai: None
                      }
             }
            ]


def get_unseen_attack_protocol(parsed_datasets, selected_pai, available_pais):
    protocol = {"Train": {"datasets": get_filter_dataset_by_subset("Train", parsed_datasets),
                          "common_categorisation": get_category_from_a_pai_train_dev(selected_pai, available_pais)
                          },
                "Dev": {"datasets": get_filter_dataset_by_subset("Dev", parsed_datasets),
                        "common_categorisation": get_category_from_a_pai_train_dev(selected_pai, available_pais)
                        },
                "Test": {"datasets": get_filter_dataset_by_subset("Test", parsed_datasets),
                         "common_categorisation": get_category_from_a_pai_test(selected_pai)
                         }
                }
    return protocol
