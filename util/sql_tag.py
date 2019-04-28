import pandas as pd

from .sql_model import *


def get_tags(_id):
    init()
    return pd.read_sql_query(sa.select([
        files.c.id,
        files.c.path,
        tag.c.id,
        tag.c.name,
        tag.c.counter,
    ]).select_from(files.join(tag)).where(
        files.id == _id
    ), engine)


def add_file_tags(filename: str, tags: list):
    init()
    with engine.begin():
        file_stmt = files.insert().values(path=root_path(filename))
        file_id = engine.execute(file_stmt).lastrowid
        union_tags(file_id, tags)


def union_tags(_id, tags):
    for t in tags:
        tag_stmt = tag.select().where(tag.c.name == t)
        one = engine.execute(tag_stmt).fetchone()
        if one:
            stmt = tag.update().where(tag.c.id == one.id).values(
                counter=one.counter + 1
            )
            engine.execute(stmt)
            tag_id = one.id
        else:
            stmt = tag.insert().values(name=t)
            tag_id = engine.execute(stmt).lastrowid
        hist_stmt = history.insert().values(
            file_id=_id, tag_id=tag_id
        )
        engine.execute(hist_stmt)


def delete_tags(_id, tags):
    pass


def purge_tags(_id):
    pass


def search(content):
    init()
    return pd.read_sql_query(sa.select([
        files.c.id,
        files.c.filename,
        files.c.host,
        files.c.tag_id,
        tag.c.name,
        tag.c.counter,
    ]).select_from(files.join(tag)).where(
        tag.c.name.like(f'%{content}%')
    ), engine)


def custom_search(sql):
    init()
    return pd.read_sql(sql, engine)
