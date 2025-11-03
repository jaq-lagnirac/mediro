# Justin Caringal
# 
# A widget class to handle a boolean-like
# checkbox toggle object

import tkinter as tk
from tkinter import ttk
from helpers.constants import *

class CheckBoxToggle(ttk.Frame):

    """
    A class which handles user input for a
    boolean input checkbox toggle.
    """

    _DEFAULT_WIDTH = 30
    _DEFAULT_COL_SPAN = 1
    _FRAME_PADX_LEFT = 10
    _FRAME_PADX_RIGHT = 10

    def __init__(self,
                 master : tk.Tk = None,
                 *, # requires keyword arguments
                 row : int = _ORIGIN_ROW,
                 column : int = _ORIGIN_COL,
                 width : int = _DEFAULT_WIDTH,
                 col_span : int = _DEFAULT_COL_SPAN) -> None:
        """Class constructor method.

        Args:
            master (tk.Tk): The root object of the textbox.
            target_directory (str): The directory to watch.
            row (int): The placement row of the created object.
            column (int): The placement column of the created object.
            width (int): The width of the Frame.
            col_span (int): The number of columns that the object takes up.
        """

        super().__init__(master)
        
        self.row = row
        self.col = column
        self.width = width
        self.col_span = col_span

        self.grid(row=self.row,
                  column=self.col,
                  columnspan=self.col_span,
                  padx=(self._FRAME_PADX_LEFT, self._FRAME_PADX_RIGHT),
                  sticky='W')

        self.check_values = {
            'save_on_close' : tk.BooleanVar(),
            'save_on_execution' : tk.BooleanVar(),
        }


        self.save_on_close = \
            tk.Checkbutton(self,
                           text='Save settings on close.',
                           font=_FONT_INFO,
                           variable=self.check_values['save_on_close'])
        self.save_on_close.grid(row=_ORIGIN_ROW,
                                column=_ORIGIN_COL,
                                sticky='W')
        
        self.save_on_execution = \
            tk.Checkbutton(self,
                           text='Save settings on program execution.',
                           font=_FONT_INFO,
                           variable=self.check_values['save_on_execution'])
        self.save_on_execution.grid(row=(_ORIGIN_ROW + 1),
                                    column=_ORIGIN_COL,
                                    sticky='W')
    
    def get_all_check_values(self) -> dict:
        """Returns all boolean check values in the form
        of a dictionary.
        
        Args:
            None
        
        Returns:
            dict: Returns a dictionary of the check values
        """
        return self.check_values
    
    def set_all_check_values(self, update_dict : dict) -> None:
        """Updates all of the checkmark values to the
        values contained in certain keys of a dictionary.
        
        Args:
            update_dict (dict): The dict containing the values
                to update the checkboxes to. Also contains
                values that will not be accessed or altered
                by this method.
        
        Returns:
            None
        """
        for key in self.check_values.keys():
            self.check_values[key].set(update_dict[key])
        return

    def get_check_value(self,
                        key : str) -> bool:
        """Given a dict key, returns the boolean value
        stored in the key's location.

        The method will return False if the key is not found in
        the dictionary.
        
        Args:
            key (str): Key to be accessed.
            
        Returns:
            bool: Returns the value stored at the dict key.
        """
        if key not in self.check_values:
            print(f'Key {key} not found in check_values.') # remove for prod(?)
            return False
        return self.check_values[key].get()

__all__ = ['CheckBoxToggle']