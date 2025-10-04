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
from constants import *
from mediro_engine import mediro_sort


class MainWindow(tk.Tk):

    """
    Generates the main window which the user will interact with.
    """

    # MainLogo at (0, 0), shift subsequent objects to column 1
    _ORIGIN_ROW = _ORIGIN_ROW
    _ORIGIN_COL = _ORIGIN_COL + 1
    # _FONT_NAME = 'Verdana'
    # _FONT_SIZE = 10
    # _FONT_INFO = (_FONT_NAME, _FONT_SIZE)

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
        self._populate_window()
        self._populate_config_values()

    def _populate_window(self) -> None:
        """Creates objects in main window.
        
        A function which organizes the creation of objects
        after the main Tkinter window is created.
        
        Args:
            None
            
        Returns:
            None
        """

        MainLogo(self) # at origin (0, 0)

        self.spacer = ttk.Label(self,
                                text='')
        self.spacer.grid(row=self._ORIGIN_ROW,
                         column=self._ORIGIN_COL,
                         columnspan=100,
                         pady=50)
        
        DIR_Q_WIDTH = 50
        DIR_Q_COL_SPAN = 2
        self.input_dir_qn = FileQuestion(self,
                                         question='Input Directory:',
                                         row=(self._ORIGIN_ROW + 1),
                                         column=self._ORIGIN_COL,
                                         textbox_width=DIR_Q_WIDTH,
                                         col_span=DIR_Q_COL_SPAN,
                                         is_dir_search=True)
        self.output_dir_qn = FileQuestion(self,
                                          question='Output Directory:',
                                          row=(self._ORIGIN_ROW + 2),
                                          column=self._ORIGIN_COL,
                                          textbox_width=DIR_Q_WIDTH,
                                          col_span=DIR_Q_COL_SPAN,
                                          is_dir_search=True,
                                          require_existence=False)
        self.unsorted_dir_qn = FileQuestion(self,
                                            question='Unsorted Directory:',
                                            row=(self._ORIGIN_ROW + 3),
                                            column=self._ORIGIN_COL,
                                            textbox_width=DIR_Q_WIDTH,
                                            col_span=DIR_Q_COL_SPAN,
                                            is_dir_search=True,
                                            require_existence=False)
        
        # self.event_handler = DirEventHandler(self)
        self.monitor = DirectoryMonitor(self,
                                        # event_handler=self.event_handler,
                                        row=(self._ORIGIN_ROW + 4),
                                        column=self._ORIGIN_COL,
                                        output_width=DIR_Q_WIDTH,
                                        col_span=DIR_Q_COL_SPAN)
        
        stylesheet = ttk.Style()
        stylesheet.configure('Main.TButton', font=_FONT_INFO)
        BOT_ORIGIN_ROW = self._ORIGIN_ROW + 10
        BOT_BUTTON_COL = self._ORIGIN_COL + DIR_Q_COL_SPAN - 1
        
        self.start_button = ttk.Button(self,
                                       text='Start',
                                       command=self.start_mediro_sort,
                                       width=10,
                                       style='Main.TButton')
        self.start_button.grid(sticky='NES',
                               row=BOT_ORIGIN_ROW,
                               column=BOT_BUTTON_COL,
                               padx=(0, 10))
        
        return
        
    def _populate_config_values(self) -> None:
        """Extracts config values and fills values.
        
        A function which extracts the values from the local
        configuration file and populates the relevant window
        objects with the values.

        Args:
            None

        Returns:
            None
        """

        # creates local config file if none present
        # and reads in config values to use locally
        self.config = read_config()

        # creates dirs if they do not exist
        create_path(self.config['input_dir'])
        # create_path(self.config['unsorted_dir'])
        
        # populates defaults from config values
        self.input_dir_qn.set_textbox(self.config['input_dir'])
        self.output_dir_qn.set_textbox(self.config['output_dir'])
        self.unsorted_dir_qn.set_textbox(self.config['unsorted_dir'])
        
        # self.monitor.update_target_dir(self.config['input_dir'])
        return

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

        self.config['input_dir'] = \
            self.input_dir_qn.get_textbox()
        self.config['output_dir'] = \
            self.output_dir_qn.get_textbox()
        self.config['unsorted_dir'] = \
            self.input_dir_qn.get_textbox()
        save_config(self.config)

        return
    
    def start_mediro_sort(self) -> None:
        """Streamlines the mediro_sort call.
        
        Args:
            None
        
        Returns:
            None
        """

        input_dir = self.input_dir_qn.get_textbox()
        output_dir = self.output_dir_qn.get_textbox()
        unsorted_dir = self.unsorted_dir_qn.get_textbox()
        mediro_sort(input_dir, output_dir, unsorted_dir)
        return
    
__all__ = ['MainWindow']