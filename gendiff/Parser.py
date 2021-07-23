import json
import yaml


def parse_files(args):
    file1 = open(args['first_file'])
    file2 = open(args['second_file'])
    if args['first_file'].endswith('.json'):
        file1 = json.load(file1)
        file2 = json.load(file2)
    elif args['first_file'].endswith(('.yml', '.yaml')):
        file1 = yaml.safe_load(file1)
        file2 = yaml.safe_load(file2)
    str_replace(file1)
    str_replace(file2)
    return file1, file2


def str_replace(tree):
    corr_str = {
        False: 'false',
        True: 'true',
    }
    for i, v in tree.items():
        if type(v) == dict:
            str_replace(v)
        elif v in corr_str.keys():
            tree[i] = corr_str[v]
    return tree
