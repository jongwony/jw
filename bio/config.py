import contextlib
from configparser import ConfigParser
from functools import partial
from os import path, makedirs


def join_path(*current_path):
    return path.join(script_path, *current_path)


def root_path(*p):
    root = ini.get('DEFAULT', 'root') \
           or path.join(path.expanduser('~'), 'Documents', '.jw')

    return path.join(root, *p)


# TODO: config.ini ~/.jw.ini
script_path = path.dirname(path.abspath(__file__))
ini = ConfigParser()
ini_path = join_path('config.ini')
ini.read(ini_path)

get = partial(ini.get, 'DEFAULT')
get_section = ini.get

with contextlib.suppress(FileExistsError):
    makedirs(root_path())
