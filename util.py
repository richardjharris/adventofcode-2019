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
