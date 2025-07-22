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
    _DEFAULT_LABEL_WIDTH = 20
    _DEFAULT_TEXTBOX_WIDTH = 30
    _DEFAULT_COL_SPAN = 1
    _FRAME_PADX_LEFT = 10
    _FRAME_PADX_RIGHT = 10
    _SUCCESS_COL = '#00dd00'
    _FAIL_COL = '#ff0000'
    _FONT_NAME = 'Verdana'
    _FONT_SIZE = 14
    _FONT_INFO = (_FONT_NAME, _FONT_SIZE)

    def __init__(self,
                 master : tk.Tk = None,
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
                  sticky='W')
        
        # label asking the user a question
        QUESTION_LABEL_ROW = self._ORIGIN_ROW
        QUESTION_LABEL_COL = self._ORIGIN_COL
        self.question_label = ttk.Label(self,
                                        width=self.label_width,
                                        text=self.question,
                                        anchor='w',
                                        justify='left',
                                        font=self._FONT_INFO)
        self.question_label.grid(row=QUESTION_LABEL_ROW,
                                 column=QUESTION_LABEL_COL,
                                 sticky='W')
        
        # textbox collecting the user input
        TEXTBOX_ROW = self._ORIGIN_ROW
        TEXTBOX_COL = self._ORIGIN_COL + 1
        self.text_str = tk.StringVar()
        self.textbox = ttk.Entry(self,
                                 width=self.textbox_width,
                                 textvariable=self.text_str,
                                 font=self._FONT_INFO)
        self.textbox.grid(row=TEXTBOX_ROW,
                          column=TEXTBOX_COL,
                          sticky='NESW')

        # added input validation
        # https://stackoverflow.com/a/51421764
        self.text_str.trace_add('write', self.validate_input)

        # status message updating the user on the validity of input
        STATUS_LABEL_ROW = self._ORIGIN_ROW + 1
        STATUS_LABEL_COL = TEXTBOX_COL
        self.status_label = ttk.Label(self,
                                      text=self.status,
                                      anchor='w',
                                      justify='left',
                                      font=self._FONT_INFO)
        self.status_label.grid(row=STATUS_LABEL_ROW,
                               column=STATUS_LABEL_COL,
                               sticky='NESW')


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
                                 foreground=self._SUCCESS_COL)
        return True
    