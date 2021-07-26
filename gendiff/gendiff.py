from gendiff.Parser import parse_files
from gendiff.format_stylish import stylish_diff
from gendiff.format_plain import plain_diff
from gendiff.format_json import json_diff
from gendiff.make_diff import make_diff


def generate_diff(file1, file2, format_='stylish'):
    file1, file2 = parse_files(file1, file2)
    diff = make_diff(file1, file2)['MAIN']
    if format_ == 'stylish':
        return stylish_diff(diff)
    if format_ == 'plain':
        return plain_diff(diff)
    if format_ == 'json':
        return json_diff(diff)