from collections import defaultdict
from decimal import Decimal
from util import slurp
import math
import unittest

def clean(string):
    "strip trailing and leading spaces from all lines and remove empty lines"
    return "\n".join(line.strip() for line in string.strip().split('\n'))    

def findAsteroids(mapString):
    """
    return a set of tuples representing the co-ordinates of all asteroids
    in the map.
    """
    grid = mapString.split('\n')
    height = len(grid)
    width = len(grid[0])

    asteroids = set()
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '#':
                asteroids.add((x,y))

    return asteroids

def findBestLocation(mapString):
    """
    find the location of the asteroid that can detect the most other asteroids
    in its line of sight. also returns the number detected.
    """

    asteroids = findAsteroids(mapString)
    best = None

    # Compute the angle and distance of each asteroid relative to the origin
    for src in asteroids:
        seen = set()
        for dest in asteroids:
            if dest is src:
                continue
            vector = (dest[0] - src[0], dest[1] - src[1])
            angle = clockwiseAngle(vector)
            seen.add(angle)

        detected = len(seen)

        if best is None or best['detected'] < detected:
            best = { 'detected': detected, 'position': src }

    return best

def destroyAsteroids(mapString):
    """
    destroy asteroids in clockwise order repeatedly. return co-ordinates of asteroids
    in the order they were destroyed
    """

    # Find the positions of all asteroids
    asteroids = findAsteroids(mapString)

    # Get the position of our monitoring station
    origin = findBestLocation(mapString)['position']
    asteroids.remove(origin)

    # Compute the angle and distance of each asteroid relative to the origin
    byAngle = defaultdict(list)
    for asteroid in asteroids:
        vector = (asteroid[0] - origin[0], asteroid[1] - origin[1])
        distance = vectorLength(vector)
        angle = clockwiseAngle(vector)

        byAngle[angle].append((asteroid, distance))

    # Start the death ray
    destroyed = []
    while asteroids:
        for angle in sorted(byAngle):
            # Destroy the asteroid with the smallest distance for each given angle
            if byAngle[angle]:
                closest = min(byAngle[angle], key=lambda x: x[1])
                byAngle[angle].remove(closest)
                asteroids.remove(closest[0])
                destroyed.append(closest[0])

    return destroyed

def vectorLength(u):
    return math.sqrt(u[0]*u[0] + u[1]*u[1])

def vectorDotProduct(u, v):
    return u[0] * v[0] + u[1] * v[1]

def clockwiseAngle(v, precision=10):
    """
    return clockwise angle for vector: the angle from vector (0,-1)
    pointing straight up {well, down in Cartesian} to the vector

    E.g. for a vector (0,-1) the angle is 0
         for a vector (1,-1) the angle is 45 (going up-right)
         for a vector (0, 1) the angle is 180 (going down)
         for a vector (-1,-1) the angle is 315 (going up-left)

    The angle is truncated to precision decimal places (default 10)
    to allow equality comparison.

    """
    u = (0, -1)
    cosAngle = vectorDotProduct(u, v) / (vectorLength(u) * vectorLength(v))
    angle = math.acos(cosAngle)

    # We know u is pointing up. If v is negative (left side of the clock)
    # convert the angle from counter-clockwise to clockwise
    if v[0] < 0:
        angle = 2*math.pi - angle

    # Turn into degrees for ease of debugging
    angle = math.degrees(angle)

    # We need to normalise the angle as floating point errors can prevent
    # equality of angles that are actually the same. For example:
    # angle=14.036243467926457 contents=[((14, 1), 12.36931687685298)]
    # angle=14.036243467926484 contents=[((13, 5), 8.246211251235321)]
    # Use Decimal to allow the angles to be stored and compared without further
    # floating point errors (although float passes the tests)
    angle = Decimal(f'{angle:.{precision}f}')

    return angle

class TestQ10(unittest.TestCase):
    def test_vector(self):
        self.assertEqual(vectorLength((math.sqrt(2),math.sqrt(2))), 2.0)
        self.assertEqual(vectorLength((0,3)), 3.0)
        self.assertEqual(vectorLength((0,-3)), 3.0)

        self.assertEqual(vectorDotProduct((2,2), (0,3)), 6)

    def test_clean(self):
        self.assertEqual(clean("""
        aa
        bb
        """), "aa\nbb")

    def test_basic(self):
        "basic test to make sure hiding works in all four directions"
        test = clean("""
        ...#...
        .......
        #..#..#
        ...#...
        """)
        self.assertEqual(findBestLocation(test), { 'detected': 4, 'position': (3, 2) })

    def test_example1(self):
        "first example in question spec"
        test = clean("""
        .#..#
        .....
        #####
        ....#
        ...##
        """)
        self.assertEqual(findBestLocation(test), { 'detected': 8, 'position': (3, 4) })

    def test_large_example1(self):
        test = clean("""
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
        """)
        self.assertEqual(findBestLocation(test), { 'detected': 33, 'position': (5, 8) })

    def test_large_example2(self):
        test = clean("""
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
        """)
        self.assertEqual(findBestLocation(test), { 'detected': 35, 'position': (1, 2) })

    def test_large_example3(self):
        test = clean("""
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
        """)
        self.assertEqual(findBestLocation(test), { 'detected': 41, 'position': (6, 3) })

    def test_large_example4(self):
        test = clean("""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
        """)
        self.assertEqual(findBestLocation(test), { 'detected': 210, 'position': (11, 13) })

    def test_part1(self):
        test = slurp('q10_input')
        self.assertEqual(findBestLocation(test), { 'detected': 269, 'position': (13, 17) })

    def test_destroy_basic(self):
        test = clean("""
            .#..
            ####
            .#..
        """)
        self.assertEqual(findBestLocation(test), { 'detected': 4, 'position': (1,2) })
        self.assertEqual(destroyAsteroids(test), [
            (1,1), (2,1), (3,1), (0,1), (1,0)
        ])
    
    def test_destroy_example1(self):
        test = clean("""
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##
""")
        destroyed = destroyAsteroids(test)
        self.assertEqual(destroyed[0:9], [
            (8,1), (9,0), (9,1), (10,0), (9,2), (11,1), (12,1), (11,2), (15,1)
        ])
        self.assertEqual(destroyed[9:18], [
            (12,2), (13,2), (14,2), (15,2), (12,3), (16,4), (15,4), (10,4), (4,4)
        ])
        self.assertEqual(destroyed[18:27], [
            (2,4), (2,3), (0,2), (1,2), (0,1), (1,1), (5,2), (1,0), (5,1)
        ])

    def test_destroy_example2(self):
        test = clean("""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
        """)
        destroyed = destroyAsteroids(test)
        self.assertEqual(destroyed[0], (11,12))
        self.assertEqual(destroyed[1], (12,1))
        self.assertEqual(destroyed[2], (12,2))
        self.assertEqual(destroyed[9], (12,8))
        self.assertEqual(destroyed[19], (16,0))
        self.assertEqual(destroyed[49], (16,9))
        self.assertEqual(destroyed[99], (10,16))
        self.assertEqual(destroyed[198], (9,6))
        self.assertEqual(destroyed[199], (8,2))
        self.assertEqual(destroyed[200], (10,9))
        self.assertEqual(destroyed[298], (11,1))
        self.assertEqual(len(destroyed), 299)

    def test_part2(self):
        test = slurp('q10_input')
        destroyed = destroyAsteroids(test)
        number200 = destroyed[199]
        self.assertEqual(number200, (6, 12))

