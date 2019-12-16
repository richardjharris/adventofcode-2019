"Day 1 - The Tyranny of the Rocket Equation"
import math
import unittest
import util
from typing import Callable

def fuel_calc(value: int) -> int:
    """
    fuel calculation used in both solution parts
    """
    return int(math.floor(int(value) / 3) - 2)


def recursive_fuel_calc(value: int) -> int:
    """
    Like fuel_calc, except also consider the fuel required to generate
    mass ALSO requires fuel of its own. Return the total fuel required.
    """
    total = 0
    while True:
        value = fuel_calc(value)
        if value < 0:
            break
        total += value
    return total


def total_fuel(input_file: str, fuel: Callable[[int], int] = fuel_calc) -> int:
    """
    for all modules in input, return the mass required to launch them
    using the specified calculation
    """
    inputs = util.read_lines(input_file)
    return sum(fuel(int(mass)) for mass in inputs)


class TestQ1(unittest.TestCase):
    def test_fuel_calc(self):
        "examples from Part 1"
        self.assertEqual(fuel_calc(12), 2)
        self.assertEqual(fuel_calc(14), 2)
        self.assertEqual(fuel_calc(1969), 654)
        self.assertEqual(fuel_calc(100756), 33583)

    def test_part1(self):
        "Part 1 solution"
        self.assertEqual(total_fuel("inputs/q01"), 3231195)

    def test_recursive_fuel_calc(self):
        "examples from Part 2"
        self.assertEqual(recursive_fuel_calc(14), 2)
        self.assertEqual(recursive_fuel_calc(1969), 966)
        self.assertEqual(recursive_fuel_calc(100756), 50346)

    def test_part2(self):
        "Part 2 solution"
        self.assertEqual(
            total_fuel("inputs/q01", fuel=recursive_fuel_calc),
            4843929)
