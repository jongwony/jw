from bio import handler
from util import sql_tag, sql_core
from .gfunc import GFunc


class SQLiteFunc(GFunc):
    bioparser = GFunc.bioparser

    @bioparser.register
    @bioparser.add_argument('content', type=str)
    @bioparser.add_argument('-q', '--sql', dest='custom', action='store_true',
                            help='custom sql stdin')
    def search(self):
        def func(content: str, custom=False, **kwargs):
            if not custom:
                result = sql_tag.search(content)
            else:
                result = sql_tag.custom_search(content)
            print(result)

        return func

    @bioparser.register
    @bioparser.add_argument('-t', '--tag', action='store_true',
                            help='list all tag')
    def ls(self):
        def func(**kwargs):
            if kwargs.get('tag'):
                print(sql_tag.custom_search('tag'))
            else:
                print(sql_tag.custom_search('files'))

        return func

    # TODO: DEL
    @bioparser.register
    @bioparser.add_argument('_id', type=str)
    def edit(self):
        def func(_id, **kwargs):
            try:
                meta, content = sql_core.edit(int(_id))
                print(f'Saved {meta}')
            except ValueError:
                return
            else:
                tags = input('Tags<space>: ').split()
                sql_tag.union_tags(_id, tags)

        return func

    @bioparser.register
    @bioparser.add_argument('category', nargs='?', default='md',
                            help='file extension, load templates')
    def temp(self):
        def func(category, **kwargs):
            try:
                filename, content = handler.temp(category)
                print(f'Saved {filename}')
            except ValueError:
                return
            else:
                tags = input('Tags<space>: ').split()
                sql_tag.add_file_tags(filename, tags)

        return func
