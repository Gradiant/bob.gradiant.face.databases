from bob.gradiant.face.databases.classes import inter_database_categorisation as inter_db_cat


def filter_labels_by_protocol(protocol, dict_all_labels):
    filtered_labels = {}
    for aggregate_subset, aggregate_settings_subset_list in protocol.items():
        filtered_labels[aggregate_subset] = {}
        if aggregate_settings_subset_list:
            filtered_labels = filter_labels_by_database_and_subsets(aggregate_settings_subset_list,
                                                                    aggregate_subset, dict_all_labels,
                                                                    filtered_labels)

            filtered_labels = filter_labels_by_common_categorisation(aggregate_settings_subset_list,
                                                                     aggregate_subset, filtered_labels)
        else:  # grandtest
            filtered_labels = get_grandtest_ground_truth(aggregate_subset, dict_all_labels, filtered_labels)

    return filtered_labels


def get_grandtest_ground_truth(aggregate_subset, dict_all_labels, filtered_labels):
    for database, dict_basenames in dict_all_labels[aggregate_subset].items():
        for basename, categorisation in dict_basenames.items():
            filtered_labels[aggregate_subset][basename] = categorisation
    return filtered_labels


def filter_labels_by_database_and_subsets(aggregate_settings_subset_list, aggregate_subset, dict_all_labels,
                                          filtered_labels):

    if "datasets" not in aggregate_settings_subset_list or aggregate_settings_subset_list["datasets"] is None:
        filtered_labels = get_grandtest_ground_truth(aggregate_subset, dict_all_labels, filtered_labels)
        return filtered_labels

    for settings_subset_dict in aggregate_settings_subset_list["datasets"]:
        database_name = settings_subset_dict["name"]
        child_database_subsets = settings_subset_dict["subsets"]
        for child_subset in child_database_subsets:
            if not database_name in dict_all_labels[child_subset]:
                raise ValueError("dict_all_labels is not well formatted. Tried to access to {}".format(database_name))
            filtered_labels[aggregate_subset].update(dict_all_labels[child_subset][database_name])
    return filtered_labels


def filter_labels_by_common_categorisation(aggregate_settings_subset_list, aggregate_subset, filtered_labels):
    if "common_categorisation" not in aggregate_settings_subset_list:
        return filtered_labels

    for settings_subset_dict in aggregate_settings_subset_list["common_categorisation"]:

        category = settings_subset_dict["category"]
        type_dict = settings_subset_dict['type']

        wanted_labels = []
        for type, sub_types in type_dict.items():
            if sub_types:
                if type == 'real':
                    wanted_labels.append(inter_db_cat.COMMON_CATEGORISATION[category][type])
                else:
                    for sub_type in sub_types:
                        wanted_labels.append(inter_db_cat.COMMON_CATEGORISATION[category][type][sub_type])
            else:
                wanted_labels += inter_db_cat.AGGREGATE_DATABASE_AVAILABLE_LABELS[category][type]

        filtered_labels[aggregate_subset] = {access: access_labels
                                             for access, access_labels in filtered_labels[aggregate_subset].items()
                                             if access_labels[category] in wanted_labels}

    return filtered_labels
