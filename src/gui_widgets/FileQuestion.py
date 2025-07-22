# Justin Caringal
# 
# A child class that asks the user to choose
# a file or directory, either through the use of the
# textbox or a pop-up file explorer window

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
                         textbox_width)
        self.button_width = button_width + 1 # extra 1 centers a bit better
        self.is_dir_search = is_dir_search

        # toggles between file search and dir search

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
        

    def _get_path_from_dialog(self) -> None:
        """Updates the output string with filename dialog"""

        self.filepath = None # scope resolution
        if self.is_dir_search:
            self.filepath = filedialog.askdirectory(
            title=self.question,
        )
        else: # is a file search
            self.filepath = filedialog.askopenfilename(
                title=self.question,
                filetypes=[("All files", "*.*")]
            )

        if self.filepath: # file successfully chosen
            self.textbox.delete(0, 'end')
            self.textbox.insert(0, self.filepath)
        else: # most likely premature exit
            self.status_label.config(text='File not chosen.',
                                     foreground=TextBoxQuestion._FAIL_COL)