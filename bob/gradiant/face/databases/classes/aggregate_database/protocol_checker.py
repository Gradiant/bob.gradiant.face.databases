from bob.gradiant.face.databases.classes.aggregate_database.parsed_databases import AGGREGATE_DATABASE_PARSED_DATABASES, \
    AGGREGATE_SUBSETS
from bob.gradiant.face.databases.classes.inter_database_categorisation import COMMON_CATEGORISATION


def protocol_checker(protocol):
    """

    This function checks the dict protocol definition.
    The following code represents how it is expected:

    protocol = {'Train':
                    {'datasets': [ {'name': 'replay-mobile', 'subsets': ['Train']},
                                    {'name': 'replay-attack', 'subsets': ['Train']} ],
                     'common_categorization': [ { 'category': 'common_attack_device',
                                                  'type': {'print': ['high_quality']
                                                 }
                                              ]
                    },
                'Dev':
                    {'datasets': [ {'name': 'replay-mobile', 'subsets': ['Dev']},
                                    {'name': 'replay-attack', 'subsets': ['Dev']} ],
                     'common_categorization': [ { 'category': 'common_attack_device',
                                                  'type': {'print': ['high_quality']
                                                 }
                                              ]
                    },
                'Test':
                    {'datasets': [ {'name': 'oulu-npu', 'subsets': ['Test']},
                                    {'name': 'oulu-npu', 'subsets': ['Test']} ],
                     'common_categorization': [ { 'category': 'common_attack_device',
                                                  'type': {'real': None,
                                                           'replay': ['low_quality'],
                                                           'mask': ['low_quality']}
                                                 }
                                              ]
                    }
                }

    The protocol above represents an experiment when is going to be trained using the test subsets of replay-mobile and
    replay-attack databases, tuned on the dev subsets of the same databases and tested on the test subset of oulu-npu.

    Note 1: if you don't define or define with None the parameter databases on each subset, it will consider that you
            want to use every parsed database. Check parsed databases in the documentation.

    Note 2: if you don't define or define with None that common_categorization on all the databases, it will consider
            that your protocol is a grandtest.

    Note 3: if datasets lists contains a non-defined dataset it will throw an exception

    Note 4: if common_categorization list contains inconsistences it will throw an exception

    :param protocol: dict
    :return:
    """

    check_subsets(protocol)

    for subset, subset_settings in protocol.items():
        check_datasets(subset_settings)
        check_common_categorization(subset_settings)


def check_subsets(protocol):
    expected_keys = ['Train', 'Dev', 'Test']
    if set(protocol.keys()) != set(expected_keys):
        raise ValueError("protocols keys must be {}".format(expected_keys))


def check_datasets(subset_settings):
    if subset_settings and 'datasets' in subset_settings.keys():
        check_value_is_a_list(subset_settings['datasets'], 'datasets must be a list of dicts. '
                                                           'If daxtasets is None or not defined it '
                                                           'will use every parsed dataset')
        if subset_settings['datasets']:
            for dict_dataset in subset_settings['datasets']:
                check_dict_dataset_format(dict_dataset)


def check_dict_dataset_format(dict_dataset):
    format_error_message = 'Every entry of the datasets list must be a dict with the following format ' \
                           '\{\"name\": \"database-name\", \"subsets\":[\"Train\"])'
    if not isinstance(dict_dataset, dict):
        raise ValueError(format_error_message)

    expected_keys = ["name", "subsets"]
    if set(dict_dataset.keys()) != set(expected_keys):
        raise ValueError(format_error_message)

    name_dataset = dict_dataset["name"]
    if not isinstance(name_dataset, str):
        raise ValueError(format_error_message)

    if name_dataset not in AGGREGATE_DATABASE_PARSED_DATABASES:
        raise ValueError('Dataset name \"{}\" is not available. '
                         'Please try with {}'.format(name_dataset, AGGREGATE_DATABASE_PARSED_DATABASES))

    for subset in dict_dataset["subsets"]:
        if subset not in AGGREGATE_SUBSETS:
            raise ValueError('Dataset subsets \"{}\" for \"{}\" dataset is not available. '
                             'Try with {}'.format(subset,
                                                  name_dataset,
                                                  AGGREGATE_SUBSETS))


def check_common_categorization(subset_settings):
    if subset_settings and 'common_categorization' in subset_settings.keys():
        check_value_is_a_list(subset_settings['common_categorization'],
                              'common_categorization must be a list of dicts. '
                              'If common_categorization is None or not defined it '
                              'will use the grandest')

        if subset_settings['common_categorization']:
            for dict_common_categorization in subset_settings['common_categorization']:
                check_dict_common_categorization_format(dict_common_categorization)


def check_dict_common_categorization_format(dict_common_categorization):
    format_error_message = 'Every entry of the common_categorization list must be a dict with the following format ' \
                           '\{\"category\": \"category-name\", \"type\":{\"valid-type\": [\"valid-sub-type\"]}) '
    if not isinstance(dict_common_categorization, dict):
        raise ValueError(format_error_message)

    expected_keys = ["category", "type"]
    if set(dict_common_categorization.keys()) != set(expected_keys):
        raise ValueError(format_error_message)

    # check category
    category_value = dict_common_categorization['category']
    if not isinstance(category_value, str):
        raise ValueError(format_error_message)
    if category_value not in COMMON_CATEGORISATION.keys():
        raise ValueError('common_categorization category \"{}\" is not available. '
                         'Please try with {}'.format(category_value, COMMON_CATEGORISATION.keys()))

    type_dict_value = dict_common_categorization['type']
    if not isinstance(type_dict_value, dict):
        raise ValueError(format_error_message)

    for type, sub_type_list in type_dict_value.items():
        if type not in COMMON_CATEGORISATION[category_value].keys():
            raise ValueError('common_categorization type \"{}\" is not available. '
                             'Please try with {}'.format(type, COMMON_CATEGORISATION[category_value].keys()))
        for sub_type in sub_type_list:
            if sub_type not in COMMON_CATEGORISATION[category_value][type].keys():
                raise ValueError('common_categorization subtype \"{}\" is not available for type \"{}\". '
                                 'Please try with {}'.format(sub_type,
                                                             type,
                                                             COMMON_CATEGORISATION[category_value].keys()))


def check_value_is_a_list(value, message=''):
    """
    It checks the integrity of a list as long as it is different than zero.
    :param value:
    :param message: error message
    :return:
    """
    if value:
        if not isinstance(value, list):
            raise ValueError(message)
