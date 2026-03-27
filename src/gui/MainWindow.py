# Justin Caringal
#
# Functions for use in the Mediro Media Directory
# Formats main window that is displayed to the user,
# handles GUI window functionalities

import os
import tkinter as tk
from tkinter import ttk
from time import perf_counter
from .widgets import *
from helpers.config_handling import read_config, save_config
from helpers.paths import create_path
from helpers.constants import *
from helpers.mediro_engine import mediro_sort
from helpers.directory_analysis import count_total_files

class MainWindow(tk.Tk):

    """
    Generates the main window which the user will interact with.
    """

    # MainLogo at (0, 0), shift subsequent objects to column 1
    _ORIGIN_ROW = _ORIGIN_ROW
    _ORIGIN_COL = _ORIGIN_COL + 1

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
        self.protocol('WM_DELETE_WINDOW', self.graceful_shutdown)
        self.logging_box.update_output('Application booted up, ready to run.')
        return

    def graceful_shutdown(self) -> None:
        """Class destructor method.

        Organizes saving procedures.

        Args:
            None
        
        Returns:
            None
        """

        self.save_on_close = self.options.get_check_value('save_on_close')
        if self.save_on_close:
            self.save_input_to_config()
        self.logging_box.update_output('Shutting down window.')
        self.destroy()
        return

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
                         pady=45)
        
        DIR_Q_WIDTH = 50
        DIR_Q_COL_SPAN = 3
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
        
        OUTPUT_BOXES_HEIGHT = 22
        OUTPUT_BOXES_WIDTH = 88
        LOGBOX_WIDTH = 62
        MONITOR_WIDTH = OUTPUT_BOXES_WIDTH - LOGBOX_WIDTH
        self.logging_box = LoggingBox(self,
                                      row=(self._ORIGIN_ROW + 4),
                                      column=self._ORIGIN_COL,
                                      output_height=OUTPUT_BOXES_HEIGHT,
                                      output_width=LOGBOX_WIDTH,
                                      col_span=2)

        self.monitor = DirectoryMonitor(self,
                                        row=(self._ORIGIN_ROW + 4),
                                        column=(self._ORIGIN_COL + 2),
                                        output_height=OUTPUT_BOXES_HEIGHT,
                                        output_width=MONITOR_WIDTH,
                                        col_span=1)

        self.input_dir_qn.add_trace_funct(self.update_monitor)
        
        stylesheet = ttk.Style()
        stylesheet.configure('Main.TButton', font=_FONT_INFO)
        BOT_ORIGIN_ROW = self._ORIGIN_ROW + 10
        BOT_BUTTON_COL = self._ORIGIN_COL + DIR_Q_COL_SPAN - 1
        BOTTOM_LEFT_WIDGET_COUNT = 2

        self.options = CheckBoxToggle(self,
                                      row=BOT_ORIGIN_ROW,
                                      column=self._ORIGIN_COL)
        
        self.reset_button = ttk.Button(self,
                                       text='Reset to default',
                                       command=self.reset_config_to_default,
                                       width=15,
                                       style='Main.TButton')
        self.reset_button.grid(sticky='W',
                               row=(BOT_ORIGIN_ROW + 1),
                               column=self._ORIGIN_COL,
                               padx=(20, 10),
                               pady=(10,0))

        self.start_button = ttk.Button(self,
                                       text='Start',
                                       command=self.start_mediro_sort,
                                       width=10,
                                       style='Main.TButton')
        self.start_button.grid(sticky='E',
                               row=BOT_ORIGIN_ROW,
                               column=BOT_BUTTON_COL,
                            #    rowspan=BOTTOM_LEFT_WIDGET_COUNT,
                               padx=(0, 10),
                               pady=(10,0))
        
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
        self.config = read_config(self.logging_box.update_output)

        # creates dirs if they do not exist
        create_path(self.config['input_dir'])
        # create_path(self.config['unsorted_dir'])
        
        # populates defaults from config values
        self.input_dir_qn.set_textbox(self.config['input_dir'])
        self.output_dir_qn.set_textbox(self.config['output_dir'])
        self.unsorted_dir_qn.set_textbox(self.config['unsorted_dir'])
        self.options.set_all_check_values(self.config)

        # connects file type monitor to input directory
        self.monitor.update_target_dir(self.config['input_dir'])
        return
    
    def reset_config_to_default(self) -> None:
        """Deletes existing config if it exists and
        resets all values back to the default values
        contained in the default JSON file.
        
        Args:
            None
        
        Return:
            None
        """
        stream = self.logging_box.update_output
        stream('Resetting values to default.')
        if os.path.exists(_CONFIG_NAME):
            stream('Deleting existing configuration file.')
            os.remove(_CONFIG_NAME)
        self._populate_config_values()
        return
    
    def update_monitor(self, *entry : tk.Event) -> None:
        """Updates the directory monitor with
        a new target directory.
        
        Args:
            entry (tk.Event): The user-inputted entry, not interacted with.
        
        Returns:
            None
        """

        new_dir = self.input_dir_qn.get_textbox()
        
        # checks to make sure input is existing directory,
        # exits early if input does not exist
        if not os.path.isdir(new_dir):
            not_a_directory = \
                self.monitor.format_file_info(_NOT_DIR)
            self.monitor.set_textbox(not_a_directory)
            return
        
        self.monitor.update_target_dir(new_dir)
        self.logging_box.update_output('Now targeting input ' \
                                       f'directory: {new_dir}')
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

        # gets textbox values and saves to config
        self.config['input_dir'] = \
            self.input_dir_qn.get_textbox()
        self.config['output_dir'] = \
            self.output_dir_qn.get_textbox()
        self.config['unsorted_dir'] = \
            self.unsorted_dir_qn.get_textbox()

        # gets checkbox values, converts to boolean, saves boolean to config
        check_dict = self.options.get_all_check_values()
        bool_dict = {}
        for key, value in check_dict.items():
            bool_dict[key] = value.get()
        self.config.update(bool_dict)
        
        save_config(self.config, self.logging_box.update_output)
        return
    
    def start_mediro_sort(self) -> None:
        """Streamlines the mediro_sort call,
        handles before and after stream updates.
        
        Args:
            None
        
        Returns:
            None
        """

        stream_alias = self.logging_box.update_output

        stream_alias('Beginning Mediro execution.')
        start_time = perf_counter()

        input_dir = self.input_dir_qn.get_textbox()
        output_dir = self.output_dir_qn.get_textbox()
        unsorted_dir = self.unsorted_dir_qn.get_textbox()

        self.save_on_execution = \
            self.options.get_check_value('save_on_execution')
        if self.save_on_execution:
            self.save_input_to_config()
        
        file_count = count_total_files(input_dir)
        plural_s = lambda : '' if file_count == 1 else 's'
        stream_alias(f'{file_count} file{plural_s()} found for sorting.')

        mediro_sort(input_dir,
                    output_dir,
                    unsorted_dir,
                    stream_alias)
        
        end_time = perf_counter()
        elapsed_time = end_time - start_time
        stream_alias('Finished Mediro execution. '
                     f'Elapsed time: {elapsed_time:.4f} secs.')
        return
    
__all__ = ['MainWindow']