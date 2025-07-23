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
_INDENT = 2

def create_default_config() -> None:
    """Creates new config.json if none are detected.
    
    A function which looks for a configuration JSON file
    tied to Mediro and, if none is detected, generates
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
        json.dump(default_values, output_file, indent=_INDENT)

    # hides file if on Windows
    # not needed for Linux/Mac due to dotfiles
    if sys.platform == 'win32':
        os.system(f'attrib +h "{_CONFIG_NAME}"')
    
    return

def save_config(input_values : dict) -> None:
    """Takes new values and saves to configuration file.
    
    A function which takes user inputted values and
    saves them to the configuration file. This function
    WILL OVERWRITE any pre-existing configuration file.
    
    Args:
        input_values (dict): The values to be stored in the file.
    
    Returns:
        None
    """

    with open(_CONFIG_NAME, 'w') as output_file:
        json.dump(input_values, output_file, indent=_INDENT)
    return

__all__ = ['create_default_config', 'save_config']