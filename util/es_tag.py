import os
import socket
from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from bio import config

es = Elasticsearch()
_biotag = None


def makebulk(directory, index, doc):
    for root, _, files in os.walk(directory):
        for filename in files:
            yield {
                '_index': index,
                '_type': doc,
                'filename': f'{filename}',
                'tags': root.split('/')[1:],
                'host': socket.gethostname(),
                'create_time': datetime.utcnow(),
            }


def load():
    return bulk(es, makebulk(config.get('root'), config.get('feature.py'),
                             config.get('_doc')))


def extract_doc(o: dict, name=None, data: str = '_source'):
    result = o[data]
    if name is not None:
        result = result.get(name)
    return result


def extract_search(o: dict, name: str = None):
    for hit in o['hits']['hits']:
        source = hit['_source']
        if name is not None:
            source = source.get(name)
        yield {hit['_id']: source}


class BioTag:
    def __init__(self):
        self.index = config.get('esidx')
        # deprecated type
        self.doc_type = '_doc'

    def change_index(self, index):
        self.index = index

    # TODO: add tag_count
    def add_file_tags(self, filename: str, tags: list):
        body = {
            'filename': filename,
            'tags': tags,
            'host': socket.gethostname(),
            'create_time': datetime.utcnow(),
        }
        return es.index(self.index, self.doc_type, body)

    def _tag_op(self, _id, tags: list, *, op: str = 'union'):
        fetch = self.get_tags(_id)
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
        return es.update(self.index, self.doc_type, _id, body)

    def union_tags(self, _id, tags):
        return self._tag_op(_id, tags, op='union')

    def delete_tags(self, _id, tags):
        return self._tag_op(_id, tags, op='difference')

    def purge_tags(self, _id):
        fetch = self.get_tags(_id)
        if not fetch['found']:
            return fetch

        return es.delete(self.index, self.doc_type, _id)

    def get_tags(self, _id):
        return es.get(self.index, self.doc_type, _id)

    def search(self, query):
        return es.search(self.index, self.doc_type, body=query)


def init():
    global _biotag
    if _biotag is None:
        _biotag = BioTag()
    return _biotag
