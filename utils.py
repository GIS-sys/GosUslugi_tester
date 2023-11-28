import datetime
import time

def tryN(foo, N, delay):
    i = 0
    exception = None
    while True:
        try:
            return foo()
        except Exception as e:
            time.sleep(delay)
            i += 1
            if i == N:
                exception = e
                break
    raise exception

def formattedDateTime():
    return datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')

