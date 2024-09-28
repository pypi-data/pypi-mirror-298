# abs-sleep: Absolutely Timed Sleeps in Python

The `abs-sleep` package for Python 3 provides a thin wrapper around the [`ctypes` module](https://docs.python.org/3/library/ctypes.html) for calling [`clock_nanosleep`](https://man.archlinux.org/man/clock_nanosleep.2.en) **on Linux** with the `TIMER_ABSTIME` flag set. This allows for precisely timed sleeps that are not affected by timer drift (e.g., due to preemptions). 

The two primary provided functions are:

- `abs_sleep(wakeup_time, clock=time.CLOCK_MONOTONIC)`  
   Sleep until the absolute time `wakeup_time` (specified in seconds) is reached w.r.t. the specified clock (`time.CLOCK_MONOTONIC` by default).
- `abs_nanosleep(wakeup_time_ns, clock=time.CLOCK_MONOTONIC)`  
  Sleep until the absolute time `wakeup_time` (specified in integral nanoseconds) is reached w.r.t. the specified clock (`time.CLOCK_MONOTONIC` by default).

They are intended to be used together with [`time.monotonic()`](https://docs.python.org/3/library/time.html#time.monotonic)   and [`time.monotonic_ns()`](https://docs.python.org/3/library/time.html#time.monotonic_ns), respectively.

On POSIX platforms other than Linux, the library resorts to an inaccurate approximation. 

Tested on Linux and macOS.

## Example: Absolutely Timed Sleeps

```python
from abs_sleep import abs_sleep, abs_nanosleep
import time

t = time.monotonic()
print('One sec...', end='', flush=True)
abs_sleep(t + 1)
print('done.')

t = time.monotonic_ns()
print('Five secs...', end='', flush=True)
abs_nanosleep(t + 5000000000)
print('done.')
```

## Periodic Activations Iterators

Additionally, there are two convenience iterators that help with implementing **periodic activations** (w.r.t. `time.CLOCK_MONOTONIC`):

- `periodic(period_secs)`
- `periodic_ns(period_nsecs)`

These two iterators take a number of optional keyword arguments.

| `periodic` argument | `periodic_ns` argument | effect                                                       | default               |
| ------------------- | ---------------------- | ------------------------------------------------------------ | --------------------- |
| `offset_secs`       | `offset_nsecs`         | offset of the first activation                               | 0                     |
| `start_time_secs`   | `start_time_nsecs`     | time of the first activation                                 | current time + period |
| `align_secs`        | `align_nsecs`          | round up the start time to a multiple of the given alignment granularity | no alignment          |
| `release_jitter`    | `release_jitter`       | callback function to determine release jitter (see below)    | no jitter             |
| `sporadic_delay`    | `sporadic_delay`       | callback function to determine sporadic inter-arrival delay (see below) | no delay              |

The `release_jitter` argument accepts a function `iterator_state -> release jitter value` that, given the current iterator state object, produces a *release jitter* value for the next release  (e.g., `lambda _it: 123`). The time scale must match that of the iterator (i.e., seconds in case of `periodic` and integral nanoseconds in case of `periodic_ns`).

The `sporadic_delay` argument accepts a function `iterator_state -> sporadic delay value` that, given the current iterator state object, produces a *sporadic inter-arrival delay* value for the next release  (e.g., `lambda _it: 123`). The time scale must match that of the iterator (i.e., seconds in case of `periodic` and integral nanoseconds in case of `periodic_ns`).

The difference between release jitter and sporadic inter-arrival delays is that release jitter affects only the next activation, whereas sporadic inter-arrival delay is cumulative (i.e., a delay > 0 implicitly delays all future activations, too).

The first three arguments (offset, start time, alignment) are useful for implementing periodic real-time tasks. The latter two arguments (release jitter and sporadic delay) are useful for _simulating_ periodic and sporadic real-time task behavior.  

## Example: Periodic Activations

```python
from abs_sleep import periodic, periodic_ns
import time

# periodic activations with a period of 200 milliseconds
for i, t in enumerate(periodic(0.2)):
    print(t)
    if i >= 4:
        break

# periodic activations with a period of 500 milliseconds, aligned to integral seconds
for i, t in enumerate(periodic(0.5, align_secs=1)):
    print(t)
    if i >= 4:
        break

# periodic activations with a period of 500 milliseconds, aligned to integral seconds
for i, t in enumerate(periodic_ns(500000000, align_nsecs=1000000000)):
    print(t)
    if i >= 4:
        break        
        
# periodic activations with a period of 200 milliseconds,
# first release aligned to an integer multiple of 2 seconds,
# and a fixed amount of release jitter (123 ms)
for i, t in enumerate(periodic(0.2, align_secs=2, release_jitter=lambda _it: 0.123)):
    print(t, time.monotonic())
    if i >= 4:
        break

# sporadic activations with a sporadic inter-arrival delay of 1000ns
for i, t in enumerate(periodic_ns(100000000, align_nsecs=2000000000, sporadic_delay=lambda it: 1000)):
    print(t, time.monotonic_ns())
    if i >= 4:
        break

```

