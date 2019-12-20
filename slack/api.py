import os
import webbrowser
from operator import attrgetter

from slacker import Slacker


def help():
    webbrowser.open('https://api.slack.com/methods')


def api(name, *args):
    token_path = os.path.expanduser(os.path.join('~', 'Documents', '.jw', 'slack.token'))
    with open(token_path) as f:
        token = f.read().strip()
    bot = Slacker(token)
    kwargs = {(argv := arg.split('=', 1))[0]: argv[1] for arg in args if '=' in arg}
    args = [arg for arg in args if '=' not in arg]
    return attrgetter(name)(bot)(*args, **kwargs)
