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


def update_status(out_tree, tree, tree1):
    for i, v in out_tree.items():
        if get_key(v) != 'old' and tree.get(i) is None:
            out_tree[i].update({'status': 'add'})
        if get_key(v) != 'old' and tree1.get(i) is None:
            out_tree[i].update({'status': 'remove'})


def value_is_dict(tree):
    return type(get_value(tree)) == dict


def dir_format(index, value, out, depth):
    if value.get('status') == 'add':
        out.append('{}+ {}: {}'.format((' ' * depth), index, '{'))
    elif value.get('status') == 'remove':
        out.append('{}- {}: {}'.format((' ' * depth), index, '{'))
    else:
        out.append('{}  {}: {}'.format((' ' * depth), index, '{'))


def make_diff(tree, tree1):
    if not value_is_dict(tree) and value_is_dict(tree1):
        output = tree_non_tree_diff(tree1)
        if get_value(tree):
            out_tree = str_to_tree(tree, tree1)
        else:
            out_tree = mkdir(get_key(tree), output)
    elif value_is_dict(tree) and not value_is_dict(tree1):
        output = tree_non_tree_diff(tree)
        if get_value(tree1):
            out_tree = tree_to_str(tree, tree1)
        else:
            out_tree = mkdir(get_key(tree), output)
    elif not value_is_dict(tree) and not value_is_dict(tree1):
        return mkfile(get_key(tree), get_value(tree), get_value(tree1))
    else:
        out1 = tree_to_tree_diff(tree, tree1)
        out_tree = mkdir(get_key(tree), out1)
    update_status(out_tree, tree, tree1)
    return out_tree


def stylish_diff(diff):
    out = ['{']

    def inner(diff, depth):
        for i, v in diff.items():
            if i == 'MAIN':
                inner(v, depth)
                return "\n".join(out)
            if i == 'status':
                continue
            if get_key(v) != 'old':
                dir_format(i, v, out, depth)
                new_depth = depth + 4
                inner(v, new_depth)
            elif v['old'] is None:
                out.append('{}+ {}: {}'.format((' ' * depth), i, v['new']))
            elif v['new'] is None:
                out.append('{}- {}: {}'.format((' ' * depth), i, v['old']))
            elif v['old'] == v['new']:
                out.append('{}  {}: {}'.format((' ' * depth), i, v['new']))
            else:
                if type(v['old']) is dict:
                    new_depth = depth + 4
                    out.append('{}- {}: {}'.format((' ' * depth), i, '{'))
                    inner(v['old'], new_depth)
                else:
                    out.append('{}- {}: {}'.format((' ' * depth), i, v['old']))
                if type(v['new']) is dict:
                    new_depth = depth + 4
                    out.append('{}+ {}: {}'.format((' ' * depth), i, '{'))
                    inner(v['new'], new_depth)
                else:
                    out.append('{}+ {}: {}'.format((' ' * depth), i, v['new']))
        out.append('{}'.format(' ' * (depth - 2)) + '}')
        return "\n".join(out)
    return inner(diff, 2)


def diff_create(args):
    file1, file2 = parse_files(args)
    if args['format'] == 'stylish':
        return stylish_diff(make_diff(file1, file2))
