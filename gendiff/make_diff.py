from gendiff.Parser import parse_files


def make_diff(f1, f2):
    diff = {}
    diff.update(
        {i: {'old': f1.get(i), 'new': f2.get(i)} for i in f1})
    diff.update(
        {i: {'old': f1.get(i), 'new': f2.get(i)} for i in f2 if i not in f1})
    return dict(sorted(diff.items()))


def plain_diff(diff):
    out = ['{']
    for i in diff:
        if diff[i]['old'] == diff[i]['new']:
            out.append('    {}: {}'.format(i, diff[i]['new']))
        if diff[i]['old'] != diff[i]['new']:
            if diff[i]['old'] is None:
                out.append('  + {}: {}'.format(i, diff[i]['new']))
            elif diff[i]['new'] is None:
                out.append('  - {}: {}'.format(i, diff[i]['old']))
            else:
                out.append('  - {}: {}'.format(i, diff[i]['old']))
                out.append('  + {}: {}'.format(i, diff[i]['new']))
    out.append('}')
    return "\n".join(out)


def diff_create(args):
    file1, file2 = parse_files(args)
    return plain_diff(make_diff(file1, file2))
