import json
import sys
from argparse import ArgumentParser
from functools import wraps
from subprocess import run, PIPE
from urllib.parse import urlencode

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

from bio.config import join_path, get_section


def api_url(path, **kwargs):
    """only url kwargs"""
    host = 'http://' + get_section('JIRA', 'url')
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


def search_help(k):
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


def auth(func):
    jira_auth = load('jira_auth.json')

    @wraps(func)
    def wrapper(*args, **kwargs):
        name, path, req_param = func(*args, **kwargs)
        response = requests.request(
            name, path,
            **req_param,
            auth=HTTPBasicAuth(jira_auth['username'], jira_auth['token'])
        )
        return json.loads(response.content)

    return wrapper


# https://developer.atlassian.com/cloud/jira/platform/rest/v3/#api-rest-api-3-jql-match-post
@auth
def api_call(_id, method=None, fmt_param=None, url_param=None, req_param=None):
    if fmt_param is None:
        fmt_param = {}
    if url_param is None:
        url_param = {}
    if req_param is None:
        req_param = {}

    data = get(_id, 'name', 'path')
    if not data:
        name, path = method, _id
    else:
        name, path = data
    path = api_url(path, **fmt_param) + '?' + urlencode(url_param)

    return name, path, req_param


def create_meta(project_ids=None, project_keys=None, issue_type_ids=None,
                issue_type_names=None, expand=None):
    # TODO: keyword argument delegate
    return api_call('/rest/api/3/issue/createmeta', 'get',
                    url_param={
                        'projectIds': project_ids,
                        'projectKeys': project_keys,
                        'issuetypeIds': issue_type_ids,
                        'issuetypeNames': issue_type_names,
                        'expand': expand,
                    })


def get_issue(key):
    return api_call('api/2/issue-getIssue', fmt_param={'issueIdOrKey': key})


def search(jql, method):
    return api_call('/rest/api/3/search', method, url_param={'jql': jql})


def archive(data):
    with open('test.json', 'w') as f:
        json.dump(data, f, indent=2)


def search_me():
    issues = search('assignee = currentUser() AND resolution = Unresolved',
                    method='get')
    issues = json.dumps(issues)
    return pipe_jq(issues)


def pipe_jq(data):
    p1 = run(['jq', '.issues[].key'], input=data.encode(), stdout=PIPE)
    res1 = p1.stdout.decode().split('\n')
    p2 = run(['jq', '.issues[].fields.status.name'], input=data.encode(),
             stdout=PIPE)
    res2 = p2.stdout.decode().split('\n')
    p3 = run(['jq', '.issues[].fields.summary'], input=data.encode(),
             stdout=PIPE)
    res3 = p3.stdout.decode().split('\n')
    p4 = run(['jq', '.issues[].fields.updated'], input=data.encode(),
             stdout=PIPE)
    res4 = p4.stdout.decode().split('\n')
    df = pd.DataFrame(list(zip(res1, res2, res4, res3)),
                      columns=['Key', 'Status', 'Updated', 'Summary']).applymap(
        lambda x: x.strip('"'), )
    df['Updated'] = pd.to_datetime(df['Updated'])
    return df.sort_values('Updated')


def main(func, *args):
    return eval(func)(*args)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('command', nargs='*')
    parsed_args = parser.parse_args()
    fname, *a = parsed_args.command
    sys.exit(main(fname, *a))
