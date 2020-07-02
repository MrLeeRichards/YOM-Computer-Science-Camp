#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Demonstration of how to hide a window temporarily.

This program simply displays a button that can be clicked by the user. Once
clicked, the window hides itself for a few seconds and then reappears."""

import datetime
import tkinter.ttk

# Public Names
__all__ = (
    'main',
)

# Module Documentation
__version__ = 1, 0, 1
__date__ = datetime.date(2020, 7, 2)
__author__ = 'Stephen Paul Chappell'
__credits__ = 'Summer Computer Science Camp'


def main():
    """Launch a GUI demo using procedural code instead of using classes."""
    tkinter.NoDefaultRoot()
    # Create a window where the various widgets will be shown.
    root = tkinter.Tk()
    root.resizable(False, False)
    root.title('GUI Test')

    def hide_and_show_window():
        """Hide the root and then display it again a few seconds later."""
        root.withdraw()
        root.after(5000, root.deiconify)

    # Create a few widgets, but do not place them on the screen just yet.
    textbox = tkinter.ttk.Entry(root)
    action_button = tkinter.ttk.Button(
        root, text='Hide', command=hide_and_show_window)
    # Use the grid manager to make the widgets visible in the window.
    textbox.grid(row=0, column=0, padx=5, pady=5)
    action_button.grid(row=0, column=1, padx=5, pady=5)
    # Run the application event loop so that it is displayed on the screen.
    root.mainloop()


if __name__ == '__main__':
    main()
