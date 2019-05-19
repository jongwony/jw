from argparse import ArgumentParser

from .api import *


def main(args=None):
    parser = ArgumentParser()
    parser.add_argument('command', nargs='*')
    parsed_args = parser.parse_args(args)
    func, *argument = parsed_args.command
    return eval(func)(*argument)
