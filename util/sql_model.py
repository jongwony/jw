import os
import socket

import sqlalchemy as sa

engine = sa.create_engine(f"sqlite:///{os.path.expanduser('~/.jw.sqlite3')}")
meta = sa.MetaData()

fs = sa.Table(
    'fs', meta,
    sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
    sa.Column('filename', sa.VARCHAR(32)),
    sa.Column('tag_id', sa.INTEGER, sa.ForeignKey('tag.id')),
    sa.Column('host', sa.VARCHAR(16), default=socket.gethostname()),
    sa.Column('ltime', sa.DATETIME, server_default=sa.func.now()),
)

history = sa.Table(
    'history', meta,
    sa.Column('file_id', sa.INTEGER, sa.ForeignKey('fs.id')),
    sa.Column('tag_id', sa.INTEGER, sa.ForeignKey('tag.id')),
    sa.Column('host', sa.VARCHAR(16)),
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
