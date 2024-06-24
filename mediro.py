# Justin Caringal
# A tool to partition a directory into subdirectories and
# sort files (originally for visual multimedia) based on
# time-of-creation
# 
# Developed for Windows

import os # used to get ctime
import time # used to convert ctime to human-readable info
import ctypes # operates popup windows

# NOTE: os.path.getctime(path) gets creation time on Windows
# machines but gets last modification time on Linux machines

def check_path(path : str) -> bool:
    """checks the existence of a file
    
    A function to handle checking the existence of the argument
    
    Args:
        path (str): A relative path to be checked
    
    Returns:
        bool: True if file exists, False otherwise
    """

def main():
    """THE MAIN FUNCTION"""

    check_path('placeholder')

if __name__ == '__main__':
    main()

    # mymessage = 'A message'
    # title = 'Popup window'
    # popup = ctypes.windll.user32.MessageBoxW
    # popup(0, mymessage, title, 0)