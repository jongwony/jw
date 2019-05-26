import importlib.util
from argparse import ArgumentParser


def main(args=None):
    parser = ArgumentParser()
    # TODO: subparser choice preserve help string
    parser.add_argument('command')
    parse_args, residual = parser.parse_known_args(args)
    func = importlib.import_module(parse_args.command)
    return func.main(residual)
