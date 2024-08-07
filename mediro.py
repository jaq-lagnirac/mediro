# Justin Caringal
# A tool to partition a directory into subdirectories and
# sort files (originally for visual multimedia) based on
# time-of-creation
# 
# Developed for Windows


### LIBRARIES

import os # used to get ctime
import sys # handles early exits
import re # regex used to parse date-time info from name
import time # used for date/time functions
import ctypes # operates popup windows
import platform # used to prevent OSError with MessageBox

# NOTE: os.path.getctime(path) gets creation time on Windows
# machines but gets last modification time on Linux machines.
# At least that's what it said.


### CONSTANTS

INPUT_DIR = os.path.join('.', 'MEDIRO_requires_sorting')
UNSORTED_DIR = os.path.join('.', 'MEDIRO_unsorted')
IDYES = 6
MB_ICONASTERISK = 0x00000040
MB_ICONWARNING = 0x00000030
MB_YESNO = 0x00000004


### FUNCTIONS

def add_plural_s(count : int) -> str:
    """determines if an extra S should be added
    
    Args:
        count (int): the number to be pluraled
    Return:
        str: Returns an empty string if 1, s otherwise
    """

    if count == 1:
        return ''
    return 's'

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


def detect_input_dir(input_dir : str) -> None:
    """handles input directory detection
    
    A function which groups together input directory actions
    
    Args:
        input_dir (str): the relative path of the input directory
    
    Returns:
        None
    """

    if not os.path.isdir(input_dir):
        result = popup('Error',
                       f'Input subdirectory \"{input_dir}\" not found.\n' \
                       'Create subdirectory?',
                       MB_ICONWARNING | MB_YESNO)
        if result == IDYES:
            create_path(input_dir)
            popup('Update', f'Created \"{input_dir}\".\nExiting program.')
        else:
            popup('Exit', 'Exiting program.')
        sys.exit()

    return None


def confirm_program_start(input_dir : str) -> None:
    """handles popup confirmation
    
    A function which acts as a floodgate to the program,
    asking the user for consent in order to minimize the
    effects of a program misclick
    
    Args:
        input_dir (str): the relative path of the input directory
        
    Return:
        None
    """

    files_to_sort = len(os.listdir(input_dir))
    result = popup('Start-Up',
                   f'{files_to_sort} file{add_plural_s(files_to_sort)} detected.\nBegin sort?',
                   MB_YESNO)
    if result != IDYES: # should catch exiting out of prompt using the X as well
        popup('Exit', 'Exiting program.')
        sys.exit()

    return None


def main() -> None:
    """THE MAIN FUNCTION"""

    # self-contained functions, early exits located here
    detect_input_dir(INPUT_DIR)
    confirm_program_start(INPUT_DIR)
    
    create_path(UNSORTED_DIR)

    successfully_sorted = 0
    unsorted = 0
    # moves files from INPUT_DIR to new location
    for file_basename in os.listdir(INPUT_DIR):

        # generates relpath to be used during rest of loop
        file_relpath = os.path.join(INPUT_DIR, file_basename)

        # checks if file is dir, skips is True
        if os.path.isdir(file_relpath):
            unsorted += 1
            unsorted_relpath = os.path.join(UNSORTED_DIR, file_basename)
            os.replace(file_relpath, unsorted_relpath)
            continue

        # extracts time information from file based on ISO 8601
        iso8601_extended = re.findall('[12]\d{3}-[0-2]\d-[0-3]\d', file_basename)
        iso8601_basic = re.findall('[12]\d{3}[0-2]\d[0-3]\d', file_basename)
        
        # logic for extracting dir names, gives preference to ISO 8601 Extended
        year_dir = month_dir = day_dir = None # scope resolution
        if iso8601_extended:
            iso8601 = iso8601_extended[0] # YYYY-MM-DD
            # formats directory names
            year_dir = iso8601[:4]
            month_dir = f'{year_dir}_{iso8601[5:7]}'
            day_dir = f'{month_dir}_{iso8601[8:]}'
        elif iso8601_basic:
            iso8601 = iso8601_basic[0] # YYYYMMDD
            # formats directory names
            year_dir = iso8601[:4]
            month_dir = f'{year_dir}_{iso8601[4:6]}'
            day_dir = f'{month_dir}_{iso8601[6:]}'
        else:
            unsorted += 1
            unsorted_relpath = os.path.join(UNSORTED_DIR, file_basename)
            os.replace(file_relpath, unsorted_relpath)
            continue

        # checks to ensure date is not in the future,
        # moves to unsorted directory if True
        today = time.strftime('%Y_%m_%d')
        if day_dir > today:
            unsorted += 1
            unsorted_relpath = os.path.join(UNSORTED_DIR, file_basename)
            os.replace(file_relpath, unsorted_relpath)
            continue

        # creates new directory path
        new_dir_path = os.path.join('.', year_dir, month_dir, day_dir)
        create_path(new_dir_path)

        # checks if file already exists, renames to prevent overwriting file
        new_file_relpath = os.path.join(new_dir_path, file_basename)
        root, ext = os.path.splitext(new_file_relpath)
        duplicate_counter = 0
        while os.path.exists(new_file_relpath):
            original_relpath = new_file_relpath
            original_basename = os.path.basename(new_file_relpath)
            duplicate_counter += 1
            new_file_relpath = f'{root}_({duplicate_counter}){ext}'

            # asks consent of user to rename file
            result = popup(f'Warning: {original_relpath}',
                           f'\"{original_basename}\" already exists in {new_dir_path}.\n\n' \
                           f'Click YES to rename file to \"{new_file_relpath}\".\n\n' \
                           f'Click NO to move to {UNSORTED_DIR}.\n' \
                           'This action DOES NOT check the target directory for duplicate files. ' \
                           'There is NO overwrite protection for this directory.',
                           MB_ICONWARNING | MB_YESNO)
            if result != IDYES: # should catch exiting out of prompt using the X as well
                new_file_relpath = os.path.join(UNSORTED_DIR, original_basename)
                unsorted += 1
                break

        # moves file to new directory
        os.replace(file_relpath, new_file_relpath)

        successfully_sorted += 1
    
    popup('Complete',
          'Program finished executing.\n\n' \
          f'{successfully_sorted} file{add_plural_s(successfully_sorted)} sorted.\n' \
          f'{unsorted} file{add_plural_s(unsorted)} unsuccessfully sorted.\n\n' \
          'Thank you for using Mediro!\n' \
          'For more, check out github@jaq-lagnirac.')
    
    return


if __name__ == '__main__':
    main()
