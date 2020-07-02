#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create interface to async_exc like one provided by old add_timeout class,

When this program was originally written, processes were used instead of
threads. Threads can be terminated, and this is an alternative API for them."""

import datetime
import queue
import time

import async_exc
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
    """Wraps function (not methods) so that they can have a timeout."""

    def __init__(self, function, limit=60):
        """Initialize an add_timeout instance with some data it needs"""
        self._target = function
        self._limit = limit
        self._thread = None
        # noinspection PyUnresolvedReferences
        self._queue = queue.SimpleQueue()
        self._timeout = None
        self._result = None

    def __call__(self, *args, **kwargs):
        """Begin executing the wrapped function and allow termination."""
        # noinspection PyProtectedMember
        self._thread = async_exc.Thread(
            target=asynchronous._run,
            args=(self._target, args, kwargs, self._queue)
        )
        self._thread.start()
        self._timeout = time.perf_counter() + self._limit

    def cancel(self):
        """Force the underlying thread to terminate its execution,"""
        self._thread.exit()

    @property
    def ready(self):
        """Read-only property for the status of function's result."""
        if self._thread.is_alive():
            if time.perf_counter() > self._timeout:
                self.cancel()
                self._thread.join()
            else:
                return False
        if not self._queue.empty():
            self._result = self._queue.get_nowait()
        error, value = self._result
        if not error or not isinstance(value, SystemExit):
            return True

    @property
    def value(self):
        """Read-only property for the value returned from function."""
        error, value = self._result
        if error and not isinstance(value, SystemExit):
            raise value
        return value
