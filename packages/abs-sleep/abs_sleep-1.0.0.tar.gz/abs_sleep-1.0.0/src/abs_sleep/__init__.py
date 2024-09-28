from ctypes import CDLL, Structure, c_long, byref
from math import ceil
import time
import os

NANOS_IN_SEC = int(1e9)

HAVE_LIBC_ABSTIME = False

# try to import libc on Linux
try:
    if os.uname().sysname == "Linux":
        libc = CDLL("libc.so.6")
        HAVE_LIBC_ABSTIME = True
except OSError:
    pass


# https://man7.org/linux/man-pages/man2/clock_nanosleep.2.html
class TimeSpec(Structure):
    "FFI representation of libc's `struct timespec`"

    _fields_ = [
        ("tv_sec", c_long),  # really, time_t
        ("tv_nsec", c_long),
    ]

    @staticmethod
    def from_seconds(secs: float):
        "Consruct a new `TimeSpec` struct for a given timestamp from `time.clock_monotonic()`."
        return TimeSpec.from_nanoseconds(int(ceil(secs * NANOS_IN_SEC)))

    @staticmethod
    def from_nanoseconds(nsecs: int):
        "Consruct a new `TimeSpec` struct for a given timestamp from `time.clock_monotonic()`."
        ns = int(nsecs)
        return TimeSpec(ns // NANOS_IN_SEC, ns % NANOS_IN_SEC)


if HAVE_LIBC_ABSTIME:
    # Linux: https://github.com/torvalds/linux/blob/v6.11/include/uapi/linux/time.h#L73
    # FreeBSD: https://github.com/freebsd/freebsd-src/blob/release/14.1.0/sys/sys/_clock_id.h#L90
    # NetBSD: https://github.com/NetBSD/src/blob/netbsd_3_1/sys/sys/time.h#L171
    TIMER_ABSTIME = 1

    def abs_nanosleep(nsecs: int, clock: int = time.CLOCK_MONOTONIC) -> bool:
        """Sleep until the absolute given point in time (in ns).
        Returns True if the sleep was successful; False if interrupted.

        Available on Linux only.

        Keyword argument:
        clock -- what clock ID to use (default: time.CLOCK_MONOTONIC)
        """
        ts = TimeSpec.from_nanoseconds(nsecs)
        # https://man7.org/linux/man-pages/man2/clock_nanosleep.2.html
        err = libc.clock_nanosleep(clock, TIMER_ABSTIME, byref(ts), None)
        return err == 0

    def abs_sleep(secs: float, clock: int = time.CLOCK_MONOTONIC) -> bool:
        """Sleep until the absolute given point in time (in seconds).
        Returns True if the sleep was successful; False if interrupted.

        Available on Linux only.

        Keyword argument:
        clock -- what clock ID to use (default: time.CLOCK_MONOTONIC)
        """
        ts = TimeSpec.from_seconds(secs)
        # https://man7.org/linux/man-pages/man2/clock_nanosleep.2.html
        err = libc.clock_nanosleep(clock, TIMER_ABSTIME, byref(ts), None)
        return err == 0

else:
    # We don't have clock_nanosleep available, so approximate loosely.

    def abs_sleep(secs: float, clock: int = 0) -> bool:
        "An inexact approximation of an absolutely timed sleep (given in seconds)."
        # This of course doesn't always work, but as of Python 3.12 there
        # doesn't appear to be an absolutely timed sleep in the Python
        # standard library that we could instead.
        time.sleep(max(0, secs - time.monotonic()))
        return True

    def abs_nanosleep(nsecs: int, clock: int = 0) -> bool:
        "An inexact approximation of an absolutely timed sleep (given in ns)."
        return abs_sleep(nsecs / NANOS_IN_SEC)


class PeriodicActivationsIter:
    """Iterator for periodic activations (w.r.t. time.CLOCK_MONOTONIC).

    All parameters specified in seconds (float).
    """

    def __init__(
        self,
        period_secs,
        offset_secs=0,
        start_time_secs=None,
        align_secs=None,
        release_jitter=None,
        sporadic_delay=None,
    ):
        self.period_ns = int(round(period_secs * NANOS_IN_SEC))
        self.release_jitter = release_jitter
        self.sporadic_delay = sporadic_delay

        if start_time_secs is None:
            self.next_activation_time = time.monotonic_ns() + self.period_ns
        else:
            self.next_activation_time = int(round(start_time_secs * NANOS_IN_SEC))

        if align_secs:
            align = int(round(align_secs * NANOS_IN_SEC))
            self.next_activation_time = int(
                ceil(self.next_activation_time / align) * align
            )

        self.next_activation_time += int(round(offset_secs * NANOS_IN_SEC))
        self._set_jitter()

    def _set_jitter(self):
        self.next_activation_time_with_jitter = self.next_activation_time
        if self.release_jitter:
            self.next_activation_time_with_jitter += int(
                NANOS_IN_SEC * self.release_jitter(self)
            )

    def __iter__(self):
        return self

    def __next__(self):
        # sleep until next activation, possibly ignoring spurious wake-ups
        while not abs_nanosleep(self.next_activation_time_with_jitter):
            pass

        # advance to next period
        self.last_activation_time = self.next_activation_time
        self.next_activation_time += self.period_ns

        # see if there is a sporadic inter-arrival delay
        if self.sporadic_delay:
            self.next_activation_time += int(NANOS_IN_SEC * self.sporadic_delay(self))

        # see if there is release jitter
        self._set_jitter()

        # return last activation time
        return self.last_activation_time / NANOS_IN_SEC


def periodic(period_secs: float, *args, **kargs):
    """Iterator for periodic activations (w.r.t. time.CLOCK_MONOTONIC).

    All parameters specified in seconds (float).

    Example:
    ```
    for t in periodic(1):
        ...
    ```

    Keyword arguments:
    offset_secs     -- Offset of the first activation (default: 0)
    start_time_secs -- Time of the first activation (default: current time + period_secs)
    align_secs      -- Align the start time to a multiple of the given value (default: no alignment)
    release_jitter  -- function called to determine release jitter (default: no jitter)
    sporadic_delay  -- function called to determine sporadic delays between releases (default: no delay)
    """
    return PeriodicActivationsIter(period_secs, *args, **kargs)


class PeriodicActivationsNSIter:
    """Iterator for periodic activations (w.r.t. time.CLOCK_MONOTONIC).

    All parameters specified in nanoseconds (int).
    """

    def __init__(
        self,
        period_nsecs,
        offset_nsecs=0,
        start_time_nsecs=None,
        align_nsecs=None,
        release_jitter=None,
        sporadic_delay=None,
    ):
        self.period_ns = period_nsecs
        self.release_jitter = release_jitter
        self.sporadic_delay = sporadic_delay

        if start_time_nsecs is None:
            self.next_activation_time = time.monotonic_ns() + self.period_ns
        else:
            self.next_activation_time = start_time_nsecs

        if align_nsecs:
            align = align_nsecs
            self.next_activation_time = int(
                ceil(self.next_activation_time / align) * align
            )

        self.next_activation_time += offset_nsecs
        self._set_jitter()

    def _set_jitter(self):
        self.next_activation_time_with_jitter = self.next_activation_time
        if self.release_jitter:
            self.next_activation_time_with_jitter += self.release_jitter(self)

    def __iter__(self):
        return self

    def __next__(self):
        # sleep until next activation, possibly ignoring spurious wake-ups
        while not abs_nanosleep(self.next_activation_time_with_jitter):
            pass

        # advance to next period
        self.last_activation_time = self.next_activation_time
        self.next_activation_time += self.period_ns

        # see if there is a sporadic inter-arrival delay
        if self.sporadic_delay:
            self.next_activation_time += self.sporadic_delay(self)

        # see if there is release jitter
        self._set_jitter()

        # return last activation time
        return self.last_activation_time


def periodic_ns(period_nsecs, *args, **kargs):
    """Iterator for periodic activations (w.r.t. time.CLOCK_MONOTONIC).

    All parameters specified in nanoseconds (int).

    Example:
    ```
    for t in periodic_ns(1000000000):
        ...
    ```

    Keyword arguments:
    offset_nsecs     -- Offset of the first activation (default: 0)
    start_time_nsecs -- Time of the first activation (default: current time + period_nsecs)
    align_nsecs      -- Align the start time to a multiple of the given value (default: no alignment)
    release_jitter   -- function called to determine release jitter (default: no jitter)
    sporadic_delay   -- function called to determine sporadic delays between releases (default: no delay)
    """
    return PeriodicActivationsNSIter(period_nsecs, *args, **kargs)
