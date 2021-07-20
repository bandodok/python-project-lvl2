import pytest
import json
from ast import literal_eval
from gendiff.make_diff import make_files, make_diff, plain_diff, diff_create


@pytest.fixture
def get_args():
    args = 'tests/fixtures/args.txt'
    output = [lines for lines in open(args)]
    output = ''.join(output)
    return literal_eval(output)


@pytest.fixture
def get_files():
    f1 = 'tests/fixtures/file1.json'
    f2 = 'tests/fixtures/file2.json'
    file1 = json.load(open(f1))
    file2 = json.load(open(f2))
    return file1, file2


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


def test_make_files(get_args, get_files):
    assert make_files(get_args) == get_files


def test_make_diff(get_files, get_diff):
    f1, f2, = get_files
    assert make_diff(f1, f2) == get_diff


def test_plain_diff(get_diff, get_expectation):
    assert plain_diff(get_diff) == get_expectation


def test_diff_create(get_args, get_expectation):
    assert diff_create(get_args) == get_expectation
