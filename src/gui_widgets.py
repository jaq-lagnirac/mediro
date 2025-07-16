# Justin Caringal
#
# Functions for use in the Mediro Media Directory
# Contains GUI widgets for use with tkinter windows


### LIBRARIES / PACKAGES ###

import os
import tkinter as tk
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

class MainLogo(tk.Frame):

    LOGO_PATH = resource_path(os.path.join('.', 'images', 'logo-color.png'))
    LOGO_MULTIPLIER = 0.2
    FRAME_PADX_LEFT = 0
    FRAME_PADX_RIGHT = 25
    PADY_TOP = 200
    PADY_BOT = 200
    LOGO_COLOR = '#fee869'

    def __init__(self,
                 master=None):
            
            super().__init__(master)
            # positions tk.Frame in window
            self.config(background=self.LOGO_COLOR)
            self.grid(row=ORIGIN_ROW,
                      column=ORIGIN_COL,
                      rowspan=ARBITRARILY_LARGE_NUM,
                      padx=(self.FRAME_PADX_LEFT, self.FRAME_PADX_RIGHT))
            
            # NOTE: no "self" due to garbage collector avoidance
            image = Image.open(self.LOGO_PATH) # opens image
            resized_dims = [int(self.LOGO_MULTIPLIER * length) \
                                 for length in image.size]
            image = image.resize(size=resized_dims)

            # puts displays image in frame
            image = ImageTk.PhotoImage(image)
            self.logo = tk.Label(self, image=image, background=self.LOGO_COLOR)
            self.logo.image = image
            self.logo.grid(pady=(self.PADY_TOP, self.PADY_BOT))
            
