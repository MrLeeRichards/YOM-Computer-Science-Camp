#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide an interface for creating threads that can be easily aborted.

Python has lightweight threads along with actual Thread objects. However, it
does not provide an easy way to kill them. This module fixes that problem."""

import datetime
import _thread
import ctypes as _ctypes
import threading as _threading

# Public Names
__all__ = (
    'set_async_exc',
    'interrupt',
    'exit',
    'ThreadAbortException',
    'Thread'
)

# Module Documentation
__version__ = 1, 0, 1
__date__ = datetime.date(2020, 6, 30)
__author__ = 'Stephen Paul Chappell'
__credits__ = 'Summer Computer Science Camp'

# Symbolic Constants
_NULL = _ctypes.py_object()
_PyThreadState_SetAsyncExc = _ctypes.pythonapi.PyThreadState_SetAsyncExc
# noinspection SpellCheckingInspection
_PyThreadState_SetAsyncExc.argtypes = _ctypes.c_ulong, _ctypes.py_object
_PyThreadState_SetAsyncExc.restype = _ctypes.c_int

# noinspection PyUnreachableCode
if __debug__:
    # noinspection PyShadowingBuiltins
    def _set_async_exc(id, exc):
        """Call the Python's C API while providing helpful error messages."""
        if not isinstance(id, int):
            raise TypeError(f'{id!r} not an int instance')
        if exc is not _NULL:
            if not isinstance(exc, type):
                raise TypeError(f'{exc!r} not a type instance')
            if not issubclass(exc, BaseException):
                raise SystemError(f'{exc!r} not a BaseException subclass')
        return _PyThreadState_SetAsyncExc(id, exc)
else:
    _set_async_exc = _PyThreadState_SetAsyncExc


# noinspection PyShadowingBuiltins
def set_async_exc(id, exc, *args):
    """Set an asynchronous exception on a target thread to be raised ASAP."""
    if args:
        class StateInfo(exc):
            def __init__(self):
                super().__init__(*args)

        return _set_async_exc(id, StateInfo)
    return _set_async_exc(id, exc)


def interrupt(ident=None):
    """Allow thread interrupts to be raised on threads other than main."""
    if ident is None:
        _thread.interrupt_main()
    else:
        set_async_exc(ident, KeyboardInterrupt)


# noinspection PyShadowingBuiltins
def exit(ident=None):
    """Give callers a way to raise SystemExit on threads other than main."""
    if ident is None:
        _thread.exit()
    else:
        set_async_exc(ident, SystemExit)


class ThreadAbortException(SystemExit):
    """Gives threads a special exception they can catch if desired."""


class Thread(_threading.Thread):
    """Extends thread objects with methods for raising remote exceptions."""

    def set_async_exc(self, exc, *args):
        """Set an asynchronous exception on this thread to be raised ASAP."""
        return set_async_exc(self.ident, exc, *args)

    def interrupt(self):
        """Allow thread interrupts to be raised on this thread."""
        self.set_async_exc(KeyboardInterrupt)

    def exit(self):
        """Give callers a way to raise SystemExit on this thread.."""
        self.set_async_exc(SystemExit)

    def abort(self, *args):
        """Schedule a ThreadAbortException to be raised on this thread."""
        self.set_async_exc(ThreadAbortException, *args)

    def reset_abort(self):
        """Try to cancel a scheduled exception if possible."""
        self.set_async_exc(_NULL)
