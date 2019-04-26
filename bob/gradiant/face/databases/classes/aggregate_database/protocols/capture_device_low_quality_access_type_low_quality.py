"""
    It uses every parsed databases on AggregateDatabase and it will be evaluated with a grandtest protocol.
"""
from bob.gradiant.face.databases import AGGREGATE_DATABASE_PARSED_DATABASES


def get_datasets_list_from_subset(subset):
    datasets = []
    for dataset in AGGREGATE_DATABASE_PARSED_DATABASES:
        datasets.append({"name": dataset, "subsets": [subset]})
    return datasets


CAPTURE_DEVICE_LOW_QUALITY_ACCESS_TYPE_LOW_QUALITY_PROTOCOL = {
    'Train': {"datasets": get_datasets_list_from_subset("Train"),
              "common_categorisation": [{"category": "common_capture_device",
                                         "type": {"webcam": ["low_quality"],
                                                  "mobile":["low_quality"],
                                                  "tablet":["low_quality"],
                                                 }
                                         }]
              },
    'Dev': {"datasets": get_datasets_list_from_subset("Dev"),
            "common_categorisation": [{"category": "common_capture_device",
                                       "type": {"webcam": ["low_quality"],
                                                "mobile": ["low_quality"],
                                                "tablet": ["low_quality"],
                                                }
                                       }]
            },
    'Test': {"datasets": get_datasets_list_from_subset("Test"),
             "common_categorisation": [{"category": "common_pai",
                                        "type": {"real": [""],
                                                 "print":["low_quality"],
                                                 "replay":["low_quality"],
                                                 "mask": ["paper"],
                                                 }
                                         }]
             }
    }