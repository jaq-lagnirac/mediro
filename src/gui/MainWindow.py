# Justin Caringal
#
# Functions for use in the Mediro Media Directory
# Formats main window that is displayed to the user,
# handles GUI window functionalities

import tkinter as tk
from tkinter import ttk
from .widgets import *
from config_handling import read_config, save_config
from paths import create_path


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
        """Class constructor method.
        
        A function which generates a GUI window to display to
        the user and handles the formatting and generation for
        the main window. Does not run mainloop.
        
        Args:
            None
        
        Returns:
            None
        """

        # initializes main window object
        super().__init__()
        self.resizable(False, False)
        self.title('Mediro')

        MainLogo(self) # at origin (0, 0)

        self.spacer = ttk.Label(self,
                                text='')
        self.spacer.grid(row=self._ORIGIN_ROW,
                         column=self._ORIGIN_COL,
                         columnspan=100,
                         pady=50)
        
        self.input_dir_qn = FileQuestion(self,
                                         question='file',
                                         row=(self._ORIGIN_ROW + 1),
                                         column=self._ORIGIN_COL,
                                         textbox_width=50,
                                         col_span=2)
        self.unsorted_dir_qn = FileQuestion(self,
                                            question='dir',
                                            row=(self._ORIGIN_ROW + 2),
                                            column=self._ORIGIN_COL,
                                            textbox_width=50,
                                            col_span=2,
                                            is_dir_search=True)
        
        # creates local config file if none present
        # and reads in config values to use locally
        self.config = read_config()

        # creates dirs if they do not exist
        # create_path(config['input_dir'])
        # create_path(config['unsorted_dir'])
        
        # populates defaults from config values
        self.input_dir_qn.set_textbox(self.config['input_dir'])
        self.unsorted_dir_qn.set_textbox(self.config['unsorted_dir'])

    def save_input_to_config(self):
        """Updates config file with user input.
        
        A function which pulls the data from the relevant
        textboxes and saves the information to the requisite
        field in the configuration file.
        
        Args:
            None
        
        Returns:
            None
        """

        self.config = {
            'input_dir' : self.input_dir_qn.get_textbox(),
            'unsorted_dir' : self.input_dir_qn.get_textbox()
        }
        save_config(self.config)

        return