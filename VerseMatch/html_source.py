#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Define several XHTML document strings to be used in VerseMatch.

Unlike the original program written in Java, a large portion of the
XHTML code is defined separately here to be used as format strings."""

import datetime
import math
import pathlib
import sys

# Public Names
__all__ = (
)

# Module Documentation
__version__ = 1, 0, 5
__date__ = datetime.date(2020, 6, 30)
__author__ = 'Stephen Paul Chappell'
__credits__ = 'Summer Computer Science Camp'


def __getattr__(name):
    """Get HTML templates from ROOT while caching the file contents."""
    if name.isupper():  # Is the name for a constant value?
        path = (__getattr__.ROOT / name.casefold()).with_suffix('.html')
        if path.is_file():
            modified = path.stat().st_mtime
            cache_time, text = __getattr__.CACHE.get(name, (-math.inf, None))
            if cache_time < modified:
                with path.open() as file:
                    text = file.read()
                __getattr__.CACHE[name] = modified, text
            return text
        else:
            __getattr__.CACHE.pop(name, None)
    raise AttributeError(name)


__getattr__.CACHE = {}
__getattr__.ROOT = pathlib.Path(sys.argv[0]).parent / 'templates'
