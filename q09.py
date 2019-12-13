"Day 9 - Sensor Boost"
import unittest
from intcode import IntcodeSim

class TestQ9(unittest.TestCase):
    def test_part1(self):
        i = IntcodeSim.fromFile('inputs/q09')
        # Run in test mode using input 1
        i.queueInput(1).run()
        i.run()
        self.assertEqual(i.outputs, [3345854957])


    def test_part2(self):
        i = IntcodeSim.fromFile('inputs/q09')
        # Run in test mode using input 1
        i.queueInput(2).run()
        i.run()
        self.assertEqual(i.outputs, [68938])
