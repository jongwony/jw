import json

import requests
from requests.auth import HTTPBasicAuth

from bio.config import join_path


def api_url(path, **kwargs):
    """only url kwargs"""
    host = 'http://wantedlab.atlassian.net'
    return host + path.format(**kwargs)


def load(file='jira_api.json'):
    with open(join_path(file)) as f:
        data = json.load(f)
    return data


def get(_id, *key):
    for d in load():
        for m in d['method']:
            if _id == m['_id']:
                return [m[k] for k in key]


def search(k):
    # TODO: vim vmore and hlsearch
    for d in load():
        for m in d['method']:
            if k in m['_id'] or k in m['path'] or k in m['body']:
                print(f'***** {m["_id"]} *****')
                print(m['name'], m['path'])
                print(m['body'].partition('.')[0])


def get_help(_id):
    # TODO: vmore
    print(get(_id, 'body'))


def api_call(_id, url_param=None, req_param=None):
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


def get_issue(key):
    return api_call('api/2/issue-getIssue', url_param={'issueIdOrKey': key})
