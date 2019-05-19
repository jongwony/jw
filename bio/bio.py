from _cli.util import register, add_argument
from . import handler
from .sql import core, tag


@register
@add_argument('content', type=str)
@add_argument('-q', '--sql', dest='custom', action='store_true',
              help='custom sql stdin')
def search():
    def func(content: str, custom=False):
        if not custom:
            result = tag.search(content)
        else:
            result = tag.custom_search(content)
        print(result)
    return func


@register
@add_argument('-t', '--tag', action='store_true',
              help='list all tag')
def ls():
    def func(**kwargs):
        if kwargs.get('tag'):
            print(tag.custom_search('tag'))
        else:
            print(tag.custom_search('files'))
    return func


# TODO: DEL
@register
@add_argument('_id', type=str)
def edit():
    def func(_id):
        try:
            meta, content = core.edit(int(_id))
            print(f'Saved {meta}')
        except ValueError:
            return
        else:
            tags = input('Tags<space>: ').split()
            tag.union_tags(_id, tags)
    return func


@register
@add_argument('category', nargs='?', default='md',
              help='file extension, load templates')
def temp():
    def func(category):
        try:
            filename, content = handler.temp(category)
            print(f'Saved {filename}')
        except ValueError:
            return
        else:
            tags = input('Tags<space>: ').split()
            tag.add_file_tags(filename, tags)
    return func
