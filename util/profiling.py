from time import time
from inspect import getframeinfo, stack
time_series = []


def start():
    time_series.append(time())


def delta():
    caller = getframeinfo(stack()[1][0])
    stop = time()
    dt = stop - time_series[-1]
    time_series.append(stop)
    print('{}:{}\t{}'.format(caller.filename, caller.lineno, dt))


def summary():
    result = sum(b - a for a, b in zip(time_series, time_series[1:]))
    time_series.clear()
    print('Total:\t{}'.format(result))
