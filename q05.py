"Day 5 - Sunny with a Chance of Asteroids"
import unittest
from intcode import IntcodeSim

class TestQ5(unittest.TestCase):
    """
    All examples from Q5 are already in the intcode test suite, so just
    calculate the problem solutions.
    """
    def test_part1(self):
        i = IntcodeSim.fromFile("inputs/q05")
        i.queueInput(1).run()

        self.assertEqual(
            i.outputs[-1],
            7692125,
            'correct diagnostic code')

        self.assertTrue(
            all(x == 0 for x in i.outputs[1:-2]),
            'all other outputs are 0')


    def test_part2(self):
        i = IntcodeSim.fromFile('inputs/q05')
        i.queueInput(5).run()
        self.assertEqual(i.outputs, [14340395])
