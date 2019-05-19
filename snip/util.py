from os import path


def join(*paths):
    script = path.dirname(path.abspath(__file__))
    return path.join(script, *paths)
