from itertools import islice
from collections import defaultdict
import math

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

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a,b):
    return abs(a*b) // gcd(a,b)

def sign(val):
    "return -1 if negative, 0 if 0, or 1 if positive"
    if val < 0:
        return -1
    elif val > 0:
        return 1
    else:
        return 0

def path_find(start, goal, neighbour_func, heuristic_func = lambda x: 0):
    def reconstructPath(cameFrom, current):
        totalPath = [ current ]
        while current in cameFrom:
            current = cameFrom[current]
            totalPath.insert(0, current)
        return totalPath

    # Set of discovered nodes
    openSet = { start }

    # For node n, cameFrom[n] is the node immediately preceding it on the
    # cheapest path from start to n currently known
    cameFrom = {}

    # For node n, gScore[n] is the cost of the cheapest path from start to n
    # currently known
    gScore = defaultdict(lambda: math.inf)
    gScore[start] = 0

    # For node n, fScore[n] = gScore[n] + h(n)
    fScore = defaultdict(lambda: math.inf)
    fScore[start] = heuristic_func(start)

    while len(openSet) > 0:
        current = min(openSet, key=lambda x: fScore[x])
        if current == goal:
            return reconstructPath(cameFrom, current)

        openSet.remove(current)
        for neighbour in neighbour_func(current):
            # weights of the edges are all 0 in this case
            tentative_gScore = gScore[current] + 0
            if tentative_gScore < gScore[neighbour]:
                # This path to the neighbour is better than the previous one
                cameFrom[neighbour] = current
                gScore[neighbour] = tentative_gScore
                fScore[neighbour] = gScore[neighbour] + heuristic_func(neighbour)
                if neighbour not in openSet:
                    openSet.add(neighbour)

    # openset is empty, but goal never reached?
    return None
