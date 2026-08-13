import os

def get_root_folder() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')

def get_font_path(font_name: str = "0xProtoNerdFontMono-Regular.ttf") -> str:
    return os.path.join(get_root_folder(), font_name)