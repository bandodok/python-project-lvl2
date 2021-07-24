from gendiff.make_diff import diff_create
import argparse


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        "-f", "--format", default='stylish', help='set format of output')
    args = vars(parser.parse_args())
    return diff_create(args)


if __name__ == '__main__':
    main()
