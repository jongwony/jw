"""
$ bio snip func args[0] args[1] ...
"""
from subprocess import call

from bio import config


def cpq(*args):
    if args:
        connection, db, *_ = args
    else:
        connection, db = config.get('dbgroup').split()

    call([config.join_path('scripts', 'cpq.sh'), connection, db])
