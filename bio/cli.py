import json
import argparse
from functools import wraps

from bio import handler, snippet
from util import tag, img, query


class BioParser:
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._subparsers = self._parser.add_subparsers()
        self._subparser = None
        self.version_string = ''

    def parse_args(self):
        return self._parser.parse_args()

    def register(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            self._subparser = self._subparsers.add_parser(f.__name__)
            result = f(*args, **kwargs)
            self._subparser.set_defaults(func=result)
            return result
        return wrapper

    def add_argument(self, *args, **kwargs):
        def decorator(f):
            @wraps(f)
            def wrapper(*args_, **kwargs_):
                self._subparser.add_argument(*args, **kwargs)
                return f(*args_, **kwargs_)
            return wrapper
        return decorator


class CLIInit:
    bioparser = BioParser()

    biotag = tag.init()
    biofile = handler.BioFile()

    @classmethod
    def main(cls):
        for k in vars(cls):
            f = getattr(cls, k)
            if k != 'main' and callable(f):
                f(cls)

        namespace = cls.bioparser.parse_args()
        namespace.func(**vars(namespace))

    @bioparser.register
    @bioparser.add_argument('command', type=str, nargs='*')
    def snip(self):
        def func(command, **kwargs):
            op, *args = command
            getattr(snippet, op)(*args)
        return func

    @bioparser.register
    @bioparser.add_argument('content', type=str)
    @bioparser.add_argument('-j', '--json', dest='custom', action='store_true')
    @bioparser.add_argument('-t', '--type', dest='dsl', type=str, default='term')
    def search(self):
        def func(content: str, custom=False, dsl='term', **kwargs):
            if not custom:
                content = getattr(query, dsl)(content)
            else:
                content = json.loads(content)
            result = self.biotag.search(content)
            print(*tag.extract_search(result, 'tags'), sep='\n')
        return func

    @bioparser.register
    @bioparser.add_argument('_id', type=str)
    def edit(self):
        def func(_id, **kwargs):
            result = self.biofile.edit(_id)
            print(f'Changed {result.path}')
            print(f'Current tags: {tag.extract_doc(result.tags, "tags")}')
            tags = input('Tags<space>: ').split()
            update_tags = self.biotag.union_tags(_id, tags)
            print(f'Tag {tag.extract_doc(update_tags, data="result")}')
        return func

    @bioparser.register
    @bioparser.add_argument('category', nargs='?', default='md')
    def temp(self):
        def func(category, **kwargs):
            try:
                filename, content = handler.temp(category)
                print(f'Saved {filename}')
            except ValueError:
                return
            else:
                tags = input('Tags<space>: ').split()
                es_result = self.biotag.add_file_tags(filename, tags)
                print(es_result)
        return func

    @bioparser.register
    @bioparser.add_argument('content', nargs='?', type=str)
    @bioparser.add_argument('--resize', nargs=2, type=int)
    @bioparser.add_argument('--inline', type=int, default=1)
    def imgcat(self):
        def func(content, inline=1, resize=None, **kwargs):
            if content is None:
                content = img.get_clipboard_image()
            if resize is not None:
                content = img.buffer_resize(content, resize)
            print(img.iterm2_img_format(content, inline).decode())
        return func
