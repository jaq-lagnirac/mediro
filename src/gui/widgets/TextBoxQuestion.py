# Justin Caringal
# 
# A parent class framework for a textbox
# Entry question with associated label and
# status text

import tkinter as tk
from tkinter import ttk
from typing import Callable
from constants import *

class TextBoxQuestion(ttk.Frame):

    """
    A parent class that provides the basic label and textbox
    combination to take user input.
    """

    _DEFAULT_LABEL_WIDTH = 20
    _DEFAULT_TEXTBOX_WIDTH = 30
    _DEFAULT_COL_SPAN = 1
    _FRAME_PADX_LEFT = 10
    _FRAME_PADX_RIGHT = 10

    def __init__(self,
                 master : tk.Tk = None,
                 *, # requires keyword arguments
                 question : str = '',
                 status : str = '',
                 row : int = _ORIGIN_ROW,
                 column : int = (_ORIGIN_COL + 1),
                 label_width : int = _DEFAULT_LABEL_WIDTH,
                 textbox_width : int = _DEFAULT_TEXTBOX_WIDTH,
                 col_span : int = _DEFAULT_COL_SPAN) -> None:
        """Initializes the frame to take user input.
        
        A function which handles the labeling and creation
        of a user input textbox.

        Args:
            master (tk.Tk): The root object of the textbox.
            question (str): The question text to be added to the label.
            status (str): The default status message to the user.
            row (int): The placement row of the created object.
            column (int): The placement column of the created object.
            label_width (int): The width of the question Label object.
            textbox_width (int): The width of the Entry object.
            col_span (int): The number of columns that the object takes up.
            
        Returns:
            None
        """

        super().__init__(master)

        self.question = question
        self.status = status
        self.col = column
        self.row = row
        self.label_width = label_width
        self.textbox_width = textbox_width
        self.col_span = col_span

        # positions tk.Frame in window
        self.grid(row=self.row,
                  column=self.col,
                  columnspan=self.col_span,
                  padx=(self._FRAME_PADX_LEFT, self._FRAME_PADX_RIGHT),
                  sticky='NW')
        
        # label asking the user a question
        QUESTION_LABEL_ROW = _ORIGIN_ROW
        QUESTION_LABEL_COL = _ORIGIN_COL
        self.question_label = ttk.Label(self,
                                        width=self.label_width,
                                        text=self.question,
                                        anchor='w',
                                        justify='left',
                                        font=_FONT_INFO)
        self.question_label.grid(row=QUESTION_LABEL_ROW,
                                 column=QUESTION_LABEL_COL,
                                 sticky='W')
        
        # textbox collecting the user input
        TEXTBOX_ROW = _ORIGIN_ROW
        TEXTBOX_COL = _ORIGIN_COL + 1
        self.text_str = tk.StringVar()
        self.textbox = ttk.Entry(self,
                                 width=self.textbox_width,
                                 textvariable=self.text_str,
                                 font=_FONT_INFO)
        self.textbox.grid(row=TEXTBOX_ROW,
                          column=TEXTBOX_COL,
                          sticky='NESW')

        # added input validation
        # https://stackoverflow.com/a/51421764
        self.text_str.trace_add('write', self.validate_input)

        # status message updating the user on the validity of input
        STATUS_LABEL_ROW = _ORIGIN_ROW + 1
        STATUS_LABEL_COL = TEXTBOX_COL
        self.status_label = ttk.Label(self,
                                      text=self.status,
                                      anchor='w',
                                      justify='left',
                                      font=_FONT_INFO)
        self.status_label.grid(row=STATUS_LABEL_ROW,
                               column=STATUS_LABEL_COL,
                               sticky='NESW')
        
        return
        
    
    def set_textbox(self, text : str) -> None:
        """Changes text in user input textbox.
        
        A function which handles the clearing and insertion
        of text, often used to initialize defaults or inputs
        from external sources (e.g. file dialogs).
        
        Args:
            text (str): The text string to be inserted.
        
        Returns:
            None
        """
        self.textbox.delete(0, 'end')
        self.textbox.insert(0, text)
        return
    

    def get_textbox(self) -> str:
        """Retrieves text in user input textbox.
        
        A function which handles the retrieval
        of text, used for processing further down
        the program execution.
        
        Args:
            None
        
        Returns:
            str: Returns string inputted by a user.
        """
        return self.textbox.get()


    def validate_input(self,
                       *entry : tk.Event) -> bool:
        """Validates user input before main program run.
        
        A placeholder input validation function that returns
        True no matter the input; meant to be overwritten by
        children classes if more complex input validation
        is required.

        Args:
            entry (tk.Event): The user-inputted entry, not interacted with.

        Returns:
            bool: Returns True no matter the input.
        """
        self.status_label.config(text='Valid input.',
                                 foreground=_SUCCESS_COL)
        return True
    
    def add_trace_funct(self,
                        funct : Callable[[], None],
                        mode : str = 'write') -> None:
        """Links a function to track textbox updates with trace_add.
        Args:
            funct (Callable[[], None]): The function to be added.
        """
        self.text_str.trace_add(mode, funct)
        return

__all__ = ['TextBoxQuestion']