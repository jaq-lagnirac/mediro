# Justin Caringal
# 
# A logo widget for display on the lefthand
# side of the main window for Mediro

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from constants import *

class MainLogo(ttk.Frame):

    """
    A class to initialize the logo display on the main screen
    of the application.
    """

    _LOGO_MULTIPLIER = 0.2
    _FRAME_PADX_LEFT = 0
    _FRAME_PADX_RIGHT = 10
    _PADY_BASE_VALUE = 250
    _PADY_TOP = _PADY_BASE_VALUE
    _PADY_BOT = _PADY_BASE_VALUE

    def __init__(self,
                 master : tk.Tk = None) -> None:
        """Initializes the main logo.

        A function which handles the image retrieval, formatting,
        and display of the logo on the main window of the application.

        Args:
            master (tk.Tk): The root object of the logo frame.

        Returns:
            None
        """

        # configures to window, adds styles            
        super().__init__(master)
        logo_style = ttk.Style()
        logo_style.configure('Logo.TFrame', background=_LOGO_COLOR)
        logo_style.configure('Logo.TLabel', background=_LOGO_COLOR)

        # positions tk.Frame in window
        self.config(style='Logo.TFrame')
        self.grid(row=_ORIGIN_ROW,
                  column=_ORIGIN_COL,
                  rowspan=_ARBITRARILY_LARGE_NUM,
                  padx=(self._FRAME_PADX_LEFT, self._FRAME_PADX_RIGHT))
        
        # NOTE: no "self" due to garbage collector avoidance
        image = Image.open(_LOGO_PATH) # opens image
        resized_dims = [int(self._LOGO_MULTIPLIER * length) \
                        for length in image.size]
        image = image.resize(size=resized_dims)

        # puts displays image in frame
        image = ImageTk.PhotoImage(image)
        self.logo = ttk.Label(self,
                              image=image,
                              style='Logo.TLabel')
        self.logo.image = image
        self.logo.grid(pady=(self._PADY_TOP, self._PADY_BOT))

        return
    
__all__ = ['MainLogo']