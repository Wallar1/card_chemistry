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


def least_common_multiple(num_arr):
    # lazy method is just return the multiple of all of the numbers, which is not an LCM, but it works the same
    return reduce(lambda serialized, num: serialized * num, num_arr, 1)

    # lcm = 1
    # # make sure they are all not 1, because if so, the lcm is just 1
    # if max(num_arr) == 1:
    #     return 1

    # def all_nums_are_factors(num_arr):
    #     for num in num_arr:
    #         if lcm % num != 0:
    #             return False
    #     return True

    # # some random upper bound so we dont run to infinity if this code is wrong
    # while lcm < 1000:
    #     lcm += 1
    #     if all_nums_are_factors(num_arr):
    #         return lcm
    # raise Exception("Least common multiple was not found")


# def find_random_compound(self, elements, compounds):
#     element_counts = {}
#     for element in elements:
#         element_counts[]
#     possible_compounds = []
#     for compound in compounds:
#         pass