from bio import config
from .esfunc import ESFunc
from .sqlfunc import SQLiteFunc


storage_class = {
    'elasticsearch': ESFunc,
    'sqlite3': SQLiteFunc,
}
StorageFunc = storage_class[config.get('storage')]


class CLIInit(StorageFunc):
    @classmethod
    def main(cls):
        for c in StorageFunc.__mro__:
            for k in set(vars(c)):
                f = getattr(c, k)
                if not k.startswith('__') and callable(f):
                    f(c)

        namespace = cls.bioparser.parse_args()
        if hasattr(namespace, 'func'):
            namespace.func(**vars(namespace))
        else:
            cls.bioparser.print_help()
