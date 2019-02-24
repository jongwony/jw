import json

import requests
from requests.auth import HTTPBasicAuth

from bio.config import join_path


def api_url(path, **kwargs):
    """only url kwargs"""
    host = 'http://wantedlab.atlassian.net'
    # expand=body.storage
    return host + path.format(**kwargs)


def load(file='confluence_api.json'):
    with open(join_path(file)) as f:
        data = json.load(f)
    return data


def get(_id, *key):
    for d in load():
        if _id == d['_id']:
            return [d[k] for k in key]


def search_doc(k):
    # TODO: vim vmore and hlsearch
    for d in load():
        if k in d['_id'] or k in d['path'] or k in d['body']:
            print(f'***** {d["_id"]} *****')
            print(d['name'], d['path'])
            print(d['body'].partition('.')[0])


def get_help(_id):
    # TODO: vmore
    print(get(_id, 'body'))


def api_call(_id, *, url_param=None, req_param=None):
    if url_param is None:
        url_param = {}
    if req_param is None:
        req_param = {}
    jira_auth = load('jira_auth.json')
    name, path = get(_id, 'name', 'path')
    response = requests.request(name, api_url(path, **url_param), **req_param,
                                auth=HTTPBasicAuth(jira_auth['username'],
                                                   jira_auth['token']))
    return json.loads(response.content)


def get_content(key):
    data = api_call('Get content by ID', url_param={'id': key},
                    req_param={'params': {'expand': 'body.storage'}})
    return data['body']['storage']['value']


def all_contents():
    return api_call('Get content')


def search(cql):
    return api_call('Search', req_param={'params': {'cql': cql}})


def my_post():
    data = search('creator=currentUser()')
    for d in data['results']:
        if d.get('content') and d['content']['type'] == 'page':
            print(f'***** {d["content"]["id"]} *****')
            print(d['content']['title'])
            print(api_url('/wiki' + d['url']))
            print(d['lastModified'])
