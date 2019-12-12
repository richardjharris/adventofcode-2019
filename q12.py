import functools
import itertools
import operator
import util

example1 = [
    [-1,0,2],
    [2,-10,-7],
    [4,-8,8],
    [3,5,-1],
]

example2 = [
    [-8,-10,0],
    [5,5,10],
    [2,-7,3],
    [9,-8,-3],
]

q12Input = [
    [-8,-9,-7],
    [-5,2,-1],
    [11,8,-14],
    [1,-4,-11],
]

def runStep(bodies):
    for axis in range(3):
        runAxisStep(bodies, axis)

def runAxisStep(bodies, axis):
    pairs = itertools.combinations(bodies, 2)
    # Apply gravity
    for (a,b) in pairs:
        # Adjustment for first planet.
        if a["pos"][axis] < b["pos"][axis]:
            adj = 1
        elif a["pos"][axis] == b["pos"][axis]:
            adj = 0
        else:
            adj = -1

        a["vel"][axis] += adj
        b["vel"][axis] -= adj
    # Apply velocity
    for body in bodies:
        body["pos"][axis] += body["vel"][axis]


def totalEnergy(bodies):
    "return total energy of system of bodies"
    def sumAbs(point):
        return sum(map(abs, point))

    energy = 0
    for body in bodies:
        energy += (sumAbs(body['pos']) * sumAbs(body['vel']))
    return energy


def part1():
    bodies = list(map(lambda pos: {"pos": pos, "vel": [0,0,0]}, q12Input))
    for _ in range(1000):
        runStep(bodies)
    print(totalEnergy(bodies))

def part2_naive(startPositions):
    """
    Naive method to find the number of steps taken to reach a previous state
    This is too slow for the q12 input.
    """

    # Mapping of previous states seen
    prevStates = set()

    def state(bodies):
        "generate state hash from bodies"
        return repr(bodies)

    bodies = list(map(lambda pos: {"pos": pos, "vel": [0,0,0]}, startPositions))

    # Run the simulation until we reach any previous known state
    step = 0
    while state(bodies) not in prevStates:
        prevStates.add(state(bodies))
        runStep(bodies)
        step += 1
    return step

def part2(startPositions):
    # For each axis, run the simulation until we find the number of steps
    # required to cycle for that axis.
    bodies = list(map(lambda pos: {"pos": pos, "vel": [0,0,0]}, startPositions))

    cycles = []
    for axis in range(3):
        # We keep track of the step of each previous state seen. In practice,
        # we don't need to do this, because the state always returns to its
        # initial state (step=0) before any other state.
        prevStates = {}
        def state(bodies):
            return repr(bodies)

        step = 0
        while state(bodies) not in prevStates:
            prevStates[state(bodies)] = step
            runAxisStep(bodies, axis)
            step += 1

        cycles.append((prevStates[state(bodies)], step))

    # If all cycles start at zero, it's pretty easy to figure out at what
    # step they will align: we take the lowest common multiple of each axis'
    # cycle length.
    for cycle in cycles:
        if cycle[0] != 0:
            raise f"don't know how to handle {cycle}";

    return functools.reduce(util.lcm, (c[1] for c in cycles))


print(part2(q12Input))
