import pytest
from gendiff.make_diff import generate_diff
from gendiff.Parser import str_replace


@pytest.fixture
def get_files():
    file1 = 'tests/fixtures/file1.json'
    file2 = 'tests/fixtures/file2.json'
    return file1, file2


@pytest.fixture
def get_yml_files():
    file1 = 'tests/fixtures/file1.yml'
    file2 = 'tests/fixtures/file2.yaml'
    return file1, file2


@pytest.fixture
def get_r_files():
    file1 = 'tests/fixtures/file3.json'
    file2 = 'tests/fixtures/file4.json'
    return file1, file2


@pytest.fixture
def get_r_yml_files():
    file1 = 'tests/fixtures/file3.yml'
    file2 = 'tests/fixtures/file4.yaml'
    return file1, file2


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


@pytest.fixture
def get_plain_expectation():
    expect = 'tests/fixtures/plain_expectation.txt'
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


def test_diff_create(get_files, get_yml_files, get_expectation):
    file1, file2 = get_files
    file3, file4 = get_yml_files
    assert generate_diff(file1, file2) == get_expectation
    assert generate_diff(file3, file4) == get_expectation


def test_r_diff_create(get_r_files, get_r_yml_files, get_r_expectation):
    file1, file2 = get_r_files
    file3, file4 = get_r_yml_files
    assert generate_diff(file1, file2) == get_r_expectation
    assert generate_diff(file3, file4) == get_r_expectation


def test_reverse_r_diff_create(get_r_files, get_r_yml_files, get_reverse_r_expectation):
    file1, file2 = get_r_files
    file3, file4 = get_r_yml_files
    assert generate_diff(file2, file1) == get_reverse_r_expectation
    assert generate_diff(file4, file3) == get_reverse_r_expectation


def test_plain_diff_create(get_r_files, get_r_yml_files, get_plain_expectation):
    file1, file2 = get_r_files
    file3, file4 = get_r_yml_files
    assert generate_diff(file1, file2, 'plain') == get_plain_expectation
    assert generate_diff(file3, file4, 'plain') == get_plain_expectation
