import itertools
import util

def output_each(iterable, times=1):
    "Return iterator that outputs each value in iterable n times"
    while True:
        try:
            v = next(iterable)
            for _ in range(times):
                yield v
        except StopIteration:
            break


def apply_fft(i: list, times: int = 1) -> list:
    for _ in range(times):
        o = ""
        for step in range(len(i)):
            pattern = output_each(itertools.cycle([0, 1, 0, -1]), times=(step+1))
            # Skip first element
            next(pattern)

            new_value = sum(int(digit) * next(pattern) for digit in i)
            o += (str(new_value)[-1])
        i = o
    return o

print(apply_fft("12345678"))
print(apply_fft("12345678", times=4))

print(apply_fft(util.slurp("inputs/q16"), times=100)[0:8])
