import json
from gendiff.format_stylish import get_key, new_or_old_is_dict


def dict_format(i, v, new_out):
    index1 = None
    inner_value = v
    if get_key(v) != 'old':
        index = f"  {i}"
        return index, index1, inner_value, new_out
    elif type(v['old']) is dict:
        if type(v['new']) is not dict and v['new'] is not None:
            index1 = f"+ {i}"
        index = f"- {i}"
        inner_value = v['old']
        return index, index1, inner_value, new_out
    elif type(v['new']) is dict:
        if type(v['old']) is not dict and v['old'] is not None:
            new_out.update({f"- {i}": v['old']})
        index = f"+ {i}"
        inner_value = v['new']
        return index, index1, inner_value, new_out


def file_format(i, v, new_out):
    if v['old'] == v['new']:
        index = f"  {i}"
        value = v['new']
    elif v['old'] is None:
        index = f"+ {i}"
        value = v['new']
    elif v['new'] is None:
        index = f"- {i}"
        value = v['old']
    else:
        new_out.update({f"- {i}": v['old']})
        index = f"+ {i}"
        value = v['new']
    return index, value, new_out


def json_diff(diff):

    def inner(tree):
        new_out = {}
        for i, v in tree.items():
            if get_key(v) != 'old' or new_or_old_is_dict(v):
                index, index1, inner_value, new_out = dict_format(i, v, new_out)
                new_value = inner(inner_value)
                new_out.update({index: new_value})
                if index1 == f"+ {i}":
                    new_out.update({index1: v['new']})
            else:
                index, value, new_out = file_format(i, v, new_out)
                new_out.update({index: value})
        return new_out
    output = json.dumps(inner(diff), indent=2)
    output = output.replace('"false"', 'false')
    output = output.replace('"true"', 'true')
    output = output.replace('"null"', 'null')
    return output
