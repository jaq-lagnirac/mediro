# Justin Caringal
# A tool to partition a directory into subdirectories and
# sort files (originally for visual multimedia) based on
# time-of-creation
# 
# Developed for Windows


### LIBRARIES

import os # used to get ctime
import sys # handles early exits
import time # used to convert ctime to human-readable info
import ctypes # operates popup windows
import platform # used to prevent OSError with MessageBox

# NOTE: os.path.getctime(path) gets creation time on Windows
# machines but gets last modification time on Linux machines


### CONSTANTS

INPUT_DIR = os.path.join('.', 'requires_sorting')
IDYES = 6
IDNO = 7
MB_ICONASTERISK = 0x00000040
MB_ICONWARNING = 0x00000030
MB_YESNO = 0x00000004


### FUNCTIONS

def popup(title : str, msg : str, modifier : int = MB_ICONASTERISK) -> int:
    """abstracts popup
    
    A function to handle the pop-up status
    windows and platform system detection
    
    Args:
        title (str): The text that appears at the top of the window
        msg (str): The main body of the message
        modifier (int): Hex code which modifies the popup's appearance
        
    Returns:
        int: Returns int code of which button was pressed,
        -1 if on a non-Windows machine
    """

    # the first zero specifies a pop-up window
    # the second zero styles the window based on a hex code
    # for more info:
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messagebox
    if platform.system() == 'Windows':
        return ctypes.windll.user32.MessageBoxW(0, msg, f'Mediro - {title}', modifier)
    return -1


def create_path(path : str) -> None:
    """handles directory management
    
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


def detect_input_dir() -> None:
    """handles input directory detection
    
    A function which groups together input directory actions
    
    Args:
        None
    
    Returns:
        None
    """

    if not os.path.isdir(INPUT_DIR):
        result = popup('Error',
                       f'Input subdirectory \"{INPUT_DIR}\" not found.\n' \
                       'Create subdirectory?',
                       MB_ICONWARNING | MB_YESNO)
        if result == IDYES:
            create_path(INPUT_DIR)
            popup('Update', f'Created \"{INPUT_DIR}\".\nExiting program.')
        else:
            popup('Exit', 'Exiting program.')
        sys.exit()

    return None


def main():
    """THE MAIN FUNCTION"""

    detect_input_dir() # self-contained function, early exit located here

    files_to_sort = len(os.listdir(INPUT_DIR))
    result = popup('Start-Up', f'{files_to_sort} files detected.\nBegin sort?', MB_YESNO)
    if result == IDNO:
        popup('Exit', 'Exiting program.')
        sys.exit()

    for file_basename in os.listdir(INPUT_DIR):

        # extracts time information from file
        file_relpath = os.path.join(INPUT_DIR, file_basename)
        creation_time = os.path.getctime(file_relpath)
        time_struct = time.localtime(creation_time)

        # formats directory names
        year_dir = time.strftime('%Y', time_struct)
        month_dir = time.strftime('%Y_%m', time_struct)
        day_dir = time.strftime('%Y_%m_%d', time_struct)

        # creates new directory path
        new_dir_path = os.path.join(year_dir, month_dir, day_dir)
        create_path(new_dir_path)

        # moves image to new directory
        new_file_relpath = os.path.join(new_dir_path, file_basename)
        os.replace(file_relpath, new_file_relpath)


if __name__ == '__main__':
    main()

    # print(os.path.getctime('mediro.py'))

    # os.makedirs('testdir/subdir')
    # os.replace('test.txt', 'testdir/test.txt')