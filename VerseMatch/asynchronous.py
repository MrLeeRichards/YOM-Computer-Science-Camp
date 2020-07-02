#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrap the multiprocessing module with an alternative interface.

Processes do not automatically have timeouts associated with them. This module
remedies that problem and provides classes for Executors and Futures."""

import _thread
import abc as _abc
import collections as _collections
import datetime as _datetime
import enum as _enum
import math as _math
import multiprocessing as _multiprocessing
import operator as _operator
import queue as _queue
import signal as _signal
import sys as _sys
import time as _time

# Public Names
__all__ = (
    'Executor',
    'get_timeout',
    'set_timeout',
    'submit',
    'map_',
    'shutdown'
)

# Module Documentation
__version__ = 1, 0, 1
__date__ = _datetime.date(2020, 6, 30)
__author__ = 'Stephen Paul Chappell'
__credits__ = 'Summer Computer Science Camp'


class _Base(metaclass=_abc.ABCMeta):
    """Gives child classes a common way of working with timeouts."""

    __slots__ = (
        '__timeout',
    )

    @_abc.abstractmethod
    def __init__(self, timeout):
        """Initialize the timeout value when an instance is created."""
        self.timeout = _math.inf if timeout is None else timeout

    def get_timeout(self):
        """Return the stored timeout value."""
        return self.__timeout

    def set_timeout(self, value):
        """Set the timeout after checking the value for possible errors."""
        if not isinstance(value, (float, int)):
            raise TypeError('value must be of type float or int')
        if value <= 0:
            raise ValueError('value must be greater than zero')
        self.__timeout = value

    timeout = property(get_timeout, set_timeout)


def _run_and_catch(fn, args, kwargs):
    """Run a function and report if the function succeeded or not."""
    # noinspection PyPep8,PyBroadException
    try:
        return False, fn(*args, **kwargs)
    except:
        return True, _sys.exc_info()[1]


def _run(fn, args, kwargs, queue):
    """Run a function and place the result in a queue for later processing."""
    queue.put_nowait(_run_and_catch(fn, args, kwargs))


class _State(_enum.IntEnum):
    """Enumerates all the states a Future instance can be in."""
    PENDING = _enum.auto()
    RUNNING = _enum.auto()
    CANCELLED = _enum.auto()
    FINISHED = _enum.auto()
    ERROR = _enum.auto()


def _run_and_catch_loop(iterable, *args, **kwargs):
    """Extract functions from an iterable and run with common arguments."""
    exception = None
    for fn in iterable:
        error, value = _run_and_catch(fn, args, kwargs)
        if error:
            exception = value
    if exception:
        raise exception


class _Future(_Base):
    """Encapsulates the idea of something that can be run in the future."""

    __slots__ = (
        '__queue',
        '__process',
        '__start_time',
        '__callbacks',
        '__result',
        '__mutex'
    )

    def __init__(self, timeout, fn, args, kwargs):
        """Initialize the instance for running a separate process."""
        super().__init__(timeout)
        self.__queue = _multiprocessing.Queue(1)
        self.__process = _multiprocessing.Process(
            target=_run,
            args=(fn, args, kwargs, self.__queue),
            daemon=True
        )
        self.__start_time = _math.inf
        self.__callbacks = _collections.deque()
        self.__result = True, TimeoutError()
        self.__mutex = _thread.allocate_lock()

    @property
    def __state(self):
        """Read-only property for calculating the Future's state."""
        pid, exitcode = self.__process.pid, self.__process.exitcode
        return (_State.PENDING if pid is None else
                _State.RUNNING if exitcode is None else
                _State.CANCELLED if exitcode == -_signal.SIGTERM else
                _State.FINISHED if exitcode == 0 else
                _State.ERROR)

    def __repr__(self):
        """Create a string representation for this Future."""
        root = f'{type(self).__name__} at {id(self)} state={self.__state.name}'
        if self.__state < _State.CANCELLED:
            return f'<{root}>'
        error, value = self.__result
        suffix = f'{"raised" if error else "returned"} {type(value).__name__}'
        return f'<{root} {suffix}>'

    def __consume_callbacks(self):
        """Iterate through all the callbacks stored in this Future."""
        while self.__callbacks:
            yield self.__callbacks.popleft()

    def __invoke_callbacks(self):
        """Run all of the callbacks in a safe environment."""
        self.__process.join()
        _run_and_catch_loop(self.__consume_callbacks(), self)

    def cancel(self):
        """Try to cancel the running of this Future if possible."""
        self.__process.terminate()
        self.__invoke_callbacks()

    def __auto_cancel(self):
        """Automatically cancel execution if the timeout is over."""
        elapsed_time = _time.perf_counter() - self.__start_time
        if elapsed_time > self.timeout:
            self.cancel()
        return elapsed_time

    def cancelled(self):
        """Return whether or not this Future is in a cancelled state."""
        self.__auto_cancel()
        return self.__state is _State.CANCELLED

    def running(self):
        """Check whether or not this Future is in a running state."""
        self.__auto_cancel()
        return self.__state is _State.RUNNING

    def done(self):
        """Return whether or not this instance is finished running."""
        self.__auto_cancel()
        return self.__state > _State.RUNNING

    def __handle_result(self, error, value):
        """Store the result of completely running the Future."""
        self.__result = error, value
        self.__invoke_callbacks()

    def __ensure_termination(self):
        """Force the instance to be in a terminated state."""
        with self.__mutex:
            elapsed_time = self.__auto_cancel()
            if not self.__queue.empty():
                self.__handle_result(*self.__queue.get_nowait())
            elif self.__state < _State.CANCELLED:
                remaining_time = self.timeout - elapsed_time
                if remaining_time == _math.inf:
                    remaining_time = None
                try:
                    result = self.__queue.get(True, remaining_time)
                except _queue.Empty:
                    self.cancel()
                else:
                    self.__handle_result(*result)

    def result(self):
        """Return the result of running the Future."""
        self.__ensure_termination()
        error, value = self.__result
        if error:
            raise value
        return value

    def exception(self):
        """If there was an exception, return it instead of raising it."""
        self.__ensure_termination()
        error, value = self.__result
        if error:
            return value

    def add_done_callback(self, fn):
        """Add a callback to run after termination."""
        if self.done():
            fn(self)
        else:
            self.__callbacks.append(fn)

    def _set_running_or_notify_cancel(self):
        """Signal the instance to begin running or to stop."""
        if self.__state is _State.PENDING:
            self.__process.start()
            self.__start_time = _time.perf_counter()
        else:
            self.cancel()


