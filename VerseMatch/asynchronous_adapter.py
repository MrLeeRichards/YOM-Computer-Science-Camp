#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adapt asynchronous module to act like old add_timeout class.

This is a drop-in replacement for the timeout module. Instead of using the
multiprocessing module directly, it uses asynchronous functionality instead."""

import datetime
import asynchronous

# Public Names
__all__ = (
    'add_timeout',
)

# Module Documentation
__version__ = 1, 0, 1
__date__ = datetime.date(2020, 6, 30)
__author__ = 'Stephen Paul Chappell'
__credits__ = 'Summer Computer Science Camp'


# noinspection PyPep8Naming
class add_timeout:
    """Adds a timeout to a function in an easy-to-use interface."""

    def __init__(self, function, limit=60):
        """Initialize instance with the variables it will need to work with."""
        self._executor = asynchronous.Executor(limit)
        self._function = function
        self._future = None

    def __call__(self, *args, **kwargs):
        """Create a future using the instance's stored Executor object."""
        self._future = self._executor.submit(self._function, *args, **kwargs)

    def cancel(self):
        """Try to cancel running a Future instance."""
        self._future.cancel()

    @property
    def ready(self):
        """Read-only property giving the underlying function's status."""
        return (False if not self._future.done() else
                True if not self._future.cancelled() else
                None)

    @property
    def value(self):
        """Read-only property giving the result from running a function."""
        return self._future.result()
