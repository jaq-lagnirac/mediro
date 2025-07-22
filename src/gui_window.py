# Justin Caringal
#
# Functions for use in the Mediro Media Directory
# Formats main window that is displayed to the user,
# handles GUI window functionalities


### LIBRARIES / PACKAGES ###

import tkinter as tk
from gui_widgets import *


### GLOBAL CONSTANTS / VARIABLES ###

FONT_NAME = 'Verdana'
FONT_SIZE = 10
FONT_INFO = (FONT_NAME, FONT_SIZE)


### FUNCTIONS ###


def generate_main_window() -> tk.Tk:
    """Generates GUI window to display to the user.
    
    A function which handles the formatting and generation for
    the main window. Does not run mainloop.
    
    Args:
        None
    
    Returns:
        tk.Tk: Returns a filled tkinter window.
    """

    # declares main window object
    root = tk.Tk()
    root.resizable(False, False)
    root.title('Mediro')

    MainLogo(root)

    TextBoxQuestion(root, question='test12345', row=0, column=1)
    TextBoxQuestion(root, question='test2', row=0, column=2)
    TextBoxQuestion(root, question='test3', row=1, column=1)
    TextBoxQuestion(root, question='test4', row=1, column=2)

    FileQuestion(root, question='file', row=2, column=1)    


    root.mainloop()


# code to test window generation
if __name__ == "__main__":
    generate_main_window()

__all__ = ['generate_main_window']