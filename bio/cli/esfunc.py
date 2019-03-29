import json

from bio import handler
from util import es_tag, es_query
from .gfunc import GFunc


class ESFunc(GFunc):
    bioparser = GFunc.bioparser
    biofile = GFunc.biofile
    biotag = es_tag.init()

    @bioparser.register
    @bioparser.add_argument('content', type=str)
    @bioparser.add_argument('-j', '--json', dest='custom', action='store_true',
                            help='custom json stdin')
    @bioparser.add_argument('-t', '--type', dest='dsl', type=str, default='term',
                            help='|'.join(
                                x for x in dir(es_query) if not x.startswith('_')))
    def search(self):
        def func(content: str, custom=False, dsl='term', **kwargs):
            if not custom:
                content = getattr(es_query, dsl)(content)
            else:
                content = json.loads(content)
            result = self.biotag.search(content)
            print(*es_tag.extract_search(result, 'tags'), sep='\n')

        return func

    @bioparser.register
    @bioparser.add_argument('_id', type=str)
    def edit(self):
        def func(_id, **kwargs):
            result = self.biofile.edit(_id)
            print(f'Changed {result.path}')
            print(f'Current tags: {es_tag.extract_doc(result.tags, "tags")}')
            tags = input('Tags<space>: ').split()
            update_tags = self.biotag.union_tags(_id, tags)
            print(f'Tag {es_tag.extract_doc(update_tags, data="result")}')

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

