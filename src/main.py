# Justin Caringal
#
# The main driver program for the Mediro application

import os
import logging
from gui import MainWindow

def main() -> None:
    """The main function of the entire application."""

    # configures and starts up logging function
    LOG_FILE = '.mediro.log'
    WELCOME_TEXT = 'Welcome to Mediro!\n'
    WELCOME_TEXT += ('-' * (len(WELCOME_TEXT) - 1)) + '\n'
    with open(LOG_FILE, 'w') as file:
        file.write(WELCOME_TEXT)
    LOGGING_FORMAT = '[%(asctime)s] %(message)s'
    logging.basicConfig(filename=LOG_FILE,
                        filemode='a',
                        format=LOGGING_FORMAT,
                        level=logging.INFO)
    try:
        # boots up main window to user
        window = MainWindow()
        window.mainloop()
    finally:
        with open(LOG_FILE, 'r') as file:
            print(file.read())
        os.remove(LOG_FILE)

if __name__ == "__main__":
    main()