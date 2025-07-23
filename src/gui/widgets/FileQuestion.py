# Justin Caringal
# 
# A child class that asks the user to choose
# a file or directory, either through the use of the
# textbox or a pop-up file explorer window

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from .TextBoxQuestion import TextBoxQuestion

class FileQuestion(TextBoxQuestion):

    """
    A child class that gathers a user-inputted directory.
    """

    _DEFAULT_BUTTON_WIDTH = 5
    _BUTTON_TEXT = '...'

    def __init__(self,
                 master : tk.Tk = None,
                 question : str = '',
                 status : str = '',
                 row : int = TextBoxQuestion._ORIGIN_ROW,
                 column : int = TextBoxQuestion._ORIGIN_COL,
                 label_width : int = TextBoxQuestion._DEFAULT_LABEL_WIDTH,
                 textbox_width : int = TextBoxQuestion._DEFAULT_TEXTBOX_WIDTH \
                    - _DEFAULT_BUTTON_WIDTH,
                 col_span : int = TextBoxQuestion._DEFAULT_COL_SPAN,
                 button_width : int = _DEFAULT_BUTTON_WIDTH,
                 is_dir_search : bool = False) -> None:
        """Initializes the frame to take user input for a directory.
        
        A function which handles the labeling and creation
        of a user input textbox and creates a button for
        additional dialog options.

        Args:
            master (tk.Tk): The root object of the textbox.
            question (str): The question text to be added to the label.
            status (str): The default status message to the user.
            row (int): The placement row of the created object.
            column (int): The placement column of the created object.
            label_width (int): The width of the question Label object.
            textbox_width (int): The width of the Entry object.
            col_span (int): The number of columns that the object takes up.
            button_width (int): The width of the Button object to bring up
                a file dialog.
            is_dir_search (bool): If True, will pull up dialog for directory
                search. Otherwise, will search for filename.

        Returns:
            None
        """

        super().__init__(master,
                         question,
                         status,
                         row,
                         column,
                         label_width,
                         textbox_width,
                         col_span)
        self.button_width = button_width + 1 # extra 1 centers a bit better
        self.is_dir_search = is_dir_search

        # positioning button to the right of the textbox
        FILE_DIALOG_ROW = TextBoxQuestion._ORIGIN_ROW
        FILE_DIALOG_COL = TextBoxQuestion._ORIGIN_COL + 2
        self.file_exp_button = ttk.Button(self,
                                          text=self._BUTTON_TEXT,
                                          width=self.button_width,
                                          command=self._get_path_from_dialog)
        self.file_exp_button.grid(row=FILE_DIALOG_ROW,
                                  column=FILE_DIALOG_COL,
                                  sticky='NESW')
        
        return
        

    def validate_input(self,
                       *entry : tk.Event) -> bool:
        """Validates existence of filepath before execution.
        
        A function which validates the filepath user input.
        
        Args:
            entry (tk.Event): The user-inputted entry, not interacted with.
        
        Returns:
            bool: Returns True if the filepath exists, False otherwise.
        """

        filepath_input = self.get_textbox()
        if os.path.exists(filepath_input):
            self.status_label.config(text='Valid filepath.',
                                     foreground=self._SUCCESS_COL)
            return True
        
        self.status_label.config(text='Filepath not found.',
                                 foreground=self._FAIL_COL)
        return False


    def _get_path_from_dialog(self) -> None:
        """Updates the output string with filename dialog.
        
        A function which handles filedialog and displays
        the chosen filepath to the user through the Entry
        object.

        Args:
            None
        
        Returns:
            None
        """

        self.filepath = None # scope resolution
        file_type = None # scope resolution
        if self.is_dir_search:
            self.filepath = filedialog.askdirectory(
            title=self.question,
            )
            file_type = 'Directory'
        else: # is a file search
            self.filepath = filedialog.askopenfilename(
                title=self.question,
                filetypes=[("All files", "*.*")]
            )
            file_type = 'File'

        if self.filepath: # file successfully chosen
            self.set_textbox(self.filepath)
            self.status_label.config(text=f'{file_type} successfully chosen.',
                                     foreground=TextBoxQuestion._SUCCESS_COL)
        else: # most likely premature exit
            self.status_label.config(text=f'{file_type} not chosen.',
                                     foreground=TextBoxQuestion._FAIL_COL)
            
        return