class Executor(_Base):
    """Allows Future instances to be grouped together and run easily."""

    __slots__ = (
        '__futures',
    )

    def __init__(self, timeout=None):
        """Initialize the instance with no running Futures."""
        super().__init__(timeout)
        self.__futures = set()

    def submit(self, fn, *args, **kwargs):
        """Begin running a future and return it to the caller."""
        future = _Future(self.timeout, fn, args, kwargs)
        self.__futures.add(future)
        future.add_done_callback(self.__futures.remove)
        # noinspection PyProtectedMember
        future._set_running_or_notify_cancel()
        return future

    @staticmethod
    def __cancel_futures(iterable):
        """Automatically cancel all running Futures in this Executor,"""
        _run_and_catch_loop(map(_operator.attrgetter('cancel'), iterable))

    def map(self, fn, *iterables):
        """Map an iterable to be run on a single function."""
        futures = tuple(self.submit(fn, *args) for args in zip(*iterables))

        def result_iterator():
            future_iterator = iter(futures)
            try:
                for future in future_iterator:
                    yield future.result()
            finally:
                self.__cancel_futures(future_iterator)

        return result_iterator()

    def shutdown(self):
        """Stop all Futures from this instance to stop executing."""
        self.__cancel_futures(frozenset(self.__futures))

    def __enter__(self):
        """Provide support for entering a with block of code."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Automatically terminate running Futures on exiting a with block."""
        self.shutdown()
        return False


# Symbolic Constants
_executor = Executor()
get_timeout = _executor.get_timeout
set_timeout = _executor.set_timeout
submit = _executor.submit
map_ = _executor.map
shutdown = _executor.shutdown
del _executor
