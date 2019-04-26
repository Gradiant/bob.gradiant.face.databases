from bob.gradiant.face.databases.classes.dummy_database.dummy_access import DummyAccess
from bob.gradiant.core import Database, TypeDatabase, AccessModifier


class DummyDatabase(Database):

    def __init__(self, base_path, type_database=TypeDatabase.SPLIT, annotation_base_path=None):
        self.base_path = base_path
        super(DummyDatabase, self).__init__(base_path,
                                            type_database=TypeDatabase.ALL_FILES_TOGETHER,
                                            annotation_base_path=annotation_base_path)

    def __str__(self, name='Database'):
        return super(DummyDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'dummy-database'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = {'users': 3,
                     'Train videos': 2,
                     'Dev videos': 2,
                     'Test videos': 2}
        return dict_info

    def get_attack_dict(self):
        return {'real': 0, 'attack': 1}

    def get_subsets(self):
        return ['Train', 'Dev', 'Test']

    def get_protocols(self):
        return ['grandtest']

    def get_capture_devices(self):
        return {'device-1': 0, 'device-2': 1}

    def get_all_accesses(self, access_modifier=AccessModifier()):
        dict_accesses_by_subset = self.get_accesses_by_subset(access_modifier)
        return dict_accesses_by_subset

    def get_accesses_by_subset(self, access_modifier=AccessModifier()):
        dict_accesses_by_subset = {}
        for subset in ['Train', 'Dev', 'Test']:
            list_accesses = []
            for number_access in range(0, 5):
                list_accesses.append(DummyAccess('base_path',
                                                 'real_' + str(number_access),
                                                 access_modifier=access_modifier,
                                                 database_name=DummyDatabase.name()))
            for number_access in range(0, 5):
                list_accesses.append(DummyAccess('base_path', 'attack_' + str(number_access),
                                                 access_modifier=access_modifier,
                                                 database_name=DummyDatabase.name()))
            list_accesses.sort(key=lambda x: x.name)
            dict_accesses_by_subset[subset] = list_accesses
        return dict_accesses_by_subset

    def get_all_labels(self):
        dict_files = {}
        for subset in ['Train', 'Dev', 'Test']:
            dict_subset = {}
            for number_access in range(0, 5):
                dict_subset['real_' + str(number_access)] = {'user': number_access,
                                                             'pai': 0,
                                                             'common_pai': 0,
                                                             'capture_device': 3,
                                                             'common_capture_device': 0,
                                                             'scenario': 3,
                                                             'light': 1}
            for number_access in range(0, 5):
                dict_subset['attack_' + str(number_access)] = {'user': number_access,
                                                               'pai': 3,
                                                               'common_pai': 2,
                                                               'capture_device': 3,
                                                               'common_capture_device': 0,
                                                               'scenario': 3,
                                                               'light': 1}
            dict_files[subset] = dict_subset
        return dict_files

    def get_ground_truth(self, protocol):
        dict_files = {}
        for subset in ['Train', 'Dev', 'Test']:
            dict_subset = {}
            for number_access in range(0, 5):
                dict_subset['real_' + str(number_access)] = self.get_attack_dict()['real']
            for number_access in range(0, 5):
                dict_subset['attack_' + str(number_access)] = self.get_attack_dict()['attack']
            dict_files[subset] = dict_subset
        return dict_files

    def get_devices_labels(self):
        pass

    def get_devices_dict(self):
        pass
