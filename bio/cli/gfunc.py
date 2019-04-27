from imgcat import img
from bio import handler, snippet
from .parser import BioParser


class GFunc:
    bioparser = BioParser()
    biofile = handler.BioFile()

    @bioparser.register
    @bioparser.add_argument('command', type=str, nargs='*',
                            help='custom snippet scripts: bio/scripts')
    def snip(self):
        def func(command, **kwargs):
            op, *args = command
            getattr(snippet, op)(*args)

        return func

    @bioparser.register
    @bioparser.add_argument('content', nargs='?', type=str,
                            help='None(clipboard) or base64 string or filename')
    @bioparser.add_argument('--resize', nargs=2, type=int)
    @bioparser.add_argument('--inline', type=int, default=1,
                            help='1(default): inline, 0: download')
    def imgcat(self):
        def func(content, inline=1, resize=None, **kwargs):
            if content is None:
                content = img.get_clipboard_image()
            if resize is not None:
                content = img.buffer_resize(content, resize)
            print(img.iterm2_img_format(content, inline).decode())

        return func

