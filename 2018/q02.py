import collections
import itertools
import unittest
import util

def reverse_dict(d):
    return {v: k for k, v in d.items()}

def letters_in_common(a, b):
    assert len(a) == len(b)
    common = []
    for i in range(len(a)):
        if a[i] == b[i]:
            common.append(a[i])
    return common


def checksum(words):
    # Checksum = number of ids containing exactly two of any letter
    #          + number with exactly three of any letter
    count_two, count_three = 0, 0
    for word in words:
        counts = reverse_dict(collections.Counter(word))
        if 2 in counts:
            count_two += 1
        if 3 in counts:
            count_three += 1
    return count_two * count_three


def find_correct_box_common_letters(words):
    assert len(words) >= 2
    assert all(len(w) == len(words[0]) for w in words)

    word_length = len(words[0])

    # Find two words which differ by only one character
    for a, b in itertools.combinations(words, 2):
        common = letters_in_common(a, b)
        if len(common) == word_length - 1:
            # All but one letter in common
            return "".join(common)
    return None


class TestQ2(unittest.TestCase):
    def test_basic_part1(self):
        self.assertEqual(checksum([
            'abcdef',
            'bababc',
            'abbcde',
            'abcccd',
            'aabcdd',
            'abcdee',
            'ababab',
        ]), 12)


    def test_part1(self):
        self.assertEqual(checksum(util.read_lines('2018/inputs/q02')), 7808)


    def test_basic_part2(self):
        self.assertEqual(find_correct_box_common_letters([
           "abcde",
           "fghij",
           "klmno",
           "pqrst",
           "fguij",
           "axcye",
           "wvxyz",
        ]), "fgij")

        self.assertEqual(find_correct_box_common_letters([
           "aab",
           "acb",
           "abc",
           "xyz",
        ]), "ab")


    def test_part2(self):
        self.assertEqual(
            find_correct_box_common_letters(util.read_lines("2018/inputs/q02")),
            "efmyhuckqldtwjyvisipargno",
        )
