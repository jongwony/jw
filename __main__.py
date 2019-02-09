import argparse

import bio
from util import tag, img


def temp():
    def func(category, **kwargs):
        try:
            filename, content = bio.temp(category)
            print(f'Saved {filename}')
        except ValueError:
            return
        else:
            tags = input('Tags<space>: ').split()
            es_result = tag.add_file_tag('bio', filename, tags)
            return es_result

    p = subparsers.add_parser(temp.__name__)
    p.add_argument('--category', type=str, default='md')
    p.add_argument('--filename', type=str)
    p.set_defaults(func=func)


def imgcat():
    def func(content, inline=1, resize=None, **kwargs):
        if resize is not None:
            content = img.buffer_resize(content, resize)
        print(img.iterm2_img_format(content, inline).decode())

    p = subparsers.add_parser(imgcat.__name__)
    p.add_argument('content', type=str)
    p.add_argument('--resize', nargs=2, type=int)
    p.add_argument('--inline', type=int, default=1)
    p.set_defaults(func=func)


if __name__ == '__main__':
    version_string = ''
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # TODO: Enhance Modularization
    temp()
    imgcat()
    namespace = parser.parse_args()
    namespace.func(**vars(namespace))
