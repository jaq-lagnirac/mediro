# Justin Caringal
# 
# A parent class framework for a textbox
# Entry question with associated label and
# status text

import tkinter as tk
from tkinter import ttk

class TextBoxQuestion(ttk.Frame):

    """
    A parent class that provides the basic label and textbox
    combination to take user input.
    """

    _ORIGIN_ROW = 0
    _ORIGIN_COL = 0
    _LABEL_WIDTH = 20
    _TEXTBOX_WIDTH = 30
    _FRAME_PADX_LEFT = 0
    _FRAME_PADX_RIGHT = 10

    def __init__(self,
                 master : tk.Tk = None,
                 text : str = '',
                 row : int = _ORIGIN_ROW,
                 column : int = (_ORIGIN_COL + 1)) -> None:
        """Initializes the frame to take user input.
        
        A function which handles the labeling and creation
        of a user input textbox.

        Args:
            master (tk.Tk): The root object of the textbox.
            text (str): The text to be added to the label.
            row (int): The placement row of the created object.
            column (int): The placement column of the created object.
        """

        self.row = row
        self.col = column
        self.text = text

        super().__init__(master)
        # positions tk.Frame in window
        self.grid(row=self.row,
                  column=self.col,
                  padx=(self._FRAME_PADX_LEFT, self._FRAME_PADX_RIGHT))
        
        # label asking the user a question
        LABEL_ROW = self._ORIGIN_ROW
        LABEL_COL = self._ORIGIN_COL
        self.label = ttk.Label(self,
                               width=self._LABEL_WIDTH,
                               text=self.text,
                               anchor='w',
                               justify='left')
        self.label.grid(row=LABEL_ROW,
                        column=LABEL_COL,
                        sticky='W')
        
        # textbox collecting the user input
        TEXTBOX_ROW = self._ORIGIN_ROW
        TEXTBOX_COL = self._ORIGIN_COL + 1
        self.text_str = tk.StringVar()
        self.textbox = ttk.Entry(self,
                                 width=self._TEXTBOX_WIDTH,
                                 textvariable=self.text_str)
        self.textbox.grid(row=TEXTBOX_ROW,
                          column=TEXTBOX_COL,
                          sticky='NESW')

        # added input validation
        # https://stackoverflow.com/a/51421764
        self.text_str.trace_add('write', self.validate_input)

    def validate_input(self,
                       *entry : tk.Event) -> bool:
        """Validates user input before main program run.
        
        A placeholder input validation function that returns
        True no matter the input; meant to be overwritten by
        children classes if more complex input validation
        is required.

        Args:
            entry (tk.Event): The user-inputted entry, not interacted with

        Returns:
            bool: Returns True no matter the input.
        """
        return True
    