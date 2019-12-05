from enum import Enum, unique
from copy import copy

@unique
class Dir(Enum):
    L = (-1,0)
    R = (1,0)
    U = (0,1)
    D = (0,-1)

def wirePoints(wireString):
    """ return list of tuples where the wire has visited """
    pos = (0,0)
    points = set()
    for part in wireString.split(','):
        direction = Dir[part[0]].value
        distance = int(part[1:])
        for i in xrange(0,distance):
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            points.add(copy(pos))
    return points

def findIntersections(strs):
    """ given multiple strings, find intersections other than (0,0) """
    return set.intersection(*map(wirePoints, strs))

def mDistance(pos):
    """ return Manhattan distance to pt from (0,0) """
    return abs(pos[0]) + abs(pos[1])

def findClosest(pts):
    """ returns closest point by mannhatten distance """
    return min(pts, key=mDistance)

def run(filename):
    """ load wires from file and return information """
    lines = open(filename, 'r').readlines()
    i = findIntersections(lines)
    c = findClosest(i)
    d = mDistance(c)
    print i
    print c
    print d

run("q3_ex0")
run("q3_ex1")
run("q3_ex2")
run("q3_input")
