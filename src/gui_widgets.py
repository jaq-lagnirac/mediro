# Justin Caringal
#
# Functions for use in the Mediro Media Directory
# Contains GUI widgets for use with tkinter windows


### LIBRARIES / PACKAGES ###

import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from mediro_paths import resource_path


### GLOBAL CONSTANTS / VARIABLES ###

FONT_NAME = 'Verdana'
FONT_SIZE = 10
FONT_INFO = (FONT_NAME, FONT_SIZE)
ORIGIN_ROW = 0
ORIGIN_COL = 0
ARBITRARILY_LARGE_NUM = 100 # to take up entire left side


### CLASSES ###

class MainLogo(ttk.Frame):

    _LOGO_PATH = resource_path(os.path.join('.', 'images', 'logo-color.png'))
    _LOGO_MULTIPLIER = 0.2
    _FRAME_PADX_LEFT = 0
    _FRAME_PADX_RIGHT = 10
    _PADY_TOP = 200
    _PADY_BOT = 200
    _LOGO_COLOR = '#fee869'

    def __init__(self,
                 master=None):

            # configures to window, adds styles            
            super().__init__(master)
            logo_style = ttk.Style()
            logo_style.configure('Logo.TFrame', background=self._LOGO_COLOR)
            logo_style.configure('Logo.TLabel', background=self._LOGO_COLOR)

            # positions tk.Frame in window
            self.config(style='Logo.TFrame')
            self.grid(row=ORIGIN_ROW,
                      column=ORIGIN_COL,
                      rowspan=ARBITRARILY_LARGE_NUM,
                      padx=(self._FRAME_PADX_LEFT, self._FRAME_PADX_RIGHT))
            
            # NOTE: no "self" due to garbage collector avoidance
            image = Image.open(self._LOGO_PATH) # opens image
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
            

class TextBoxQuestion(ttk.Frame):

    _LABEL_WIDTH = 20
    _TEXTBOX_WIDTH = 30
    _FRAME_PADX_LEFT = 0
    _FRAME_PADX_RIGHT = 10

    def __init__(self,
                 master=None,
                 text='',
                 row=ORIGIN_ROW,
                 column=(ORIGIN_COL + 1)):

        self.row = row
        self.col = column
        self.text = text

        super().__init__(master)
        # positions tk.Frame in window
        self.grid(row=self.row,
                  column=self.col,
                  padx=(self._FRAME_PADX_LEFT, self._FRAME_PADX_RIGHT))
        
        # label asking the user a question
        LABEL_ROW = ORIGIN_ROW
        LABEL_COL = ORIGIN_COL
        self.label = ttk.Label(self,
                               width=self._LABEL_WIDTH,
                               text=self.text,
                               anchor='w',
                               justify='left')
        self.label.grid(row=LABEL_ROW,
                        column=LABEL_COL,
                        sticky='W')
        
        # textbox collecting the user input
        TEXTBOX_ROW = ORIGIN_ROW
        TEXTBOX_COL = ORIGIN_COL + 1
        self.text_str = tk.StringVar()
        self.textbox = ttk.Entry(self,
                                 width=self._TEXTBOX_WIDTH,
                                 textvariable=self.text_str)
        self.textbox.grid(row=TEXTBOX_ROW,
                          column=TEXTBOX_COL,
                          sticky='NESW')