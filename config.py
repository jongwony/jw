from os import path
import sys
from configparser import ConfigParser


config = ConfigParser()
ini_path = path.join(path.dirname(path.abspath(__file__)), 'config.ini')
config.read(ini_path)

module = sys.modules[__name__]

for conf in config:
    setattr(module, conf, config[conf])
