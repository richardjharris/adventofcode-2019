"Day 2 - 1202 Program Alarm"
import intcode
import unittest
import util
from typing import Optional, Tuple

def part1(filename: str) -> int:
    """
    Runs the intcode at filename, patching as directed,
    and returns the value at memory position 0
    """
    i = intcode.IntcodeSim.fromFile(filename)
    # Patch code as directed
    i.arr[1] = 12
    i.arr[2] = 2
    i.run()
    return i.arr[0]

def part2(filename: str, target_output: int) -> Optional[Tuple[int, int]]:
    """
    Determine the values of memory position 0 + 1 which will result in the
    target output.
    """
    code = util.slurp(filename)

    # The solution requires us to return 100 * noun + verb. Therefore it's a
    # good bet that both noun and verb are positive and have a maximum of two
    # digits.
    for noun in range(100):
        for verb in range(100):
            i = intcode.IntcodeSim(code)
            i.arr[1] = noun
            i.arr[2] = verb
            i.run()
            if i.arr[0] == target_output:
                return noun, verb

    return None

class TestQ2(unittest.TestCase):
    """
    Tests for the Q2 solution.
    The examples are already in the intcode.py test suite.
    """
    def test_part1(self):
        value = part1("inputs/q02")
        self.assertEqual(value, 2782414)

    def test_part2(self):
        noun, verb = part2("inputs/q02", 19690720)
        self.assertEqual(noun, 98)
        self.assertEqual(verb, 20)
