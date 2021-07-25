import pytest
from ast import literal_eval
from gendiff.make_diff import diff_create
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
def get_r_args():
    args = 'tests/fixtures/r_json_args.txt'
    output = [lines for lines in open(args)]
    output = ''.join(output)
    return literal_eval(output)


@pytest.fixture
def get_reverse_r_args():
    args = 'tests/fixtures/reverse_r_json_args.txt'
    output = [lines for lines in open(args)]
    output = ''.join(output)
    return literal_eval(output)


@pytest.fixture
def get_expectation():
    expect = 'tests/fixtures/expectation.txt'
    output = [lines for lines in open(expect)]
    output = ''.join(output)
    return output


@pytest.fixture
def get_r_expectation():
    expect = 'tests/fixtures/r_expectation.txt'
    output = [lines for lines in open(expect)]
    output = ''.join(output)
    return output


@pytest.fixture
def get_reverse_r_expectation():
    expect = 'tests/fixtures/reverse_r_expectation.txt'
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
        'two': 'null',
        'three': 'true',
        'four': 'false'
    }


def test_diff_create(get_args, get_yml_args, get_expectation):
    assert diff_create(get_args) == get_expectation
    assert diff_create(get_yml_args) == get_expectation


def test_r_diff_create(get_r_args, get_r_expectation):
    assert diff_create(get_r_args) == get_r_expectation


def test_reverse_r_diff_create(get_reverse_r_args, get_reverse_r_expectation):
    assert diff_create(get_reverse_r_args) == get_reverse_r_expectation
