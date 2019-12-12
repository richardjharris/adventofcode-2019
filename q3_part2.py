from enum import Enum, unique
from copy import copy

@unique
class Dir(Enum):
    L = (-1,0)
    R = (1,0)
    U = (0,1)
    D = (0,-1)

def wirePoints(wireString):
    """ return dict of tuples where the wire has visited, mapping to steps taken """
    pos = (0,0)
    points = dict()
    steps = 0
    for part in wireString.split(','):
        direction = Dir[part[0]].value
        distance = int(part[1:])
        for i in xrange(0,distance):
            steps += 1
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            if pos not in points:
                points[pos] = steps
    return points

def findQuickestIntersection(str1, str2):
    """ find the points existing in both strings, and pick the one with the
    lowest combined steps """
    pts1 = wirePoints(str1)
    pts2 = wirePoints(str2)
    lowestPos = None
    lowestPosSteps = None
    for pos, steps1 in pts1.items():
        if pos in pts2:
            steps2 = pts2[pos]
            if lowestPos is None or lowestPosSteps > steps1 + steps2:
                lowestPos = pos
                lowestPosSteps = steps1 + steps2
    return lowestPos, lowestPosSteps

# 610
print findQuickestIntersection(
    "R75,D30,R83,U83,L12,D49,R71,U7,L72",
    "U62,R66,U55,R34,D71,R55,D58,R83"
)

# 410
print findQuickestIntersection(
    "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
    "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
)

# 107036
lines = open('inputs/q03', 'r').readlines()
print findQuickestIntersection(*lines)
