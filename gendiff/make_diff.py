import json
import yaml


def make_files(args):
    if args['first_file'].endswith('.json'):
        file1 = json.load(open(args['first_file']))
        file2 = json.load(open(args['second_file']))
        return file1, file2
    elif args['first_file'].endswith(('.yml', '.yaml')):
        file1 = yaml.safe_load(open(args['first_file']))
        file2 = yaml.safe_load(open(args['second_file']))
        return file1, file2


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
    file1, file2 = make_files(args)
    return plain_diff(make_diff(file1, file2))
