# Justin Caringal
#
# Functions for use in the Mediro Media Directory
# Organizer which are used to help create and manage
# directory pathings both on compilation and during
# program execution


### LIBRARIES / PACKAGES ###

import os
import sys

def resource_path(relpath : str) -> str:
    """Finds external resource for onefile pyinstaller executable.
    
    A function which generates a new relative path for external data,
    (i.e. images) during execution, mainly for use when creating an
    executable with PyInstaller.

    Based off of the following StackOverflow forum post:
    https://stackoverflow.com/a/72060275

    Args:
        relpath (str): a relative path to the file in question
    
    Returns:
        str: Returns a new path to the file
    """

    # https://stackoverflow.com/a/72060275
    try:
        base_path = sys._MEIPASS # only found in PyInstaller
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relpath)

def create_path(path : str) -> None:
    """Handles directory management.
    
    A function to checks the existence of a path and handle
    creating a directory path if one does not exist
    
    Args:
        path (str): A relative path to be checked
    
    Returns:
        None
    """

    if not os.path.exists(path):
        os.makedirs(path)

    return None

__all__ = ['resource_path', 'create_path']