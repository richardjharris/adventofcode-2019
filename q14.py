'Day 14 - Space Stoichiometry'
import collections
import copy
import dataclasses
import math
import unittest
import util
from typing import List

@dataclasses.dataclass
class Quantity():
    amount: int
    chemical: str

    def __mul__(self, number):
        if not isinstance(number, int):
            raise ValueError("must multiply Quantity by an int")
        return Quantity(self.amount * number, self.chemical)

    @classmethod
    def parse(cls, string):
        amount, chemical = string.split(' ')
        return cls(int(amount), chemical)


@dataclasses.dataclass
class Formula():
    requires: List[Quantity]
    produces: Quantity


class Stock(collections.defaultdict):
    def __init__(self, *args, **kwargs):
        super(Stock, self).__init__(*args, **kwargs)
        self.default_factory = int

    def __repr__(self):
        return "Stock(" + ", ".join(f"{key} {self[key]}" for key in self.keys()) + ")"


def parse_formulas(strings):
    """
    Given formula strings, return dict mapping each chemical to
    a tuple of (int produced, [Quantity] required)
    """
    formulae = {}
    for string in strings:
        left, right = string.rstrip('\n').split(' => ')

        requires = [Quantity.parse(req) for req in left.split(', ')]
        produces = Quantity.parse(right)

        if produces.chemical in formulae:
            raise Exception(f"two formulas for the same chemical {produces.chemical}")

        formulae[produces.chemical] = Formula(produces=produces, requires=requires)

    return formulae
    

def ore_needed(strings, target_fuel=1):
    """
    Given formula strings such as '10 ORE => 10 A', '1 A => 1 FUEL'
    Returns the amount of ORE required to generate target units of FUEL

    This is done by representing the stock as a balance sheet and applying
    formulas to make negative numbers into positive ones. We multiply the
    formula to do it as much as possible, then correct any surplus afterwards,
    until we cannot perform any more formulas.
    """
    f = parse_formulas(strings)

    # Track how much we have of each chemical
    stock = Stock()

    # Represent fuel as a deficit, which we need to balance
    stock["FUEL"] = -target_fuel

    # Try to balance each chemical in turn by applying the formula
    # (the key is, we also have negative stock, which we resolve by applying
    # the formula with negative values)
    # Don't balance ORE: allow it to become negative, and its value will
    # be the total ORE used.
    while True:
        balanced = True
        for chemical in stock:
            if chemical == "ORE" or stock[chemical] >= 0:
                continue
            formula = f[chemical]
            times = (-stock[chemical] + formula.produces.amount - 1) \
                    // formula.produces.amount
            stock[chemical] += times * formula.produces.amount
            for item in formula.requires:
                stock[item.chemical] -= times * item.amount
            balanced = False
            # Restart to avoid 'dictionary changed size during iteration'
            break

        if balanced:
            # We didn't make any changes this iteration, so we're done
            break

    return -stock['ORE']


def max_fuel(strings, ore_limit=1000000000000):
    """
    Given formula strings and an ore limit, return the maximum amount of FUEL
    that can be produced before running out of ore.

    Since our ore_needed code accepts a target_fuel parameter, this can
    be done via binary search.
    """
    low, high, ore = 1, 1, 0
    # Try factors of 10 until we exceed the limit, to reduce the search space
    while ore <= ore_limit:
        low, high = high, high * 10
        ore = ore_needed(strings, high)
    
    # Binary search within this range to find the actual maximum
    mid = 0
    while high - low > 1:
        mid = (high + low) // 2
        ore = ore_needed(strings, mid)

        if ore > ore_limit:
            high = mid
        else:
            low = mid

    return low


class TestQ14(unittest.TestCase):
    def test_basic(self):
        strs = ['1 ORE => 2 A', '6 A => 1 FUEL']
        self.assertEqual(ore_needed(strs), 3, '3 ORE -> 6 A -> 1 FUEL')
        self.assertEqual(max_fuel(strs, ore_limit=10), 3)
        self.assertEqual(max_fuel(strs, ore_limit=20), 6)

        strs = ['10 ORE => 10 A', '5 A => 1 FUEL']
        self.assertEqual(ore_needed(strs), 10, 'cannot run partial formula')


    def test_example1(self):
        strs = [
            '10 ORE => 10 A',
            '1 ORE => 1 B',
            '7 A, 1 B => 1 C',
            '7 A, 1 C => 1 D',
            '7 A, 1 D => 1 E',
            '7 A, 1 E => 1 FUEL',
        ]
        self.assertEqual(ore_needed(strs), 31)


    def test_example2(self):
        strs = [
            '9 ORE => 2 A',
            '8 ORE => 3 B',
            '7 ORE => 5 C',
            '3 A, 4 B => 1 AB',
            '5 B, 7 C => 1 BC',
            '4 C, 1 A => 1 CA',
            '2 AB, 3 BC, 4 CA => 1 FUEL',
        ]
        self.assertEqual(ore_needed(strs), 165)


    def test_large_example1(self):
        strs = [
            '157 ORE => 5 NZVS',
            '165 ORE => 6 DCFZ',
            '44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL',
            '12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ',
            '179 ORE => 7 PSHF',
            '177 ORE => 5 HKGWZ',
            '7 DCFZ, 7 PSHF => 2 XJWVT',
            '165 ORE => 2 GPVTF',
            '3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT',
        ]
        self.assertEqual(ore_needed(strs), 13312)
        self.assertEqual(max_fuel(strs), 82892753)


    def test_large_example2(self):
        strs = [
            '2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG',
            '17 NVRVD, 3 JNWZP => 8 VPVL',
            '53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL',
            '22 VJHF, 37 MNCFX => 5 FWMGM',
            '139 ORE => 4 NVRVD',
            '144 ORE => 7 JNWZP',
            '5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC',
            '5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV',
            '145 ORE => 6 MNCFX',
            '1 NVRVD => 8 CXFTF',
            '1 VJHF, 6 MNCFX => 4 RFSQX',
            '176 ORE => 6 VJHF',
        ]
        self.assertEqual(ore_needed(strs), 180697)
        self.assertEqual(max_fuel(strs), 5586022)


    def test_large_example3(self):
        strs = [
            '171 ORE => 8 CNZTR',
            '7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL',
            '114 ORE => 4 BHXH',
            '14 VRPVC => 6 BMBT',
            '6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL',
            '6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT',
            '15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW',
            '13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW',
            '5 BMBT => 4 WPTQ',
            '189 ORE => 9 KTJDG',
            '1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP',
            '12 VRPVC, 27 CNZTR => 2 XDBXC',
            '15 KTJDG, 12 BHXH => 5 XCVML',
            '3 BHXH, 2 VRPVC => 7 MZWV',
            '121 ORE => 7 VRPVC',
            '7 XCVML => 6 RJRHP',
            '5 BHXH, 4 VRPVC => 5 LTCX',
        ]
        self.assertEqual(ore_needed(strs), 2210736)
        self.assertEqual(max_fuel(strs), 460664)


    def test_part1(self):
        strs = util.read_lines('inputs/q14')
        self.assertEqual(ore_needed(strs), 201324)


    def test_part2(self):
        strs = util.read_lines('inputs/q14')
        self.assertEqual(max_fuel(strs), 6326857)
