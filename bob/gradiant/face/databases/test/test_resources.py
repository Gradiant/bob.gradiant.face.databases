import os
import pickle

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class TestResources:

    @staticmethod
    def get_aggregated_database_all_dict_labels():
        filename = os.path.join(CURRENT_PATH, "../../../../../resources/aggregate_database_all_labels.pickle")
        with open(filename, 'rb') as handle:
            aggregated_database_all_dict = pickle.load(handle)
        return aggregated_database_all_dict
