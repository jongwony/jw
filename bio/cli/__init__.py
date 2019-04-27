from .sqlfunc import SQLiteFunc


class CLIInit(SQLiteFunc):
    @classmethod
    def main(cls):
        for c in SQLiteFunc.__mro__:
            for k in set(vars(c)):
                f = getattr(c, k)
                if not k.startswith('__') and callable(f):
                    f(c)

        namespace = cls.bioparser.parse_args()
        if hasattr(namespace, 'func'):
            namespace.func(**vars(namespace))
        else:
            cls.bioparser.print_help()
