import os
import base64


is_screen = os.environ.get('TERM').startswith('screen')
osc = b'\033Ptmux;\033\033]' if is_screen else b'\033]'
st = b'\a\033\\' if is_screen else b'\a'


def iterm2_img_format(filename=None, inline=1, content=None):
    if content:
        b64content = content.encode()
        size = len(base64.b64decode(b64content))
    elif filename:
        size = os.stat(filename).st_size
        with open(filename, 'rb') as f:
            b64content = base64.b64encode(f.read())
    else:
        raise IOError

    result = osc
    result += b'1337;File='

    if filename:
        result += b'name=%s;' % base64.b64encode(filename.encode())

    result += b'size=%s;' % bytes(str(size).encode())
    result += b'inline=%s' % bytes(str(inline).encode())
    result += b':'
    result += b'%s' % b64content
    result += st
    result += b'\n'

    return result


def print_image(filename=None, inline=1, content=None):
    print(iterm2_img_format(filename, inline, content).decode())

