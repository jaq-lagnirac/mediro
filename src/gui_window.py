# Justin Caringal
#
# Functions for use in the Mediro Media Directory
# Formats main window that is displayed to the user,
# handles GUI window functionalities

import tkinter as tk
from tkinter import ttk
from gui_widgets import *

ORIGIN_ROW = 0
ORIGIN_COL = 1 # MainLogo at (0, 0), shifted to column 1
FONT_NAME = 'Verdana'
FONT_SIZE = 10
FONT_INFO = (FONT_NAME, FONT_SIZE)

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

    MainLogo(root) # at origin (0, 0)

    spacer = ttk.Label(root,
                       text='')
    spacer.grid(row=ORIGIN_ROW,
                column=ORIGIN_COL,
                columnspan=100,
                pady=(100,0))
    
    FileQuestion(root, question='file', row=(ORIGIN_ROW + 1), column=ORIGIN_COL, textbox_width=50, col_span=2)
    FileQuestion(root, question='dir', row=(ORIGIN_ROW + 2), column=ORIGIN_COL, textbox_width=50, col_span=2, is_dir_search=True)


    return root

# code to test window generation
if __name__ == "__main__":
    test = generate_main_window()
    test.mainloop()

__all__ = ['generate_main_window']