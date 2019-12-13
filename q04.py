"Day 4 - Secure Container"
import unittest

def matches_criteria(number: int) -> int:
    """
    given a six digit number, returns true if it matches the criteria:
     - two adjacent digits are the same
     - going from left to right, the digits never decrease
    """
    twoAdjacent = False
    prevDigit = None
    for digit in str(number):
        if prevDigit is None:
            pass
        else:
            if int(prevDigit) > int(digit):
                return False
            elif int(prevDigit) == int(digit):
                twoAdjacent = True
        prevDigit = digit

    if not twoAdjacent:
        return False

    return True


def matches_criteria_two(number: int) -> int:
    """
    as matchesCriteria, except requires the two adjacent matching digits
    to NOT be a part of a larger group of matching digits
    """
    currentChainLength = 0
    twoAdjacentFound = False
    prevDigit = None
    for digit in str(number):
        if prevDigit is None:
            pass
        else:
            if int(prevDigit) > int(digit):
                return False
            elif int(prevDigit) == int(digit):
                currentChainLength += 1
            else:
                if currentChainLength == 1:
                    twoAdjacentFound = True
                currentChainLength = 0
        prevDigit = digit

    if currentChainLength == 1:
        twoAdjacentFound = True

    if not twoAdjacentFound:
        return False

    return True


class TestQ4(unittest.TestCase):
    def test_matches1(self):
        self.assertEqual(matches_criteria(111111), True)
        self.assertEqual(matches_criteria(111123), True)
        self.assertEqual(matches_criteria(122345), True)
        self.assertEqual(matches_criteria(223450), False, 'decreasing pair')
        self.assertEqual(matches_criteria(123789), False, 'no double')


    def test_matches2(self):
        self.assertEqual(matches_criteria_two(112233), True)
        self.assertEqual(matches_criteria_two(123444), False, 'triplet')
        self.assertEqual(matches_criteria_two(111122), True, 'four 1s, but also double')


    input_range = range(145852, 616942 + 1)

    def test_part1(self):
        # The input range are all 6-digit numbers, so no need to test that.
        matched = sum(1 for i in self.input_range if matches_criteria(i))
        self.assertEqual(matched, 1767)


    def test_part2(self):
        matched = sum(1 for i in self.input_range if matches_criteria_two(i))
        self.assertEqual(matched, 1192)
