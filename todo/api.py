import os
import webbrowser
from pprint import pprint
from operator import attrgetter
from contextlib import contextmanager

import jmespath
from todoist import TodoistAPI


def help():
    webbrowser.open('https://github.com/Doist/todoist-python')


@contextmanager
def token():
    token_path = os.path.expanduser(os.path.join('~', 'Documents', '.jw', 'todoist.token'))
    with open(token_path) as f:
        yield f.read().strip()


@contextmanager
def main():
    with token() as t:
        todo = TodoistAPI(t)
    todo.sync()
    yield todo
    todo.commit()


def call(name, *args):
    kwargs = {(argv := arg.split('=', 1))[0]: argv[1] for arg in args if '=' in arg}
    args = [arg for arg in args if '=' not in arg]
    with main() as todo:
        return attrgetter(name)(todo)(*args, **kwargs)


def sample():
    with main() as todo:
        pprint(todo.state['items'][0].data)


def items(*args):
    with main() as todo:
        data = todo.state['items']
    pprint(jmespath.search(args[0], [attrgetter('data')(x) for x in data]))
