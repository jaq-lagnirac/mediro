# Justin Caringal
# 
# Handles the logging functionalities of the application,
# Sets up and facilitates output to the user.

import os
import sys
import logging
import tkinter as tk
from tkinter import ttk
from constants import *

class LoggingBox(ttk.Frame):

    """
    Handles the logging functionalities of the application,
    Sets up and facilitates output to the user.
    """

    _DEFAULT_OUTPUT_HEIGHT = 10
    _DEFAULT_OUTPUT_WIDTH = 50
    _DEFAULT_COL_SPAN = 1
    _FRAME_PADX_BASE = 0
    _FRAME_PADX_LEFT = _FRAME_PADX_BASE + 8
    _FRAME_PADX_RIGHT = _FRAME_PADX_BASE + 2
    _OUTPUT_FONT_INFO = ('Courier New', 12)

    def __init__(self,
                 master : tk.Tk = None,
                 *, # requires keyword arguments
                 row : int = _ORIGIN_ROW,
                 column : int = (_ORIGIN_COL + 1),
                 output_height : int = _DEFAULT_OUTPUT_HEIGHT,
                 output_width : int = _DEFAULT_OUTPUT_WIDTH,
                 col_span : int = _DEFAULT_COL_SPAN) -> None:
        """Initializes the frame to start monitoring a target directory.

        Args:
            master (tk.Tk): The root object of the textbox.
            row (int): The placement row of the created object.
            column (int): The placement column of the created object.
            output_height (int): The width of the Text object.
            output_width (int): The width of the Text object.
            col_span (int): The number of columns that the object takes up.
            
        Returns:
            None
        """

        super().__init__(master)
        self.col = column
        self.row = row
        self.output_height = output_height
        self.output_width = output_width
        self.col_span = col_span

        # positions tk.Frame in window
        self.grid(row=self.row,
                  column=self.col,
                  columnspan=self.col_span,
                  padx=(self._FRAME_PADX_LEFT, self._FRAME_PADX_RIGHT),
                  sticky='NW')
        
        # creates text widget
        self.output_text = tk.Text(self,
                                   wrap='word',
                                   font=self._OUTPUT_FONT_INFO,
                                   height=self.output_height,
                                   width=self.output_width)
        self.output_text.grid(row=_ORIGIN_ROW,
                              column=_ORIGIN_COL,
                              columnspan=3)
        self.output_text.config(state='disabled')
        self.output_text.tag_config('hanging_indent',
                                    lmargin1=0,
                                    lmargin2=20) # 10 pixels = 1 char

        # creates scrollbar
        self.output_scrollbar = tk.Scrollbar(self)
        self.output_scrollbar.grid(row=0,
                                   column=100,
                                   rowspan=100,
                                   sticky='NS')

        # configures text widget to use scrollbar
        self.output_text.config(yscrollcommand=self.output_scrollbar.set)
        self.output_scrollbar.config(command=self.output_text.yview)

    def update_output(self,
                      msg : str = '') -> None:
        """Updates the window with the latest log file.
        
        Args:
            msg (str): Optional message to add to the log.
        
        Returns:
            None
        """

        if msg:
            logging.info(msg)

        log_text = None # scope resolution
        with open(_LOG_FILE, 'r') as file:
            log_text = file.read()
        self.output_text.config(state='normal')
        self.output_text.delete(1.0,
                                tk.END)
        self.output_text.insert('end',
                                log_text,
                                'hanging_indent')
        self.output_text.config(state='disabled')
        self.output_text.yview(tk.END)
        self.update()
        
        return
    
__all__ = ['LoggingBox']