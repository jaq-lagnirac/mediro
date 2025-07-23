# Justin Caringal
#
# Functions for use with Mediro that
# handle the reading and writing of the
# configuration JSON file for the program

import os
import sys
import json
from paths import resource_path

_CONFIG_NAME = '.MEDIRO.config.json'
_DEFAULT_CONFIG_NAME = resource_path('default.config.json')

def check_create_config() -> None:
    """Creates new config.json if none are detected.
    
    A function which looks for a configuration JSON file
    tied to Mediro and, if none are detected, generates
    one in the same directory as the application.
    
    Args:
        None
    
    Returns:
        None
    """
    
    if os.path.exists(_CONFIG_NAME):
        return
    
    default_values = None # scope resolution
    with open(_DEFAULT_CONFIG_NAME, 'r') as default_file:
        default_values = json.load(default_file)

    with open(_CONFIG_NAME, 'w') as output_file:
        json.dump(default_values, output_file, indent=2)

    # hides file if on Windows
    # not needed for Linux/Mac due to dotfiles
    if sys.platform == 'win32':
        os.system(f'attrib +h "{_CONFIG_NAME}"')
    
    return

__all__ = ['check_create_config']