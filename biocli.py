import argparse

import bio
from util import tag, img


def imgcat(content, inline=1, resize=None):
    if resize is not None:
        content = img.buffer_resize(content, resize)
    print(img.iterm2_img_format(content, inline).decode())


def temp(category):
    try:
        filename, content = bio.temp(category)
        print(f'Saved {filename}')
    except ValueError:
        return
    else:
        tags = input('Tags<space>: ').split()
        es_result = tag.add_file_tag('bio', filename, tags)
        return es_result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--temp')
    parser.add_argument('--imgcat')
    parser.add_argument('--resize')
    parser.add_argument('--download')
    parser.add_argument('--clipboard')
    args = parser.parse_args()
    if args.temp:
        temp(args.temp)
    elif args.imgcat:
        imgcat(args.imgcat, resize=eval(args.resize) if args.resize else None)

