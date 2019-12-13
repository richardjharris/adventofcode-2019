"Day 3 - Crossed Wires"
import enum
import unittest
from typing import Iterable, Tuple, Dict, Optional, List
from util import read_lines

Point = Tuple[int, int]

@enum.unique
class Dir(enum.Enum):
    "enum to map wire movement direction names to vectors"
    L = (-1, 0)
    R = (1, 0)
    U = (0, 1)
    D = (0, -1)


def find_intersections(wires: List[Dict[Point, int]]):
    """
    Given a list of wires (dicts of point -> steps taken)
    Return the points present in all wires, i.e. the intersections
    """
    if not wires:
        return set()

    intersections = wires[0].keys()
    for wire in wires[1:]:
        intersections &= wire.keys()

    return intersections


def wire_points(wire_string: str) -> Dict[Point, int]:
    """
    Given a wire string such as 'D3,R1,U2...' return a dict mapping
    each point the wire covers, with the minimum steps taken before
    the wire reaches that point.
    """
    pos = (0, 0)
    points: Dict[Point, int] = dict()
    steps = 0
    for part in wire_string.split(','):
        direction = Dir[part[0]].value
        distance = int(part[1:])
        for _ in range(distance):
            steps += 1
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            if pos not in points:
                points[pos] = steps

    return points


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
    wires = list(map(wire_points, wire_strings))
    crosses = find_intersections(wires)
    return manhattan_dist_from_origin(find_closest(crosses))


def part2(wire_strings: Iterable[str]) -> Optional[int]:
    """
    Given a list of wire strings, return the minimum combined number
    of steps along each strings' paths before an intersection is
    reached.
    """
    wires = list(map(wire_points, wire_strings))
    lowest = None

    for crossing in find_intersections(wires):
        steps = sum(wire[crossing] for wire in wires)
        if lowest is None or steps < lowest:
            lowest = steps

    return lowest

class TestQ3(unittest.TestCase):
    def test_part1_basic(self):
        wires = [
            "R8,U5,L5,D3",
            "U7,R6,D4,L4",
        ]
        self.assertEqual(part1(wires), 6)


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


    def test_part2_example1(self):
        wires = [
            "R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "U62,R66,U55,R34,D71,R55,D58,R83",
        ]
        self.assertEqual(part2(wires), 610)


    def test_part2_example2(self):
        wires = [
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
        ]
        self.assertEqual(part2(wires), 410)


    def test_part2(self):
        wires = read_lines("inputs/q03")
        self.assertEqual(part2(wires), 107036)
