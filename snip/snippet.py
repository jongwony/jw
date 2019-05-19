"""
$ bio snip func args[0] args[1] ...
"""
from subprocess import call
from tempfile import NamedTemporaryFile

import config
from . import join


def cpq(*args):
    if args:
        connection, db, *_ = args
    else:
        connection, db = config.get('dbgroup').split()

    call([join('scripts', 'cpq.sh'), connection, db])


def ed(*args):
    editor = config.get('editor')
    if args:
        connection, db, *_ = args
    else:
        connection, db = config.get('dbgroup').split()

    cmd = 'y'
    buffer = b'SET NAMES utf8mb4;'
    while cmd == 'y':
        with NamedTemporaryFile() as tf:
            filepath = tf.name
            tf.write(buffer)
            tf.flush()

            call([editor, '+set backupcopy=yes', '+set filetype=sql', filepath])
            tf.seek(0)
            buffer = tf.read()

            call([
                join('scripts', 'ed.sh'),
                connection,
                db,
                filepath,
            ])

        cmd = input('Continue[y/n]? ')
