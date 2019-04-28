import socket

import sqlalchemy as sa

from bio.config import root_path

engine = sa.create_engine(f"sqlite:///{root_path('.jw.sqlite3')}")
meta = sa.MetaData()

files = sa.Table(
    'files', meta,
    sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
    sa.Column('path', sa.VARCHAR(32)),
    sa.Column('ltime', sa.DATETIME, server_default=sa.func.now()),
)

history = sa.Table(
    'history', meta,
    sa.Column('file_id', sa.INTEGER, sa.ForeignKey('files.id')),
    sa.Column('tag_id', sa.INTEGER, sa.ForeignKey('tag.id')),
    sa.Column('host', sa.VARCHAR(16), default=socket.gethostname()),
    sa.Column('atime', sa.DATETIME, server_default=sa.func.now()),
)

tag = sa.Table(
    'tag', meta,
    sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
    sa.Column('name', sa.VARCHAR(64), unique=True),
    sa.Column('counter', sa.INTEGER, default=1),
    sa.Column('ltime', sa.DATETIME, server_default=sa.func.now())
)

synonym = sa.Table(
    'synonym', meta,
    sa.Column('tag_id', sa.INTEGER, sa.ForeignKey('tag.id')),
    sa.Column('name', sa.VARCHAR(64)),
    sa.Column('ctime', sa.DATETIME, server_default=sa.func.now())
)


def init():
    meta.create_all(engine)
