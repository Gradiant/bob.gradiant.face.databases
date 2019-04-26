from bob.gradiant.face.databases.classes.aggregate_database.protocols.protocol_utils import get_filter_dataset_by_subset


def get_category_from_adverse_train_dev():
    return [{"category": "common_capture_device",
             "type": {"webcam": ["high_quality"],
                      "mobile":["high_quality"],
                      "tablet":["high_quality"],
                      "digital_camera":["high_quality"]
                      }
            },
            {"category": "common_pai",
             "type": {"real": None,
                      "print": ["low_quality", "medium_quality"],
                      "replay": ["low_quality", "medium_quality"],
                      "mask": ["paper"]
                      }
             },
            {"category": "common_lightning",
             "type": {"controlled": None,
                      "no_info": None
                      }
             }
            ]


def get_category_from_adverse_test():
    return [{"category": "common_capture_device",
             "type": {"webcam": ["low_quality"],
                      "mobile":["low_quality"],
                      "tablet":["low_quality"],
                      "digital_camera":["low_quality"]
                      }
            },
            {"category": "common_pai",
             "type": {"real": None,
                      "print": ["high_quality"],
                      "replay": ["high_quality"],
                      "mask": ["rigid", "silicone"]
                      }
             },
            {"category": "common_lightning",
             "type": {"adverse": None
                      }
             }
            ]


def get_cross_conditions_adverse_protocol(parsed_datasets):
    protocol = {"Train": {"datasets": get_filter_dataset_by_subset("Train", parsed_datasets),
                          "common_categorisation": get_category_from_adverse_train_dev()
                          },
                "Dev": {"datasets": get_filter_dataset_by_subset("Dev", parsed_datasets),
                        "common_categorisation": get_category_from_adverse_train_dev()
                        },
                "Test": {"datasets": get_filter_dataset_by_subset("Test", parsed_datasets),
                         "common_categorisation": get_category_from_adverse_test()
                         }
                }
    return protocol


def get_category_from_optimal_train_dev():
    return [{"category": "common_capture_device",
             "type": {"webcam": ["low_quality"],
                      "mobile":["low_quality"],
                      "tablet":["low_quality"],
                      "digital_camera": ["low_quality"]
                      }
            },
            {"category": "common_pai",
             "type": {"real": None,
                      "print": ["high_quality", "medium_quality"],
                      "replay": ["high_quality", "medium_quality"],
                      "mask": ["rigid", "silicone"]
                      }
             },
            {"category": "common_lightning",
             "type": {"adverse": None,
                      "no_info": None,
                      }
             }
            ]


def get_category_from_optimal_test():
    return [{"category": "common_capture_device",
             "type": {"webcam": ["high_quality"],
                      "mobile":["high_quality"],
                      "tablet":["high_quality"],
                      "digital_camera": ["high_quality"]
                      }
            },
            {"category": "common_pai",
             "type": {"real": None,
                      "print": ["low_quality"],
                      "replay": ["low_quality"],
                      "mask": ["paper"]
                      }
             },
            {"category": "common_lightning",
             "type": {"controlled": None
                      }
             }
            ]


def get_cross_conditions_optimal_protocol(parsed_datasets):
    protocol = {"Train": {"datasets": get_filter_dataset_by_subset("Train", parsed_datasets),
                          "common_categorisation": get_category_from_optimal_train_dev()
                          },
                "Dev": {"datasets": get_filter_dataset_by_subset("Dev", parsed_datasets),
                        "common_categorisation": get_category_from_optimal_train_dev()
                        },
                "Test": {"datasets": get_filter_dataset_by_subset("Test", parsed_datasets),
                         "common_categorisation": get_category_from_optimal_test()
                         }
                }
    return protocol
