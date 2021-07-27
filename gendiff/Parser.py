import json
import yaml


def parse_files(first_file, second_file):
    file1 = open(first_file)
    file2 = open(second_file)
    if first_file.endswith('.json'):
        file1 = json.load(file1)
        file2 = json.load(file2)
    elif first_file.endswith(('.yml', '.yaml')):
        file1 = yaml.safe_load(file1)
        file2 = yaml.safe_load(file2)
    str_replace(file1)
    str_replace(file2)
    return {'MAIN': file1}, {'MAIN': file2}


def str_replace(tree):
    for i, v in tree.items():
        if type(v) == dict:
            str_replace(v)
        elif v is False or v is True:
            tree[i] = str(v).lower()
        elif v is None:
            tree[i] = 'null'
    return tree
