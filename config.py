import sys
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')

module = sys.modules[__name__]

for conf in config:
    setattr(module, conf, config[conf])
