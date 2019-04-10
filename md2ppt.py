import os
import re
import shutil
import sys

from util.getch import getch
from util.img import iterm2_img_format


def transition():
    char = getch()
    os.system('clear')
    return char


if __name__ == '__main__':
    term_size = shutil.get_terminal_size()
    with open(sys.argv[1]) as f:
        data = f.read()
    split_list = re.split(r'^#', data, flags=re.MULTILINE)
    regex_img = re.compile(r'!\[.*?\]\((.*?)\)')

    os.system('clear')
    for slide in split_list:
        for sentence in regex_img.split(slide):
            try:
                sys.stdout.write(iterm2_img_format(sentence).decode())
            except Exception:
                sys.stdout.write(sentence)
            sys.stdout.flush()
        ch = transition()

    sys.stdout.write('END!')
    sys.stdout.flush()
    ch = transition()
