import pytest
import json
import yaml
from ast import literal_eval
from gendiff.make_diff import parse_files, make_diff, plain_diff, diff_create
from gendiff.Parser import str_replace


@pytest.fixture
def get_args():
    args = 'tests/fixtures/json_args.txt'
    output = [lines for lines in open(args)]
    output = ''.join(output)
    return literal_eval(output)


@pytest.fixture
def get_yml_args():
    args = 'tests/fixtures/yml_args.txt'
    output = [lines for lines in open(args)]
    output = ''.join(output)
    return literal_eval(output)


@pytest.fixture
def get_files():
    f1 = 'tests/fixtures/file1.json'
    f2 = 'tests/fixtures/file2.json'
    file1 = json.load(open(f1))
    file2 = json.load(open(f2))
    str_replace(file1)
    str_replace(file2)
    return {'MAIN': file1}, {'MAIN': file2}


@pytest.fixture
def get_yml_files():
    f1 = 'tests/fixtures/file1.yml'
    f2 = 'tests/fixtures/file2.yaml'
    file1 = yaml.safe_load(open(f1))
    file2 = yaml.safe_load(open(f2))
    str_replace(file1)
    str_replace(file2)
    return {'MAIN': file1}, {'MAIN': file2}


@pytest.fixture
def get_diff():
    diff = 'tests/fixtures/diff.txt'
    output = [lines for lines in open(diff)]
    output = ''.join(output)
    return literal_eval(output)


@pytest.fixture
def get_expectation():
    expect = 'tests/fixtures/expectation.txt'
    output = [lines for lines in open(expect)]
    output = ''.join(output)
    return output


def test_str_replace():
    new_tree = {
        'one': False,
        'two': None,
        'three': True,
        'four': 'false'
    }
    str_replace(new_tree)
    assert new_tree == {
        'one': 'false',
        'two': None,
        'three': 'true',
        'four': 'false'
    }


def test_make_files(get_args, get_files, get_yml_args, get_yml_files):
    assert parse_files(get_args) == get_files
    assert parse_files(get_yml_args) == get_yml_files


def test_make_diff(get_files, get_yml_files, get_diff):
    f1, f2, = get_files
    assert make_diff(f1, f2) == get_diff
    f1, f2, = get_yml_files
    assert make_diff(f1, f2) == get_diff


def test_plain_diff(get_diff, get_expectation):
    assert plain_diff(get_diff) == get_expectation


def test_diff_create(get_args, get_expectation):
    assert diff_create(get_args) == get_expectation
