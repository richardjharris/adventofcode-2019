import itertools

q12Input = [
    [-8,-9,-7],
    [-5,2,-1],
    [11,8,-14],
    [1,-4,-11],
]

def runStep(bodies):
    pairs = itertools.combinations(bodies, 2)
    # Apply gravity
    for (a,b) in pairs:
        for axis in range(3):
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
        for axis in range(3):
            body["pos"][axis] += body["vel"][axis]


def printB(bodies):
    "debug function to print body status"
    def printPos(pos):
        return f"x={pos[0]} y={pos[1]} z={pos[2]}"

    for body in bodies:
        print(f"pos=<{printPos(body['pos'])}> vel=<{printPos(body['vel'])}>")
    print("----")


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


part1()
