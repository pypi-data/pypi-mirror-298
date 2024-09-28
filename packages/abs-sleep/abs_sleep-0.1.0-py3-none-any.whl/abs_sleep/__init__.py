from ctypes import CDLL, Structure, c_long, byref
from math import ceil
import time
import os

NANOS_IN_SEC = int(1e9)

HAVE_LIBC_ABSTIME = False

# try to import libc on Linux
try:
    if os.uname().sysname  == "Linux":
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
        "Sleep until the absolute given time (in ns), w.r.t. the given clock (Linux only)."
        ts = TimeSpec.from_nanoseconds(nsecs)
        # https://man7.org/linux/man-pages/man2/clock_nanosleep.2.html
        err = libc.clock_nanosleep(clock, TIMER_ABSTIME, byref(ts), None)
        return err == 0

    def abs_sleep(secs: float, clock: int = time.CLOCK_MONOTONIC) -> bool:
        "Sleep until the absolute given time (in seconds), w.r.t. the given clock (Linux only)."
        ts = TimeSpec.from_seconds(secs)
        # https://man7.org/linux/man-pages/man2/clock_nanosleep.2.html
        err = libc.clock_nanosleep(clock, TIMER_ABSTIME, byref(ts), None)
        return err == 0

else:
    # We don't have clock_nanosleep available, so approximate loosely.

    def abs_sleep(secs: float, clock: int = 0) -> bool:
        "An inexact approximation of an absolutely timed sleep (given in seconds)."
        # This of course doesn't always work, but as of 3.12 there
        # doesn't appear to be an absolutely timed sleep in the Python
        # standard library.
        time.sleep(max(0, secs - time.monotonic()))
        return True

    def abs_nanosleep(nsecs: int, clock: int = 0) -> bool:
        "An inexact approximation of an absolutely timed sleep (given in ns)."
        return abs_sleep(nsecs / NANOS_IN_SEC)
