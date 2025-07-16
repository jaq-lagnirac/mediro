# Justin Caringal
#
# Functions for use in the Mediro Media Directory
# Formats main window that is displayed to the user,
# handles GUI window functionalities


### LIBRARIES / PACKAGES ###

import os
import tkinter as tk
from PIL import ImageTk, Image
from mediro_paths import resource_path
from gui_widgets import MainLogo


### GLOBAL CONSTANTS / VARIABLES ###

FONT_NAME = 'Verdana'
FONT_SIZE = 10
FONT_INFO = (FONT_NAME, FONT_SIZE)
LOGO_PATH = resource_path(os.path.join('.', 'images', 'logo-color.png'))


### FUNCTIONS ###

def insert_main_logo(root : tk.Tk) -> None:
    """Puts up splash image down left-hand side of main window.
    
    A function to handle the logo image on the main page.
    
    Args:
        root (tk.Tk): Tkinter window to be edited.
    
    Returns:
        None
    """

    # opens and resizes image
    IMAGE_MULTIPLIER = 0.2
    image = Image.open(LOGO_PATH)
    image = image.resize(size=[int(IMAGE_MULTIPLIER * length) \
                               for length in image.size])
    
    # converts image to format usable by tkinter
    IMAGE_ROW = 0
    IMAGE_COLUMN = 0
    ARBITRARILY_LARGE_NUM = 100 # to take up entire left side
    YPAD_TOP = 20
    YPAD_BOT = 20
    logo = ImageTk.PhotoImage(image)
    tk.Label(root, image=logo).grid(row=IMAGE_ROW,
                                    column=IMAGE_COLUMN,
                                    rowspan=ARBITRARILY_LARGE_NUM,
                                    pady=(YPAD_TOP, YPAD_BOT))
    # label = tk.Label(root, text='test')
    # label.grid(row=1, column=0)

    return root


def test(root):
    label = tk.Label(root, text='test')
    label.grid(row=1, column=0)


def generate_main_window() -> tk.Tk:
    """Generates GUI window to display to the user.
    
    A function which handles the formatting and generation for
    the main window. Does not run mainloop.
    
    Args:
        None
    
    Returns:
        tk.Tk: Returns a filled tkinter window.
    """

    # declares main window object
    root = tk.Tk()
    root.resizable(False, False)
    root.title('Mediro')

    # IMAGE_MULTIPLIER = 0.2
    # image = Image.open(LOGO_PATH)
    # image = image.resize(size=[int(IMAGE_MULTIPLIER * length) \
    #                            for length in image.size])
    
    # # converts image to format usable by tkinter
    # IMAGE_ROW = 0
    # IMAGE_COLUMN = 0
    # ARBITRARILY_LARGE_NUM = 100 # to take up entire left side
    # YPAD_TOP = 20
    # YPAD_BOT = 20
    # logo = ImageTk.PhotoImage(image)
    # tk.Label(root, image=logo).grid(row=IMAGE_ROW,
    #                                 column=IMAGE_COLUMN,
    #                                 rowspan=ARBITRARILY_LARGE_NUM,
    #                                 pady=(YPAD_TOP, YPAD_BOT))

    MainLogo(root)

    root.mainloop()


# code to test window generation
if __name__ == "__main__":
    generate_main_window()

__all__ = ['generate_main_window']