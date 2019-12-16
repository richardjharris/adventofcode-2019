import itertools
import math
import unittest
import util

def multiplier(col: int, row: int, cycle = [0,1,0,-1]) -> int:
    """
    Returns multiplier (0, -1 or 1) for the value at column N
    for row N. Both column and row are 0-indexed.
    """
    return cycle[ ((col+1) // (row+1)) % 4 ]


def apply_fft(i: list, times: int = 1) -> list:
    # Convert string to list of int
    i = list(map(int, i))

    for time in range(times):
        i = apply_fft_once(i)

    # Convert back to string
    return "".join(map(str, i))


def apply_fft_once(i: list) -> list:
    num_digits = len(i)
    prev_total = None
    o = []

    for row in reversed(range(len(i))):
        if row == num_digits - 1:
            # The last row pattern is all zeroes except the last digit, which is 1.
            total = int(i[-1])
        else:
            """
            At row N, groups are N long. For each group in the row, work out
            where the group used to be, and where the groups no longer overlap,
            subtract the old values and add the new ones.
            """
            group_size = row + 1
            prev_group_size = group_size + 1
            # Only count from column=row, anything before that is 0.
            offset = row
            num_groups = math.ceil((num_digits - row) / group_size)
            prev_offset = row + 1
            total = prev_total

            for group_index in range(num_groups):
                group_start = offset + group_size * group_index
                group_end = offset + group_size * (group_index+1) - 1
                prev_group_start = prev_offset + prev_group_size * group_index
                prev_group_end = prev_offset + prev_group_size * (group_index + 1) - 1

                # We need to recalculate the values for the parts that don't overlap
                # (3 -> 6)  (4 -> 8)   overlap so we cover 3, 7-8
                # (6 -> 12) (7 -> 14)  overlap so we cover 6, 13-14
                # (1 -> 3)  (4 -> 6)   don't overlap so we do 1->6
                # (0 -> 0)  (1 -> 2)   don't overlap so we do 0, 1, 2
                # (7 -> 7)  (15 -> 16) don't overlap so we do 7, 15-16
                # Technically if they perfectly cover (same) we do nothing, but that
                # will never happen
                if group_end < prev_group_start:
                    # Don't overlap, so we just recalc all of it
                    recalc = range(group_start, group_end + 1)
                    prev_recalc = range(prev_group_start, prev_group_end + 1)
                else:
                    # Recalculate up to the overlap
                    recalc = range(group_start, prev_group_start)
                    prev_recalc = range(group_end + 1, prev_group_end + 1)

                for idx in prev_recalc:
                    # Undo the multiplier applied last row
                    # If the group didn't exist in the last row, do nothing
                    if idx > num_digits - 1:
                        continue
                    total -= multiplier(row=row+1, col=idx) * i[idx]

                for idx in recalc:
                    # Might be only part of a group in this row, so skip if needed
                    if idx > num_digits - 1:
                        continue
                    # Apply the multiplier for this row
                    total += multiplier(row=row, col=idx) * i[idx]

        prev_total = total
        # Add last digit of total to output
        o.insert(0, abs(total) % 10)

    return o


def find_message(i: list) -> str:
    """
    Given a list of ints, repeat the list 10,000 times, perform FFT 100 times,
    then locate the eight-digit message found at the location indicated by the
    first eight ints of the input.
    """
    i = list(map(int, i)) * 10000
    N = len(i)
    M = int(''.join(str(char) for char in i[0:7]))

    assert M > len(i) // 2

    # We exploit the fact that the message offset is in the bottom half of
    # the matrix (bottom-right quadrant) which means it only contains 1s and 0s.
    # The bottom half forms a triangle, e.g.:
    # .....
    # .....
    # 00111
    # 00011
    # 00001
    for _ in range(100):
        output = [0] * N
        total = None
        # We only need to calculate from the message offset til the end
        for idx in reversed(range(M, N)):
            if total is None:
                # Bottom row has multiplier=1 from idx onwards, so sum
                total = sum(i[idx:N])
            else:
                # Higher rows can also be summed in the same fashion, but we shortcut
                # by using the previous total + one extra '1' multiplier for the left-
                # most column
                total += i[idx]

            # Record the output (we ignore anything before the message offset)
            output[idx] = abs(total) % 10
        i = output

    return ''.join(str(char) for char in i[M:M+8])

class TestQ16(unittest.TestCase):
    def test_part1_basic(self):
        self.assertEqual(apply_fft("12345678", times=1), "48226158")
        self.assertEqual(apply_fft("12345678", times=2), "34040438")
        self.assertEqual(apply_fft("12345678", times=3), "03415518")
        self.assertEqual(apply_fft("12345678", times=4), "01029498")


    def test_part1_large_example(self):
        self.assertEqual(apply_fft("80871224585914546619083218645595", times=100)[0:8], "24176176")
        self.assertEqual(apply_fft("19617804207202209144916044189917", times=100)[0:8], "73745418")
        self.assertEqual(apply_fft("69317163492948606335995924319873", times=100)[0:8], "52432133")


    def test_part1_puzzle(self):
        answer = apply_fft(util.slurp("inputs/q16"), times=100)[0:8]
        self.assertEqual(answer, "30369587")


    def test_part2_basic(self):
        self.assertEqual(find_message("03036732577212944063491565474664"), "84462026")
        self.assertEqual(find_message("02935109699940807407585447034323"), "78725270")
        self.assertEqual(find_message("03081770884921959731165446850517"), "53553731")


    def test_part2_puzzle(self):
        answer = find_message(util.slurp("inputs/q16"))
        self.assertEqual(answer, "27683551")
