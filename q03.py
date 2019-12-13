"Day 3 - Crossed Wires"
import copy
import enum
import unittest
from typing import Iterable, Set, Tuple
from util import read_lines

Point = Tuple[int, int]

@enum.unique
class Dir(enum.Enum):
    "enum to map wire movement direction names to vectors"
    L = (-1, 0)
    R = (1, 0)
    U = (0, 1)
    D = (0, -1)

def wire_points(wire_string: str) -> Set[Point]:
    """
    given a wire string such as 'D3,R1,U2...' return a set of tuples
    marking points the wire covers.
    """
    pos = (0, 0)
    points = set()
    for part in wire_string.split(','):
        direction = Dir[part[0]].value
        distance = int(part[1:])
        for _ in range(distance):
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            points.add(copy.copy(pos))

    return points


def find_intersections(strings: Iterable[str]) -> Set[Point]:
    """
    given multiple strings, return the points that occur in all
    strings
    """
    return set.intersection(*map(wire_points, strings))


def manhattan_dist_from_origin(pos: Point) -> int:
    "return Manhattan distance to pos from (0,0)"
    return abs(pos[0]) + abs(pos[1])


def find_closest(points: Iterable[Point]) -> Point:
    "returns closest point by Manhatten distance"
    return min(points, key=manhattan_dist_from_origin)


def part1(wire_strings: Iterable[str]) -> int:
    """
    Given a list of wire strings, return the Manhattan distance from
    the origin to the closest intersection of all strings.
    """
    crosses = find_intersections(wire_strings)
    return manhattan_dist_from_origin(find_closest(crosses))


class TestQ3(unittest.TestCase):
    def test_part1_example1(self):
        wires = [
            "R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "U62,R66,U55,R34,D71,R55,D58,R83",
        ]
        self.assertEqual(part1(wires), 159)

    def test_part1_example2(self):
        wires = [
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
        ]
        self.assertEqual(part1(wires), 135)

    def test_part1(self):
        wires = read_lines("inputs/q03")
        self.assertEqual(part1(wires), 1225)
