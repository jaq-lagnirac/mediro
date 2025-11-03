# Justin Caringal
#
# The main driver program for the Mediro application

import os
import sys
import logging
from gui import MainWindow
from helpers.constants import *

def main() -> None:
    """The main function of the entire application."""

    # configures and starts up logging function
    WELCOME_TEXT = 'Welcome to Mediro!'
    WELCOME_TEXT += '\n' + ('-' * len(WELCOME_TEXT) * 2) + '\n'
    with open(_LOG_FILE, 'w') as file:
        file.write(WELCOME_TEXT)
    # hides file if on Windows
    # not needed for Linux/Mac due to dotfiles
    if sys.platform == 'win32':
        os.system(f'attrib +h "{_LOG_FILE}"')
    LOGGING_FORMAT = '[%(asctime)s] %(message)s'
    logging.basicConfig(filename=_LOG_FILE,
                        filemode='a',
                        format=LOGGING_FORMAT,
                        level=logging.INFO)
    try:
        # boots up main window to user
        window = MainWindow()
        window.mainloop()
    finally:
        with open(_LOG_FILE, 'r') as file:
            print(file.read()) # possibly remove before prod
        os.remove(_LOG_FILE)

if __name__ == "__main__":
    main()