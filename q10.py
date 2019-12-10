from util import slurp, manhattanDistance, gcd
import unittest
from copy import copy

def findBestLocation(mapString):
    "check all asteroids and return the one with the most detected asteroids"
    grid = mapString.split('\n')
    height = len(grid)
    width = len(grid[0])
    best = None

    # Find the positions of all asteroids
    asteroids = set()
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '#':
                asteroids.add((x,y))

    # Try each asteroid in arbitrary order
    for src in asteroids:
        detected = 0
        hidden = set()
        # Visit the asteroids surrounding this one, closest-first
        # TODO not sure if manhattan distance is good enough, but it passes tests
        # TODO The intended solution is probably more like: work out the angle
        # and distance for each asteroid relative to src, then count detected++ for
        # each unique angle.
        for dest in sorted(asteroids, key=lambda a: manhattanDistance(src, a)):
            # Is it our own asteroid, or one obscured by an asteroid we already saw?
            if dest is src or dest in hidden:
                continue
            detected += 1
            # Remove any asteroid that would be obscured by this one
            # First find the smallest unit of distance between src and dest that
            # exactly lines up with grid blocks.
            # E.g. for a distance of:            the unit is:
            #       (2,2), (3,3)                 (1,1)
            #       (12,-8), (6,-4)              (3,-2)
            #       (-5,0), (-3,0)               (-1,0)
            unit = (dest[0] - src[0], dest[1] - src[1])
            # gcd is negative if the y value is negative
            g = abs(gcd(*unit))
            unit = (unit[0] // g, unit[1] // g)
            pos = copy(src)
            # Probe from src in the direction of unit, removing any obscured
            # asteroids that we find.
            while pos[0] < width and pos[1] < height \
                and pos[0] >= 0 and pos[1] >= 0:
                if pos in asteroids:
                    hidden.add(copy(pos))
                pos = ( pos[0] + unit[0], pos[1] + unit[1] )

        if best is None or best['detected'] < detected:
            best = { 'detected': detected, 'position': src }

    return best

def destroyAsteroids(mapString):
    """
    destroy asteroids in clockwise order repeatedly. return co-ordinates of asteroids
    in the order they were destroyed
    """
    grid = mapString.split('\n')
    height = len(grid)
    width = len(grid[0])

    """
    we'd need to work out the exact angle between origin and each asteroid. which
    we could have done earlier, I suppose. Then sort the asteroids by angle but only
    destroy the closest one for each unique angle per rotation.
    """

    # Find the positions of all asteroids
    asteroids = set()
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '#':
                asteroids.add((x,y))

    origin = findBestLocation(mapString)
    pass


class TestQ10(unittest.TestCase):
    def clean(self, string):
        "strip trailing and leading spaces from all lines and remove empty lines"
        return "\n".join(line.strip() for line in string.strip().split('\n'))    

    def test_clean(self):
        self.assertEqual(self.clean("""
        aa
        bb
        """), "aa\nbb")

    def test_basic(self):
        "basic test to make sure hiding works in all four directions"
        test = self.clean("""
        ...#...
        .......
        #..#..#
        ...#...
        """)
        self.assertEqual(findBestLocation(test), { 'detected': 4, 'position': (3, 2) })

    def test_example1(self):
        "first example in question spec"
        test = self.clean("""
        .#..#
        .....
        #####
        ....#
        ...##
        """)
        self.assertEqual(findBestLocation(test), { 'detected': 8, 'position': (3, 4) })

    def test_large_example1(self):
        test = self.clean("""
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
        test = self.clean("""
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
        test = self.clean("""
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
        test = self.clean("""
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
