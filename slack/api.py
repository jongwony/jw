import os
import webbrowser
from contextlib import contextmanager

from slacker import Slacker


def help():
    webbrowser.open('https://api.slack.com/methods')


def api(name, *args):
    token_path = os.path.expanduser(os.path.join('~', 'Documents', '.jw', 'slack.token'))
    with open(token_path) as f:
        token = f.read()
    bot = Slacker(token)
    return eval(f'bot.{name}')(*args)


