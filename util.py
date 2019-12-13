from itertools import islice

def split_every(n, iterable):
    "split iterable into pieces of size n. lazy"
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

def slurp(filename):
    "read contents of filename into a string and return"
    with open(filename, 'r') as fh:
        return fh.read().rstrip('\n')

def read_lines(filename):
    "read contents of filename as a list of lines"
    with open(filename, 'r') as fh:
        return fh.readlines()

def manhattanDistance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a,b):
    return abs(a*b) // gcd(a,b)
