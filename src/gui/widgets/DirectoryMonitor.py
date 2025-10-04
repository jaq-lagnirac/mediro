# Justin Caringal
# 
# A monitor of the make-up of the files in a given directory
#
# Loosely based on stack overflow post linked below:
# https://stackoverflow.com/a/41684432

import os
import time
import threading
import tkinter as tk
from tkinter import ttk
from queue import Queue
from constants import *
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class DirEventHandler(FileSystemEventHandler):

    def __init__(self, monitor):
        FileSystemEventHandler.__init__(self)
        self.monitor = monitor

    def on_any_event(self, event: FileSystemEvent) -> None:
        """Overriding FileSystemEventHandler method.
        
        A function to react to any change in a target directory.
        
        Args:
            event (watchdog.events.FileSystemEventHandler): An object
                which contains information in the target directory,
                not directly accessed.
        
        Returns:
            None
        """
        self.monitor.notify(event)

class DirectoryMonitor(ttk.Frame):

    """
    A class to display the contents of a target directory.
    """

    NO_FILES_FOUND = {'No files found.' : ''}
    NOT_DIR = {'Not a directory.' : ''}
    _DEFAULT_OUTPUT_WIDTH = 50
    _DEFAULT_COL_SPAN = 1
    _FRAME_PADX_LEFT = 10
    _FRAME_PADX_RIGHT = 10
    _OUTPUT_FONT_INFO = ('Courier New', 12)

    def __init__(self,
                 master : tk.Tk = None,
                 *, # requires keyword arguments
                 target_directory : str = '.',
                 row : int = _ORIGIN_ROW,
                 column : int = (_ORIGIN_COL + 1),
                 output_width : int = _DEFAULT_OUTPUT_WIDTH,
                 col_span : int = _DEFAULT_COL_SPAN) -> None:
        """Initializes the frame to start monitoring a target directory.

        Args:
            master (tk.Tk): The root object of the textbox.
            target_directory (str): The directory to watch.
            row (int): The placement row of the created object.
            column (int): The placement column of the created object.
            output_width (int): The width of the Entry object.
            col_span (int): The number of columns that the object takes up.
            
        Returns:
            None
        """

        super().__init__(master)
        self.event_handler = DirEventHandler(self)
        self.target_dir = target_directory
        self.col = column
        self.row = row
        self.output_width = output_width
        self.col_span = col_span
        self.thread_hash = {}

        self.queue = Queue()

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
                                   height=10,
                                   width=self.output_width)
        self.output_text.grid(row=_ORIGIN_ROW,
                              column=_ORIGIN_COL,
                              columnspan=3)
        self.output_text.config(state='disabled')

        # binds methods to events
        # self.master.bind('<Destroy>', self.cleanup_observer)
        self.master.bind('<<WatchdogEvent>>', self.handle_watchdog_event)
        
    def __del__(self) -> None:
        """Class destructor"""
        self.cleanup_observer()

    def update_target_dir(self, target_directory : str) -> None:
        """Starts up observer, or retargets observer to new
        target directory.
        
        Args:
            target_directory (str): The directory to be monitored.
        
        Returns:
            None
        """

        # adds new path if not in thread hash
        self.target_dir = target_directory
        if self.target_dir not in self.thread_hash:
            self.thread_hash[self.target_dir] = threading.Event()
        
        # clears all events, making all threads inactive
        for path, _ in self.thread_hash.items():
            self.thread_hash[path].clear()
        
        # enables start flag for specific thread
        self.thread_hash[self.target_dir].set()

        watchdog_thread = threading.Thread(target=self.start_watchdog_thread,
                                           args=(target_directory,))
        watchdog_thread.daemon = True # enables daemon thread (exits with main)
        watchdog_thread.start()
        self.notify()
        return

    def start_watchdog_thread(self, target_directory : str) -> None:
        """Starts up a new thread for watchdog to monitor a new directory.
        
        Args:
            target_directory (str): The directory to be monitored.
        
        Returns:
            None
        """
        observer = Observer()
        observer.schedule(self.event_handler,
                               target_directory,
                               recursive=False)
        observer.start()
        try:
            while self.thread_hash[target_directory].is_set():
                time.sleep(0.1) # keeps thread alive
        finally:
            observer.stop()
            observer.join()


    def get_dir_info(self) -> dict:
        """Gathers and formats the file makeup of the target directory.
        
        Args:
            None
        
        Returns:
            dict: Returns a hash table of filetypes and counts
        """

        # counts file types in target directory
        extension_hash = {}
        for file in os.listdir(self.target_dir):
            _, ext = os.path.splitext(file)
            if not ext:
                ext = 'Directory'
            if ext not in extension_hash:
                extension_hash[ext] = 0
            extension_hash[ext] += 1

        # if extension_hash is empty, notify user
        if not extension_hash:
            return self.NO_FILES_FOUND

        return extension_hash
    
    def format_file_info(self, extension_hash : dict) -> str:
        """Formats the a dict of filetype info into
        a printable string.
        
        Args:
            file_info (dict): A hash table of filetypes and counts.
        
        Returns:
            str: Returns formatted text of target directory.
        """

        # heading
        EXT_SPACING_WIDTH = 15
        COUNT_SPACING_WIDTH = 10
        file_info = f'{"File Types":<{EXT_SPACING_WIDTH}}' \
            f'{"Count":<{COUNT_SPACING_WIDTH}}\n' + \
            '-' * (EXT_SPACING_WIDTH + COUNT_SPACING_WIDTH) + '\n'
        
        # body
        for ext, count in extension_hash.items():
            file_info += f'{ext:<{EXT_SPACING_WIDTH}}{count}\n'
        
        return file_info
        
    def set_textbox(self, text : str) -> None:
        """Sets the textbox output shown to the user.
        
        Args:
            text (str): The text to be shown.
            
        Returns:
            None
        """
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert('end', text)
        self.output_text.config(state='disabled')
    
    def handle_watchdog_event(self, *event : tk.Event) -> None:
        """Handles watchdog event through tkinter.
        
        Updates the output textbox with information.
        
        Args:
            event (tk.Event): The tkinter event, not directly accessed.
            
        Returns:
            None
        """
        watchdog_event = self.queue.get()
        file_info = self.get_dir_info()
        formatted_info = self.format_file_info(file_info)
        self.set_textbox(formatted_info)

    def notify(self, *event : FileSystemEvent) -> None:
        """Detects a watchdog event and passes it on to tkinter.
        
        Args:
            event (watchdog.events.FileSystemEventHandler): An object
                which contains information in the target directory,
                not directly accessed.
        
        Returns:
            None
        """
        self.queue.put(event)
        self.master.event_generate('<<WatchdogEvent>>', when='tail')
        return

__all__ = ['DirectoryMonitor']
