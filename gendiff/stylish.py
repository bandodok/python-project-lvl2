def get_key(tree):
    return next(iter(tree))


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

    def inner(tree, depth):
        for i, v in tree.items():
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
