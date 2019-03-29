import sqlalchemy as sa

from .sql_model import meta

engine = sa.create_engine('sqlite:///db.sqlite3', echo=True)
meta.create_all(engine)


def get_tags(_id):
    pass


def add_file_tags(filename: str, tags: list):
    pass


def union_tags(_id, tags):
    pass


def delete_tags(_id, tags):
    pass


def purge_tags(_id):
    pass


def search(content):
    pass
