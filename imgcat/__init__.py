from .img import get_clipboard_image, iterm2_img_format


def main(args=None):
    content = get_clipboard_image()
    print(iterm2_img_format(content, 1))
