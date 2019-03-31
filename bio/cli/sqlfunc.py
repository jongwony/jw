from bio import handler
from util import sql_tag
from .gfunc import GFunc


class SQLiteFunc(GFunc):
    bioparser = GFunc.bioparser
    biofile = GFunc.biofile
    biotag = sql_tag

    @bioparser.register
    @bioparser.add_argument('content', type=str)
    @bioparser.add_argument('-q', '--sql', dest='custom', action='store_true',
                            help='custom sql stdin')
    def search(self):
        def func(content: str, custom=False, **kwargs):
            if not custom:
                pass
                # s = select([fs]).where(fs.c)
                # content = getattr(query, dsl)(content)
            else:
                pass
                # content = json.loads(content)
            result = self.biotag.search(content)
            print(result)

        return func

    # TODO: EDIT, DEL
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
                es_result = self.biotag.add_file_tags(filename, tags)
                print(es_result)

        return func
