import argparse

import bio
from util import tag, img


def print_image():
    img.print_image()
    pass


def temp(category):
    filename, content = bio.temp(category)
    tags = input('Tags<space>: ').split()
    es_result = tag.add_file_tag('bio', filename, tags)
    return es_result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--temp', default='md')
    args = parser.parse_args()
    for k, v in vars(args):
        k(v)


