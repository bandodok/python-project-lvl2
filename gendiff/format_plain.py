def get_key(tree):
    return next(iter(tree))


def str_replace(value):
    corr_str = ['false', 'true', 'null']
    if value in corr_str:
        return value
    if type(value) is int:
        return value
    return '\'' + str(value) + '\''


def make_values(tree):
    if type(tree['old']) is dict:
        old = '[complex value]'
    else:
        old = str_replace(tree['old'])
    if type(tree['new']) is dict:
        new = '[complex value]'
    else:
        new = str_replace(tree['new'])
    return old, new


def file_format(v, path):
    new_out = []
    old, new = make_values(v)
    path = '.'.join(path)
    if v['old'] is None:
        new_out.append(f"Property \'{path}\' was added with value: {new}")
    elif v['new'] is None:
        new_out.append(f"Property \'{path}\' was removed")
    elif v['old'] != v['new']:
        new_out.append(f"Property \'{path}\' was updated. From {old} to {new}")
    return "\n".join(new_out)


def plain_diff(diff):
    out = []

    def inner(tree, path):
        for i, v in tree.items():
            new_path = path[:]
            new_path.append(i)
            if get_key(v) != 'old':
                inner(v, new_path)
            elif v['old'] != v['new']:
                new_out = file_format(v, new_path)
                out.append(new_out)
        return "\n".join(out)
    return inner(diff, [])
