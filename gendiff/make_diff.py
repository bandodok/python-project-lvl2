def mkfile(key, old_value=None, new_value=None):
    return {key: {'old': old_value, 'new': new_value}}


def mkdir(key, value, status=None):
    if not status:
        return {key: value}
    return {key: value, 'status': status}


def get_value(tree):
    return next(iter(tree.values()))


def get_key(tree):
    return next(iter(tree))


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
        if get_value(tree):
            out_tree = str_to_tree(tree, tree1)
        else:
            output = tree_non_tree_diff(tree1)
            out_tree = mkfile(get_key(tree), get_value(tree), output)
    elif value_is_dict(tree) and not value_is_dict(tree1):
        if get_value(tree1):
            out_tree = tree_to_str(tree, tree1)
        else:
            output = tree_non_tree_diff(tree)
            out_tree = mkfile(get_key(tree), output, get_value(tree1))
    elif not all((value_is_dict(tree), value_is_dict(tree1))):
        return mkfile(get_key(tree), get_value(tree), get_value(tree1))
    else:
        out1 = tree_to_tree_diff(tree, tree1)
        out_tree = mkdir(get_key(tree), out1)
    return out_tree
