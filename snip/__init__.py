from argparse import ArgumentParser
from os import path
from subprocess import call

from . import snippet


def join(*paths):
    script = path.dirname(path.abspath(__file__))
    return path.join(script, *paths)


def main(args=None):
    parser = ArgumentParser()
    parser.add_argument('command', type=str, help='custom snippet scripts')
    op, residual = parser.parse_known_args(args)
    try:
        getattr(snippet, op.command)(*residual)
    except AttributeError:
        call([join('scripts', f'{op}.sh'), *residual])
