from _cli.util import parser
from . import bio
import inspect


def main(args=None):
    for k, v in inspect.getmembers(bio, inspect.isroutine):
        if inspect.getmodule(v) is bio:
            v()

    parsed_args = parser.parse_args(args)
    print(parsed_args)
    parsed_dict = vars(parsed_args)
    func = parsed_dict.pop('func')
    func()(**parsed_dict)
