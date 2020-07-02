#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Open the pg30.db database file and test getting a verse from it.

After build.py has been run successfully, this standalone program can be used
to see if it worked properly. Press "Enter" to exit the program when done."""

import datetime
import sqlite3

# Public Names
__all__ = (
    'main',
)

# Module Documentation
__version__ = 1, 0, 1
__date__ = datetime.date(2020, 6, 30)
__author__ = 'Stephen Paul Chappell'
__credits__ = 'Summer Computer Science Camp'


def main(book, chapter, verse):
    connection = sqlite3.connect('pg30.db')
    cursor = connection.cursor()
    cursor.execute('''\
SELECT content
  FROM bible
 WHERE book = ?
   AND chapter = ?
   AND verse = ?''', (book, chapter, verse))
    text = cursor.fetchone()[0]
    input(text)


if __name__ == '__main__':
    main(17, 8, 9)
