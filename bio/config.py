from os import path
from configparser import ConfigParser
from functools import partial


def join_path(*current_path):
    return path.join(script_path, *current_path)


script_path = path.dirname(path.abspath(__file__))
ini = ConfigParser()
ini_path = join_path('config.ini')
ini.read(ini_path)

get = partial(ini.get, 'DEFAULT')
get_section = ini.get
