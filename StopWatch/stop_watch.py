#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example of how to create a GUI timing application.

This program demonstrates how a timer can be created in Python
that has a graphical user interface implemented using the tkinter
module. The code uses on object-oriented approach to creating the
program but could have been written using procedural code instead."""

import datetime
import time
import tkinter.ttk
from tkinter.constants import *

# Public Names
__all__ = (
    'StopWatch',
)

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2020, 6, 30)
__author__ = 'Stephen Paul Chappell'
__credits__ = 'Summer Computer Science Camp'


class StopWatch(tkinter.ttk.Frame):
    """Describes how to build and allow operations on a timer widget."""

    PADDING = dict(padx=5, pady=5)  # Create a configurable static variable.

    @classmethod
    def main(cls):
        """Create a GUI root for the application and place a timer in it."""
        tkinter.NoDefaultRoot()
        root = tkinter.Tk()
        root.title('Stop Watch')
        root.resizable(True, False)
        root.minsize(250, 1)
        widget = cls(root)
        widget.grid(sticky=NSEW, **cls.PADDING)
        root.grid_columnconfigure(0, weight=1)
        root.mainloop()

    def __init__(self, master=None, **kw):
        """Initialize the StopWatch widget with the variables it will need."""
        super().__init__(master, **kw)
        self.__time_string = tkinter.StringVar(self, '0.000000')
        # Create a few widgets that will be contained in this Frame.
        self.__time_label = tkinter.ttk.Label(
            self, text='Total Time:')
        self.__time_display = tkinter.ttk.Label(
            self, textvariable=self.__time_string)
        self.__mode_button = tkinter.ttk.Button(
            self, text='Start', command=self.toggle_mode)
        # Store some information that will track how much time has elapsed.
        self.__start_time = 0
        self.__total_time = 0
        self.__action_handle = None
        # Place all the widgets created up above on the grid to be displayed.
        self.grid_all_widgets()

    def toggle_mode(self):
        """Change whether or not the stop watch is tracking elapsed time."""
        if self.__mode_button['text'] == 'Start':
            self.__mode_button['text'] = 'Stop'
            self.__start_time = time.perf_counter()
            self.__action_handle = self.after_idle(self.update_timer)
        elif self.__mode_button['text'] == 'Stop':
            self.__mode_button['text'] = 'Start'
            self.after_cancel(self.__action_handle)
        else:
            raise RuntimeError('there is a bug in my program')

    def grid_all_widgets(self):
        """Tell each contained widget where to display within this Frame."""
        self.__time_label.grid(row=0, column=0, sticky=E, **self.PADDING)
        self.__time_display.grid(row=0, column=1, sticky=W, **self.PADDING)
        self.__mode_button.grid(
            row=1, column=0, columnspan=2, sticky=EW, **self.PADDING)
        self.grid_columnconfigure(1, weight=1)

    def update_timer(self):
        """Check elapsed time and update the time string with the new value."""
        current_time = time.perf_counter()
        time_difference = current_time - self.__start_time
        self.__start_time = current_time
        self.__total_time += time_difference
        self.__time_string.set(f'{self.__total_time:.6f}')
        self.__action_handle = self.after_idle(self.update_timer)


if __name__ == '__main__':
    StopWatch.main()
