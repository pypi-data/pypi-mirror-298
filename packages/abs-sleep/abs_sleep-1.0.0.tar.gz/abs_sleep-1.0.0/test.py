from abs_sleep import abs_sleep, abs_nanosleep, periodic, periodic_ns
import time

t = time.monotonic()
print('One sec...', end='', flush=True)
abs_sleep(t + 1)
print('done.')

t = time.monotonic_ns()
print('Half a sec...', end='', flush=True)
abs_nanosleep(t + 500000000)
print('done.')


for i, t in enumerate(periodic(0.2, align_secs=2)):
    print(t)
    if i >= 4:
        break


for i, t in enumerate(periodic_ns(500000000, align_nsecs=1000000000)):
    print(t)
    if i >= 4:
        break



for i, t in enumerate(periodic(0.2, align_secs=2, release_jitter=lambda it: 0.123)):
    print(t, time.monotonic())
    if i >= 4:
        break



for i, t in enumerate(periodic_ns(100000000, align_nsecs=2000000000, sporadic_delay=lambda it: 1000)):
    print(t, time.monotonic_ns())
    if i >= 4:
        break
