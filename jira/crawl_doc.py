import json

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from bio.config import join_path


def safe_tag(func):
    def wrapper(tag, attr):
        result = func(tag, attr)
        if not attr.startswith('_') and result is None:
            return Tag(name='div')
        return result

    return wrapper


Tag.__getattr__ = safe_tag(Tag.__getattr__)
Tag.select_one = safe_tag(Tag.select_one)


def jira():
    doc = requests.get(
        'https://docs.atlassian.com/software/jira/docs/api/REST/latest/')
    soup = BeautifulSoup(doc.content, features='html5lib')
    resources = soup.select("#content > div > div > section > div.resource")

    j = []
    for src in resources:
        d = {'resource': src.h3.get('id'), 'desc': src.p.get_text()}
        d.setdefault('method', [])
        for method in src.select('div.method'):
            name, path = method.h4.code.get_text().split('\xa0')
            d['method'].append({
                '_id': method.h4.get('id'),
                'name': name,
                'path': path,
                'body': method.select_one('.method-body').get_text(),
            })
        j.append(d)

    with open(join_path('jira_api.json'), 'w') as f:
        json.dump(j, f, indent=2)


def confluence():
    doc = requests.get(
        'https://developer.atlassian.com/cloud/confluence/rest/')
    soup = BeautifulSoup(doc.content, features='html5lib')
    sections = soup.select("section")

    j = []
    for i, sec in enumerate(sections):
        if i < 5:
            continue
        _id = sec.h3.get_text()
        try:
            name, path = sec.p.get_text().split()
        except ValueError:
            print(sec.p.get_text())
            continue
        body = sec.div.get_text()
        j.append({
            '_id': _id, 'name': name,
            'path': path, 'body': body,
        })
    with open(join_path('confluence_api.json'), 'w') as f:
        json.dump(j, f, indent=2)
