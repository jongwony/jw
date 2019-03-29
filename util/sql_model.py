import sqlalchemy as sa

meta = sa.MetaData()

fs = sa.Table(
    'fs', meta,
    sa.Column('id', sa.INT, primary_key=True, autoincrement=True),
    sa.Column('filename', sa.VARCHAR(64)),
    sa.Column('tagid', sa.INT),
    sa.Column('host', sa.INT),
    sa.Column('ltime', sa.TIMESTAMP),
)

history = sa.Table(
    'history', meta,
    sa.Column('fileid', sa.ForeignKey('fs.id')),
    sa.Column('tagid', sa.ForeignKey('tag.id')),
    sa.Column('host', sa.INT),
    sa.Column('atime', sa.TIMESTAMP),
)

tag = sa.Table(
    'tag', meta,
    sa.Column('id', sa.INT, primary_key=True, autoincrement=True),
    sa.Column('name', sa.VARCHAR(64)),
    sa.Column('counter', sa.INT),
)

