# Justin Caringal
#
# Functions for use in the Mediro Media Directory
# Formats main window that is displayed to the user,
# handles GUI window functionalities

import tkinter as tk
from tkinter import ttk
from .widgets import *


class MainWindow(tk.Tk):

    """
    Generates the main window which the user will interact with.
    """

    _ORIGIN_ROW = 0
    _ORIGIN_COL = 1 # MainLogo at (0, 0), shift subsequent objects to column 1
    _FONT_NAME = 'Verdana'
    _FONT_SIZE = 10
    _FONT_INFO = (_FONT_NAME, _FONT_SIZE)

    def __init__(self) -> None:
        """Generates GUI window to display to the user.
        
        A function which handles the formatting and generation for
        the main window. Does not run mainloop.
        
        Args:
            None
        
        Returns:
            None
        """
        
        # declares main window object
        super().__init__()
        self.resizable(False, False)
        self.title('Mediro')

        MainLogo(self) # at origin (0, 0)

        spacer = ttk.Label(self,
                           text='')
        spacer.grid(row=self._ORIGIN_ROW,
                    column=self._ORIGIN_COL,
                    columnspan=100,
                    pady=50)
        
        FileQuestion(self, question='file', row=(self._ORIGIN_ROW + 1), column=self._ORIGIN_COL, textbox_width=50, col_span=2)
        FileQuestion(self, question='dir', row=(self._ORIGIN_ROW + 2), column=self._ORIGIN_COL, textbox_width=50, col_span=2, is_dir_search=True)

        return