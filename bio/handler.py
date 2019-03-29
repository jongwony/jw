import contextlib
import mmap
import os
import subprocess
import tempfile
from datetime import datetime
from operator import attrgetter

from bio import config
from util import es_tag


biotag = es_tag.init()
root = config.get('root')
editor = config.get('editor')
with contextlib.suppress(FileExistsError):
    os.makedirs(root)


class BioFile:
    def __init__(self):
        self._id = None
        self.path = None
        self.meta = None
        self.content = None
        self.tags = None

    def change(self, _id):
        self._id = _id
        self.tags = biotag.get_tags(self._id)
        filename = es_tag.extract_doc(self.tags, 'filename')
        self.path = config.join_path(root, filename)
        self.meta = os.stat(self.path)

    def open(self, _id):
        self.change(_id)
        with open(self.path, 'r+b') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0)) as mm:
                self.content = mm.read()
        return self

    def edit(self, _id):
        self.change(_id)
        with open(self.path, 'a+b') as f:
            subprocess.call([editor, '+set backupcopy=yes', self.path])
            f.seek(0)
            self.content = f.read()
        return self

    def __repr__(self):
        return f'<{self.tags}, {self.path}, {datetime.fromtimestamp(self.meta.st_mtime)}>'


def get_meta(root_dir: str) -> list:
    meta = []
    for dirpath, _, files in os.walk(root_dir):
        for filepath in files:
            path = f'{dirpath}/{filepath}'
            # TODO: BioFile changed
            meta.append(BioFile(path))
    return sorted(meta, key=attrgetter('meta.st_mtime'), reverse=True)


def touch_temp(category, template_string):
    suffix = config.get_section('CATEGORY', category, fallback=category)

    with tempfile.NamedTemporaryFile(suffix=f'.{suffix}', dir=root,
                                     delete=False) as tf:
        filepath = tf.name
        tf.write(template_string.encode())
        tf.flush()

        subprocess.call([editor, '+set backupcopy=yes', filepath])

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
