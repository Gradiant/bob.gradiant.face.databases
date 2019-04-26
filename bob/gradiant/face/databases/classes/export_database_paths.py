import json
import os


def export_database_paths_from_file(filename):
    with open(filename) as f:
        try:
            data = json.load(f)
        except ValueError as e:
            raise IOError('Impossible to load valid information from {}. {}'.format(filename, e.message))
    if not data:
        raise IOError("Impossible to load valid information from {}".format(filename))
    return export_database_paths_from_dict(data)


def export_database_paths_from_dict(dict_database_paths):
    for key, path in dict_database_paths.items():
        if not os.path.isdir(path):
            raise IOError("Invalid path. \"{}\" path ({}) does not exist".format(key, path))
        os.environ[key] = path


def show_exported_envs():
    message = "Environment variables:\n"
    variable_template = "  - {} : {}\n"
    for key, value in os.environ.items():
        message += variable_template.format(key, value)
    print(message)

