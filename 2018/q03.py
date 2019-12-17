import numpy as np
import re
import unittest
import util

def parse_claims(lines):
    """
    Generator that accepts lines and returns MatchObjects with info
    for each claim.
    """
    for line in lines:
        m = re.fullmatch(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
        assert m
        yield tuple(map(int, m.groups()))


def compute_claims(lines):
    """
    Process incoming claim lines and return the number of square inches
    of fabric that are within two or more claims.
    """
    canvas = np.zeros((1000, 1000))
    for claim in parse_claims(lines):
        _, left, top, width, height = claim
        ones = np.ones((height, width))
        canvas[top:top+height, left:left+width] += ones

    num_contested = sum(1 for v in np.nditer(canvas) if v >= 2)
    return num_contested


def find_virgin_claim(lines):
    """
    Process incoming claim lines and return the claim ID which doesn't
    overlap with any other.
    """
    canvas = np.zeros((1000, 1000))
    claims = list(parse_claims(lines))

    for claim in claims:
        _, left, top, width, height = claim
        ones = np.ones((height, width))
        canvas[top:top+height, left:left+width] += ones
    
    def unclaimed(canvas, claim):
        _, left, top, width, height = claim
        for y in range(top, top + height):
            for x in range(left, left + width):
                if canvas[y,x] > 1:
                    return False
        return True

    for claim in claims:
        if unclaimed(canvas, claim):
            return claim[0]

    return None


class TestQ3(unittest.TestCase):
    example = [
        "#1 @ 1,3: 4x4",
        "#2 @ 3,1: 4x4",
        "#3 @ 5,5: 2x2",
    ]

    def test_part1_basic(self):
        self.assertEqual(compute_claims(self.example), 4)


    def test_part1(self):
        claims = util.read_lines('2018/inputs/q03')
        self.assertEqual(compute_claims(claims), 98005)


    def test_part2_basic(self):
        self.assertEqual(find_virgin_claim(self.example), 3)

        
    def test_part2(self):
        claims = util.read_lines('2018/inputs/q03')
        self.assertEqual(find_virgin_claim(claims), 331)
