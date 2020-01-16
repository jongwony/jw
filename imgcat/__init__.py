import sys
from functools import partial
from argparse import ArgumentParser, FileType

from .img import get_clipboard_image, iterm2_img_format


def main(args=None):
    parser = ArgumentParser()
    parser.add_argument('--graphviz', action='store_true')
    parser.add_argument('--clipboard', action='store_true')
    parser.add_argument('--base64', action='store_true')
    parser.add_argument('--width', type=str)
    parser.add_argument('--height', type=str)
    parser.add_argument('--preserve', type=str)
    parser.add_argument('--binary', action='store_true')
    parser.add_argument('infile', nargs='?', type=FileType('rb'),
                        help='a graphviz file to be validated or pretty-printed',
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=FileType('w'),
                        help='write the output of infile to outfile',
                        default=sys.stdout)
    parsed_args = parser.parse_args(args)

    graphviz = parsed_args.graphviz
    clipboard = parsed_args.clipboard
    base64 = parsed_args.base64
    width = parsed_args.width
    height = parsed_args.height
    preserve = parsed_args.preserve

    # file-like object
    infile = parsed_args.infile
    outfile = parsed_args.outfile

    output = partial(iterm2_img_format, preserve=preserve, width=width, height=height)

    with infile, outfile:
        if graphviz:
            from graphviz import Source
            gv = Source(infile.read())
            outfile.write(output(gv.pipe('png')))
        elif clipboard:
            outfile.write(output(get_clipboard_image()))
        elif base64:
            outfile.write(output(infile.read()))
        else:
            outfile.write(output(infile))
