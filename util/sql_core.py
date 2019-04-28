import pandas as pd

from bio import handler
from .sql_model import *


def edit(_id):
    df = pd.read_sql('files', engine)
    df.set_index('id', inplace=True)
    target = df.loc[_id]
    return target, handler.edit(target['path'])


def delete(_id):
    pass
