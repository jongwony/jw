import os
from subprocess import call
from tempfile import NamedTemporaryFile

from bio import config

editor = config.get('editor')


def touch_temp(category, template_string):
    suffix = config.get_section('CATEGORY', category, fallback=category)

    with NamedTemporaryFile(suffix=f'.{suffix}', dir=config.root_path(),
                            delete=False) as tf:
        filepath = tf.name
        tf.write(template_string.encode())
        tf.flush()

        call([editor, '+set backupcopy=yes', filepath])

        tf.seek(0)
        edited = tf.read()

    return filepath, edited


def temp(category: str = 'md') -> tuple:
    template = config.get_section('TEMPLATE', category, fallback=None)

    if template:
        with open(config.join_path(template)) as f:
            template_string = f.read()
    else:
        template_string = ''

    filepath, edited = touch_temp(category, template_string)

    if len(edited) == len(template_string):
        print(f'Not edited! deleted temp file.')
        os.remove(filepath)
        return ()

    return filepath, edited


def edit(path):
    with open(config.root_path(path), 'a+b') as f:
        call([editor, '+set backupcopy=yes', path])
        f.seek(0)
        buffer = f.read()
    return buffer
