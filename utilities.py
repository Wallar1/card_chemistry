import time


def slow_print(text):
    time.sleep(0)
    print(text)


def get_coefficient(string):
    coefficient = '0'
    start = 0
    chars = list(string)
    for idx, c in enumerate(chars):
        try:
            int(c)
            coefficient += c
        except Exception:
            start = idx
            break
    # do the max of 1 and int(coefficient) because no coefficient is assumed to be 1
    return max(1, int(coefficient)), ''.join(chars[start:])


def measure_performance(func):
    def wrapper(*args, **kwargs):
        start = time.monotonic_ns()
        return_value = func(*args, **kwargs)
        end = time.monotonic_ns()
        print('{} function took {} nanoseconds to run'.format(func.__name__, end - start))
        return return_value
    return wrapper
