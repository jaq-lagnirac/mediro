# Justin Caringal
#
# A file to hold all of the global constants
# from this project and allow them to be
# shared across all Python files

import os
from .paths import resource_path

_ARBITRARILY_LARGE_NUM = 100 # to take up entire left side
_ORIGIN_ROW = 0
_ORIGIN_COL = 0
_SUCCESS_COL = '#00dd00'
_FAIL_COL = '#ff0000'
_FONT_NAME = 'Verdana'
_FONT_SIZE = 14
_FONT_INFO = (_FONT_NAME, _FONT_SIZE)
_LOGO_COLOR = '#fee869'
_LOG_FILE = '.mediro.log'
_NO_FILES_FOUND = {'[NO FILES FOUND]' : ''}
_NOT_DIR = {'[NOT A VALID DIRECTORY]' : ''}
_LOGO_PATH = resource_path(os.path.join('.', 'images', 'logo-color.png'))
_SUPPORTED_PHOTO_EXTS = [
    '.jpg',
    '.jpeg',
    '.png',
    '.jxl',
    '.webp',
    '.heic',
    '.raw',
    ]

__all__ = [
    '_ARBITRARILY_LARGE_NUM',
    '_ORIGIN_ROW',
    '_ORIGIN_COL',
    '_SUCCESS_COL',
    '_FAIL_COL',
    '_FONT_NAME',
    '_FONT_SIZE',
    '_FONT_INFO',
    '_LOGO_COLOR',
    '_LOG_FILE',
    '_NO_FILES_FOUND',
    '_NOT_DIR',
    '_LOGO_PATH',
    '_SUPPORTED_PHOTO_EXTS',
    ]