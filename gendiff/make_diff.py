from gendiff.Parser import parse_files


def mkfile(key, old_value=None, new_value=None):
    return {key: {'old': old_value, 'new': new_value}}


def mkdir(key, value, status=None):
    if not status:
        return {key: value}
    return {key: value, 'status': status}


def get_value(tree):
    try:
        return next(iter(tree.values()))
    except Exception:
        return None


def get_key(tree):
    try:
        return next(iter(tree))
    except Exception:
        return None


def tree_non_tree_diff(tree):
    out = {}
    for i, q in get_value(tree).items():
        new_tree1 = {i: q}
        new_tree = {i: q}
        out.update(make_diff(new_tree, new_tree1))
    out1 = {}
    keys = list(out.keys())
    keys.sort()
    for i in keys:
        out1.update({i: out[i]})
    return out1


def tree_to_tree_diff(tree, tree1):
    out = {}
    for i, q in get_value(tree).items():
        new_tree = {i: q}
        new_tree1 = {i: get_value(tree1).get(i)}
        out.update(make_diff(new_tree, new_tree1))
    for i, q in get_value(tree1).items():
        new_tree = {i: get_value(tree).get(i)}
        new_tree1 = {i: q}
        dif = make_diff(new_tree, new_tree1)
        if get_key(dif) not in out:
            out.update(dif)
    out1 = {}
    keys = list(out.keys())
    keys.sort()
    for i in keys:
        out1.update({i: out[i]})
    return out1


def tree_to_str(tree, tree1):
    value = get_value(get_value(tree))
    key = get_key(get_value(tree))
    out = mkfile(get_key(tree), mkfile(key, value, value), get_value(tree1))
    return out


def str_to_tree(tree, tree1):
    value = get_value(get_value(tree1))
    key = get_key(get_value(tree1))
    out = mkfile(get_key(tree), get_value(tree), mkfile(key, value, value))
    return out


def value_is_dict(tree):
    return type(get_value(tree)) == dict


def make_diff(tree, tree1):
    if not value_is_dict(tree) and value_is_dict(tree1):
        output = tree_non_tree_diff(tree1)
        if get_value(tree):
            out_tree = str_to_tree(tree, tree1)
        else:
            out_tree = mkfile(get_key(tree), get_value(tree), output)
    elif value_is_dict(tree) and not value_is_dict(tree1):
        output = tree_non_tree_diff(tree)
        if get_value(tree1):
            out_tree = tree_to_str(tree, tree1)
        else:
            out_tree = mkfile(get_key(tree), output, get_value(tree1))
    elif not value_is_dict(tree) and not value_is_dict(tree1):
        return mkfile(get_key(tree), get_value(tree), get_value(tree1))
    else:
        out1 = tree_to_tree_diff(tree, tree1)
        out_tree = mkdir(get_key(tree), out1)

    return out_tree


def dict_format(i, v, depth):
    sign = None
    inner_value = v
    new_out = []
    if get_key(v) != 'old':
        new_out.append('{}  {}: {}'.format((' ' * depth), i, '{'))
    elif type(v['old']) is dict:
        if type(v['new']) is not dict and v['new'] is not None:
            sign = '+'
        new_out.append('{}- {}: {}'.format((' ' * depth), i, '{'))
        inner_value = v['old']
    elif type(v['new']) is dict:
        if type(v['old']) is not dict and v['old'] is not None:
            new_out.append('{}- {}: {}'.format((' ' * depth), i, v['old']))
        new_out.append('{}+ {}: {}'.format((' ' * depth), i, '{'))
        inner_value = v['new']
    return sign, inner_value, '\n'.join(new_out)


def file_format(i, v, depth):
    new_out = []
    if v['old'] == v['new']:
        new_out.append('{}  {}: {}'.format((' ' * depth), i, v['new']))
    elif v['old'] is None:
        new_out.append('{}+ {}: {}'.format((' ' * depth), i, v['new']))
    elif v['new'] is None:
        new_out.append('{}- {}: {}'.format((' ' * depth), i, v['old']))
    else:
        new_out.append('{}- {}: {}'.format((' ' * depth), i, v['old']))
        new_out.append('{}+ {}: {}'.format((' ' * depth), i, v['new']))
    return '\n'.join(new_out)


def new_or_old_is_dict(v):
    return type(v['old']) is dict or type(v['new']) is dict


def stylish_diff(diff):
    out = ['{']

    def inner(diff, depth):
        for i, v in diff.items():
            new_depth = depth + 4
            if get_key(v) != 'old' or new_or_old_is_dict(v):
                sign, inner_value, new_out = dict_format(i, v, depth)
                out.append(new_out)
                inner(inner_value, new_depth)
                if sign == '+':
                    out.append('{}+ {}: {}'.format((' ' * depth), i, v['new']))
            else:
                new_out = file_format(i, v, depth)
                out.append(new_out)
        out.append('{}'.format(' ' * (depth - 2)) + '}')
        return "\n".join(out)
    return inner(diff, 2)


def diff_create(args):
    file1, file2 = parse_files(args)
    if args['format'] == 'stylish':
        return stylish_diff(make_diff(file1, file2)['MAIN'])
