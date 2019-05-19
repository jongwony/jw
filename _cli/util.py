from argparse import ArgumentParser
from functools import wraps

parser = ArgumentParser()
subparsers = parser.add_subparsers()
subparser = None


def register(func):
    @wraps(func)
    def wrapper():
        global subparser
        subparser = subparsers.add_parser(func.__name__)
        subparser.set_defaults(func=func)
        return func()

    return wrapper


def add_argument(*a, **kw):
    def decorator(func):
        @wraps(func)
        def wrapper():
            subparser.add_argument(*a, **kw)
            return func()

        return wrapper

    return decorator
