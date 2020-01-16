import sys
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
    parser.add_argument('infile', nargs='?', type=FileType(),
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

    infile = parsed_args.infile
    outfile = parsed_args.outfile

    with infile, outfile:
        if graphviz:
            from graphviz import Source
            gv = Source(infile.read())
            outfile.write(iterm2_img_format(gv.pipe('png'), preserve=preserve, width=width, height=height))
        elif clipboard:
            content = get_clipboard_image()
            outfile.write(iterm2_img_format(content), preserve=preserve, width=width, height=height)
        elif base64:
            outfile.write(iterm2_img_format(infile.read()), preserve=preserve, width=width, height=height)
        else:
            outfile.write(iterm2_img_format(infile), preserve=preserve, width=width, height=height)
