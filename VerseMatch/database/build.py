#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a database file that contains the entire Bible in it.

This is a standalone program used to create the pg30.db database file that has
the entire Bible. The database is used by the Bible Verse Quiz program."""

import datetime
import mmap
import pathlib
import sqlite3

# Public Names
__all__ = (
    'main',
    'parse_bible'
)

# Module Documentation
__version__ = 1, 0, 1
__date__ = datetime.date(2020, 6, 30)
__author__ = 'Stephen Paul Chappell'
__credits__ = 'Summer Computer Science Camp'


def main():
    """Read the pg30.txt Bible file and create the pg30.db database file."""
    bible = parse_bible(pathlib.Path('pg30.txt'))
    # Create the database being built.
    connection = sqlite3.connect('pg30.db')
    cursor = connection.cursor()
    cursor.execute('''\
CREATE TABLE bible (
  book    INTEGER,
  chapter INTEGER,
  verse   INTEGER,
  content TEXT
)''')
    # Add all verses to database.
    for book_i, book in enumerate(bible, 1):
        for chapter_i, chapter in enumerate(book, 1):
            for verse_i, verse in enumerate(chapter, 1):
                cursor.execute('''\
INSERT INTO bible (
  book,
  chapter,
  verse,
  content
) VALUES (?, ?, ?, ?)''',
                               (book_i, chapter_i, verse_i, verse))
    # Commit changes and close database.
    connection.commit()
    connection.close()


def parse_bible(path):
    """Take a specially formatted file and extract the Bible's structure."""
    book = chapter = verse = 1
    book_list, chapter_list, verse_list = [], [], []
    start = 0
    with path.open('rb') as file:
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as bible:
            for next_line in b'\r\n', b'\r', b'\n':
                if bible.find(next_line) >= 0:
                    break
            else:
                raise EOFError('could not find any line delimiters')
            while True:
                sub = f'{book:02}:{chapter:03}:{verse:03} '.encode()
                index = bible.find(sub, start)
                if index >= 0:
                    start = index + len(sub)
                    end = bible.find(next_line * 2, start)
                    if end < 0:
                        raise EOFError('could not find the end of the verse')
                    bible.seek(start)
                    verse_text = bible.read(end - start).decode()
                    verse_list.append(' '.join(verse_text.split()))
                    start = end
                    verse += 1
                elif verse != 1:
                    chapter_list.append(tuple(verse_list))
                    verse_list.clear()
                    chapter += 1
                    verse = 1
                elif chapter != 1:
                    book_list.append(tuple(chapter_list))
                    chapter_list.clear()
                    book += 1
                    chapter = 1
                elif book != 1:
                    return tuple(book_list)
                else:
                    raise EOFError('could not find any of the expected data')


if __name__ == '__main__':
    main()
