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


def popup(msg : str, title : str) -> int:
    """abstracts popup
    
    A function to handle the pop-up status windows
    
    Args:
        msg (str): The main body of the message
        title (str): The text that appears at the top of the window
        
    Returns:
        int: Returns int code of which button was pressed
    """

    # the first zero specifies a pop-up window
    # the second zero styles the window based on a hex code
    # for more info:
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messagebox
    return ctypes.windll.user32.MessageBoxW(0, msg, title, 0x00000040)


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

    mymessage = 'A message'
    title = 'Popup window'
    print(popup(mymessage, title))