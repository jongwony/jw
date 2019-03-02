"""
$ bio snip func args[0] args[1] ...
"""
from subprocess import call
from tempfile import NamedTemporaryFile

from bio import config


def cpq(*args):
    if args:
        connection, db, *_ = args
    else:
        connection, db = config.get('dbgroup').split()

    call([config.join_path('scripts', 'cpq.sh'), connection, db])


def ed(*args):
    editor = config.get('editor')
    if args:
        connection, db, *_ = args
    else:
        connection, db = config.get('dbgroup').split()

    cmd = 'y'
    buffer = b''
    while cmd == 'y':
        with NamedTemporaryFile() as tf:
            filepath = tf.name
            tf.write(buffer)
            tf.flush()

            call([editor, '+set backupcopy=yes', '+set filetype=sql', filepath])
            tf.seek(0)
            buffer = tf.read()

            call([
                config.join_path('scripts', 'ed.sh'),
                connection,
                db,
                filepath,
            ])

        cmd = input('Continue[y/n]? ')
