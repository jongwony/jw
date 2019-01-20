import os
import socket
from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


es = Elasticsearch()

# deprecated type
doc_type = '_doc'


def makebulk(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            yield {
                '_index': 'bio',
                '_type': doc_type,
                'filename': f'{filename}',
                'tags': root.split('/')[1:],
                'host': socket.gethostname(),
                'create_time': datetime.utcnow(),
            }


def load():
    bulk(es, makebulk('files'))


def add_tag(index, filename, tag):
    body = {filename: tag}
    return es.index(index, doc_type, body)


def get_tag(index, _id):
    return es.get(index, doc_type, _id)


def dump():
    pass
