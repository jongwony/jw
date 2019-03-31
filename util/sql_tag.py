import pandas as pd

from .misc import relative_path
from .sql_model import *


def get_tags(_id):
    return pd.read_sql_query(fs.join(tag).select([
        fs.id,
        fs.filename,
        fs.host,
        tag.id,
        tag.name,
        tag.counter,
    ]).where(
        fs.id == _id
    ), engine)


def add_file_tags(filename: str, tags: list):
    with engine.begin():
        for t in tags:
            stmt = tag.select().where(tag.c.name == t)
            one = engine.execute(stmt).fetchone()
            if one:
                stmt = tag.update().where(
                    tag.c.id == one.id
                ).values(
                    counter=one.counter + 1
                )
            else:
                stmt = tag.insert().values(name=t)
            tag_id = engine.execute(stmt).lastrowid
            stmt = fs.insert().values(
                filename=relative_path(filename), tag_id=tag_id
            )
            engine.execute(stmt)


def union_tags(_id, tags):
    pass


def delete_tags(_id, tags):
    pass


def purge_tags(_id):
    pass


def search(content):
    return pd.read_sql_query(fs.join(tag).select([
        fs.id,
        fs.filename,
        fs.host,
        fs.tag_id,
        tag.name,
        tag.counter,
    ]).where(
        tag.c.name.like(f'%{content}%')
    ), engine)
