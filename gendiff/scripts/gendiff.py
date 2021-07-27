from gendiff.gendiff import generate_diff
import argparse


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        "-f", "--format", default='stylish', help='set format of output')
    args = vars(parser.parse_args())
    file1 = args['first_file']
    file2 = args['second_file']
    format_ = args['format']
    return generate_diff(file1, file2, format_)


if __name__ == '__main__':
    main()
