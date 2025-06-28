# Justin Caringal
#
# A tool to partition a directory into subdirectories and
# sort files (originally for visual multimedia) based on
# time-of-creation


### LIBRARIES / PACKAGES ###

import os
import sys
import re
import tkinter as tk
from PIL import ImageTk, Image
from mediro_paths import resource_path


### GLOBAL CONSTANTS / VARIABLES ###

FONT_INFO = ('Verdana', 10)
LOGO_PATH = resource_path(os.path.join('.', 'images', 'logo-color.png'))
INPUT_DIR = os.path.join('.', 'MEDIRO_requires_sorting')
UNSORTED_DIR = os.path.join('.', 'MEDIRO_unsorted')


### FUNCTIONS ###

def main() -> None:
    """MAIN FUNCTION"""

    X_WIDGET_PADDING = 20
    TEXT_SIDE_PADDING = (X_WIDGET_PADDING, 0)
    INPUT_SIDE_PADDING = (0, X_WIDGET_PADDING)

    # declares main window
    root.resizable(False, False)
    root.title('Mediro')

    # formats "splash" header
    IMAGE_ROW = 0
    IMAGE_COLUMN = 0
    IMAGE_MULTIPLIER = 0.2
    image = Image.open(LOGO_PATH) # opens image
    image = image.resize(size=[int(IMAGE_MULTIPLIER * length) \
                               for length in image.size])
    # converts image to format usable by Tkinter
    logo = ImageTk.PhotoImage(image)
    tk.Label(root, image=logo).grid(row=IMAGE_ROW,
                                    column=IMAGE_COLUMN,
                                    columnspan=100,
                                    padx=(X_WIDGET_PADDING, X_WIDGET_PADDING))
    
    tk.Label(root, text='placeholder').grid(row=IMAGE_ROW + 1,
                                            column=IMAGE_COLUMN,
                                            padx=TEXT_SIDE_PADDING)

    # bottom rows
    BOTTOM_ROW = 100 # arbitrarily large number
    BUTTON_ROW = BOTTOM_ROW - 10
    STATUS_ROW = BUTTON_ROW - 1
    BUTTON_COLUMN_START = IMAGE_COLUMN + 1
    STATUS_FONT = ('Courier New', 11)
    status = tk.Label(root, text='', font=STATUS_FONT)
    status.grid(sticky='W',
                row=STATUS_ROW,
                column=IMAGE_COLUMN,
                columnspan=100,
                padx=TEXT_SIDE_PADDING,
                pady=(12, 12))
    # NOTE: sticky='NESW' used to fill box to fit column and row
    enter_button = tk.Button(root,
                             text='Enter',
                             command=lambda:print('Enter'))
    enter_button.grid(sticky='NESW',
                      row=BUTTON_ROW,
                      column=BUTTON_COLUMN_START)
    enter_button.config(state='disabled') # default state is disabled
    help_button = tk.Button(root,
                            text='Info/Help',
                            command=lambda:print('Info/Help'))
    help_button.grid(sticky='NESW',
                     row=BUTTON_ROW,
                     column=BUTTON_COLUMN_START + 1)
    cancel_button = tk.Button(root,
                              text='Cancel',
                              command=root.destroy)
    cancel_button.grid(sticky='NESW',
                       row=BUTTON_ROW,
                       column=BUTTON_COLUMN_START + 2,
                       padx=(0, X_WIDGET_PADDING))
    
    # bottom credits
    description = tk.Label(root,
                           text='\nDeveloped by Technical Services ' + \
                            '& Systems, Pickler Memorial Library, ' + \
                            'Truman State University, MO, 2024\n' + \
                            'Raw ver. info.: Z2l0aHViQGphcS1sYWduaXJhYw==',
                           justify='left',
                           font=(FONT_INFO[0], 7))
    description.grid(sticky='W', row=BOTTOM_ROW, column=0, columnspan=100)

    # starts up main window
    root.mainloop()

### MAIN LOOP ###
if __name__ == '__main__':
    root = tk.Tk() # initializes global root window
    main() # starts main loop
