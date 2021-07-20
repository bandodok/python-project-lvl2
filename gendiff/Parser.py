import json
import yaml


def parse_files(args):
    if args['first_file'].endswith('.json'):
        file1 = json.load(open(args['first_file']))
        file2 = json.load(open(args['second_file']))
        return file1, file2
    elif args['first_file'].endswith(('.yml', '.yaml')):
        file1 = yaml.safe_load(open(args['first_file']))
        file2 = yaml.safe_load(open(args['second_file']))
        return file1, file2
