# Justin Caringal
#
# Functions for use with Mediro that
# handle the reading and writing of the
# configuration JSON file for the program

import os
import sys
import json
from typing import Callable
from paths import resource_path

_CONFIG_NAME = '.MEDIRO.config.json'
_DEFAULT_CONFIG_NAME = resource_path('default.config.json')
_JSON_INDENT = 2

def _create_default_config(stream : Callable[[str], None]) -> None:
    """Creates new config.json if none are detected.
    
    A function which looks for a configuration JSON file
    tied to Mediro and, if none is detected, generates
    one in the same directory as the application.

    Ran before most if not all functions to ensure there
    is a proper and valid target for config file handling.
    
    Args:
        stream (Callable[[str], None]): The output stream for the messages.

    Returns:
        None
    """
    
    if os.path.exists(_CONFIG_NAME):
        stream('Mediro configuration file found.')
        return
    
    default_values = None # scope resolution
    with open(_DEFAULT_CONFIG_NAME, 'r') as default_file:
        default_values = json.load(default_file)

    keys_to_add_cwd = default_values['keys_to_add_cwd']
    for key in keys_to_add_cwd:
        basename = default_values[key]
        default_values[key] = os.path.join(os.getcwd(), basename)

    with open(_CONFIG_NAME, 'w') as output_file:
        json.dump(default_values, output_file, indent=_JSON_INDENT)

    # hides file if on Windows
    # not needed for Linux/Mac due to dotfiles
    if sys.platform == 'win32':
        os.system(f'attrib +h "{_CONFIG_NAME}"')
    
    stream('No Mediro configuration file detected. ' \
           'Creating default configuration file.')
    return

def read_config(stream : Callable[[str], None] = print) -> dict:
    """Reads in values from JSON file.
    
    A function which reads in the configuration values from a
    config.json file in the working directory and reads them
    into a local dictionary.
    
    Args:
        stream (Callable[[str], None]): The output stream for the messages.
    
    Returns:
        dict: Returns a dictionary of configuration values.
    """

    _create_default_config(stream)

    config_values = None # scope resolution
    with open(_CONFIG_NAME, 'r') as input_file:
        config_values = json.load(input_file)
    return config_values

def save_config(input_values : dict,
                stream : Callable[[str], None] = print) -> None:
    """Takes new values and saves to configuration file.
    
    A function which takes user inputted values and
    saves them to the configuration file. This function
    WILL OVERWRITE any pre-existing configuration file.
    
    Args:
        input_values (dict): The values to be stored in the file.
    
    Returns:
        None
    """

    _create_default_config(stream)
    with open(_CONFIG_NAME, 'w') as output_file:
        json.dump(input_values, output_file, indent=_JSON_INDENT)
    return

__all__ = ['read_config', 'save_config']