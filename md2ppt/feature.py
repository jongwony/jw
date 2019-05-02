import os
import re
import shutil
import sys
from itertools import chain
from operator import methodcaller

from pyfiglet import print_figlet
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from imgcat.img import iterm2_img_format
from .util.getch import getch

term_size = shutil.get_terminal_size()


def code_highlight(code, lexer):
    try:
        if not lexer:
            lexer = guess_lexer(code)
        else:
            lexer = get_lexer_by_name(lexer)
    except ClassNotFound:
        lexer = TextLexer()

    return highlight(code, lexer, Terminal256Formatter())


def code_glyph(code, lexer=None, border=True):
    hl_code = code_highlight(code, lexer)
    if border:
        header = "\u2554" + '\u2550' * (term_size.columns - 2) + '\u2557\n'
        footer = "\u255A" + '\u2550' * (term_size.columns - 2) + '\u255D\n'
        wall = '\u2551'
    else:
        header = footer = ''
        wall = ' '

    hl_box = '\n'.join(
        f"{wall} {sentence}" + ' ' * (
                term_size.columns - len(origin) - 3) + f"{wall}"
        for sentence, origin in
        zip(hl_code.rstrip().split('\n'), code.rstrip().split('\n'))
    )
    return f'{header}{hl_box}{footer}'


def transition():
    char = getch()
    if char == ':':
        char = input(':')
    os.system('clear')
    return char


def pre(m, border=True):
    lexer, code = m.groups()
    if lexer in ['gv', 'graphviz']:
        from graphviz import Source
        gv = Source(code)
        sys.stdout.write(iterm2_img_format(gv.pipe('png')))
    else:
        sys.stdout.write(code_glyph(code, lexer, border))
    sys.stdout.flush()


def images(m):
    sentence = m.group(1)
    try:
        sys.stdout.write(iterm2_img_format(sentence))
    except Exception:
        sys.stdout.write(sentence)
    sys.stdout.flush()


def figlet(m):
    extra, title = m.groups()
    if extra == '':
        print_figlet(
            title, colors='WHITE:',
            width=term_size.columns, justify='center'
        )
    elif extra == '#':
        print_figlet(
            title, font='banner', colors='WHITE:',
            width=term_size.columns
        )
    else:
        print_figlet(title, font='3x5', colors='WHITE:', width=term_size.columns)


def controller(ch, cur):
    if ch == 'q':
        raise StopIteration

    if ch.isdigit():
        return int(ch)

    return cur + 1


def slideshow(md):
    global term_size
    regex_domain = {
        re.compile(r'!\[.*\]\((.*?)\)'): images,
        re.compile(r'```([a-z]*)\n([\s\S]*?)\n```'): pre,
        re.compile(r'#(#{0,5}) (.*)'): figlet,
    }

    with open(md) as f:
        data = f.read()
    split_list = re.split(r'^---$', data, flags=re.M)

    os.system('clear')
    slide_idx = 0
    while slide_idx < len(split_list):
        slide = split_list[slide_idx]
        term_size = shutil.get_terminal_size()
        print(f'slide: {slide_idx}'.rjust(term_size.columns))
        matched = chain(*[re.finditer(pattern, slide)
                          for pattern in regex_domain])
        matched = sorted(matched, key=methodcaller('start'))
        idx = 0
        for m in matched:
            sys.stdout.write(slide[idx:m.start()])
            sys.stdout.flush()
            regex_domain[m.re](m)
            idx = m.end()
        sys.stdout.write(slide[idx:])
        sys.stdout.flush()
        try:
            slide_idx = controller(transition(), slide_idx)
        except StopIteration:
            break

    sys.stdout.write('END!')
    sys.stdout.flush()
    transition()


def main():
    slideshow(sys.argv[1])
