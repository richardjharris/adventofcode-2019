import numpy as np
import re
import unittest
import util

def compute_claims(lines):
    canvas = np.zeros((1000, 1000))
    for line in lines:
        m = re.fullmatch(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
        assert m
        _, left, top, width, height = map(int, m.groups())
        claim = np.ones((height, width))

        canvas[top:top+height, left:left+width] += claim

    claims = sum(1 for v in np.nditer(canvas) if v >= 2)
    return claims


class TestQ3(unittest.TestCase):
    def test_part1_basic(self):
        self.assertEqual(compute_claims([
            "#1 @ 1,3: 4x4",
            "#2 @ 3,1: 4x4",
            "#3 @ 5,5: 2x2",
        ]), 4)


    def test_part1(self):
        claims = util.read_lines('2018/inputs/q03')
        self.assertEqual(compute_claims(claims), 98005)
