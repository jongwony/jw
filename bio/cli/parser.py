import argparse
from functools import wraps


class BioParser:
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._subparsers = self._parser.add_subparsers()
        self._subparser = None
        self.version_string = ''

    def parse_args(self):
        return self._parser.parse_args()

    def print_help(self):
        return self._parser.print_help()

    def register(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            self._subparser = self._subparsers.add_parser(f.__name__)
            result = f(*args, **kwargs)
            self._subparser.set_defaults(func=result)
            return result

        return wrapper

    def add_argument(self, *args, **kwargs):
        def decorator(f):
            @wraps(f)
            def wrapper(*args_, **kwargs_):
                self._subparser.add_argument(*args, **kwargs)
                return f(*args_, **kwargs_)

            return wrapper

        return decorator

