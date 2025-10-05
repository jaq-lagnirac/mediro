# Justin Caringal
# 
# Tools to analyze a given directory and facilitate the output to a user.

import os
from constants import *

def analyze_filetypes(dir : str) -> dict:
    """Gathers and formats the file makeup of the target directory.
    
    Args:
        dir (str): Directory to be analyzed.
    
    Returns:
        dict: Returns a hash table of filetypes and counts
    """

    # counts file types in target directory
    extension_hash = {}
    for file in os.listdir(dir):
        _, ext = os.path.splitext(file)
        if not ext:
            ext = 'Directory'
        if ext not in extension_hash:
            extension_hash[ext] = 0
        extension_hash[ext] += 1

    # if extension_hash is empty, notify user
    if not extension_hash:
        return _NO_FILES_FOUND

    return extension_hash

__all__ = ['analyze_filetypes']
