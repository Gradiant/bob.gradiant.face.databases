from bob.gradiant.face.databases.classes.aggregate_database.protocols.protocol_utils import get_filter_dataset_by_subset


def get_category_from_a_pai(selected_pai):
    return [{"category": "common_pai",
             "type": {"real": None,
                      selected_pai: None
                      }
             }
            ]


def get_one_pai_protocol(parsed_datasets, selected_pai):
    protocol = {"Train": {"datasets": get_filter_dataset_by_subset("Train", parsed_datasets),
                          "common_categorisation": get_category_from_a_pai(selected_pai)
                          },
                "Dev": {"datasets": get_filter_dataset_by_subset("Dev", parsed_datasets),
                        "common_categorisation": get_category_from_a_pai(selected_pai)
                        },
                "Test": {"datasets": get_filter_dataset_by_subset("Test", parsed_datasets),
                         "common_categorisation": get_category_from_a_pai(selected_pai)
                         }
                }
    return protocol
