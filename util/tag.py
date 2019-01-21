import os
import socket
from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import config

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
    return bulk(es, makebulk(config.DEFAULT['root']))


def add_file_tag(index, filename: str, tags: list):
    body = {
        'filename': filename,
        'tags': tags,
        'host': socket.gethostname(),
        'create_time': datetime.utcnow(),
    }
    return es.index(index, doc_type, body)


def _tag_op(index, _id, tags: list, *, op: str = 'union'):
    fetch = get_tag(index, _id)
    if not fetch['found']:
        return fetch

    merge_tags = getattr(set(fetch['_source']['tags']), op)(set(tags))
    body = {
        'doc': {
            'tags': list(merge_tags),
            'host': socket.gethostname(),
            'update_time': datetime.utcnow(),
        }
    }
    return es.update(index, doc_type, _id, body)


def union_tag(index, _id, tags):
    return _tag_op(index, _id, tags, op='union')


def delete_tag(index, _id, tags):
    return _tag_op(index, _id, tags, op='difference')


def purge_tag(index, _id):
    fetch = get_tag(index, _id)
    if not fetch['found']:
        return fetch

    return es.delete(index, doc_type, _id)


def get_tag(index, _id):
    return es.get(index, doc_type, _id)
