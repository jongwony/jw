import contextlib
import os
import subprocess
import tempfile
from configparser import ConfigParser
from datetime import datetime
from operator import attrgetter

config = ConfigParser()
config.read('config.ini')

ROOT = config['DEFAULT']['ROOT']
EDITOR = config['DEFAULT'].get('EDITOR', os.environ.get('EDITOR', 'vim'))

with contextlib.suppress(FileExistsError):
    os.makedirs(ROOT)


class BioFile:
    def __init__(self, path):
        self.path = path
        self.meta = os.stat(path)
        self.content = None

        # with open(path) as f:
        #     view_char = config['DEFAULT'].get('VIEW_CHAR', 15)
        #     with contextlib.suppress(UnicodeDecodeError):
        #         self.content = f.read().strip()[:view_char]

    def __repr__(self):
        return f'<{self.path}, {datetime.fromtimestamp(self.meta.st_mtime)}>'


def get_meta(root_dir: str) -> list:
    meta = []
    for root, _, files in os.walk(root_dir):
        for filename in files:
            path = f'{root}/{filename}'
            meta.append(BioFile(path))
    return sorted(meta, key=attrgetter('meta.st_mtime'), reverse=True)


def temp(category: str = 'md') -> str:
    suffix = config['CATEGORY'].get(category, category)
    with tempfile.NamedTemporaryFile(suffix=f'.{suffix}', dir=ROOT,
                                     delete=False) as tf:
        tf.write(config['TEMPLATE'][category])
        tf.flush()

        subprocess.call([EDITOR, tf.name])

        edited = tf.read()

    return edited
