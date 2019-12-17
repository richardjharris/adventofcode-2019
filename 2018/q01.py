import util
import unittest

def result_frequency(changes):
    freq = 0
    for change in changes:
        freq += int(change)
    return freq


def find_duplicate_frequency(changes):
    freq = 0
    seen = { freq }
    changes = list(changes)
    while True:
        for change in changes:
            freq += int(change)
            if freq in seen:
                return freq
            seen.add(freq)


class TestQ1(unittest.TestCase):
    def test_part1_basic(self):
        self.assertEqual(result_frequency(['+1', '-2', '+3', '+1']), 3)
        self.assertEqual(result_frequency(['+1', '+1', '+1']), 3)
        self.assertEqual(result_frequency(['+1', '+1', '-2']), 0)
        self.assertEqual(result_frequency(['-1', '-2', '-3']), -6)

    def test_part1(self):
        self.assertEqual(result_frequency(util.read_lines('2018/inputs/q01')), 477)

    def test_part2_basic(self):
        self.assertEqual(find_duplicate_frequency(['+1', '-1']), 0)
        self.assertEqual(find_duplicate_frequency(['+3', '+3', '+4', '-2', '-4']), 10)
        self.assertEqual(find_duplicate_frequency(['-6', '+3', '+8', '+5', '-6']), 5)
        self.assertEqual(find_duplicate_frequency(['+7', '+7', '-2', '-7', '-4']), 14)

    def test_part2(self):
        self.assertEqual(find_duplicate_frequency(util.read_lines('2018/inputs/q01')), 390)
