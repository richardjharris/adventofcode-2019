import dataclasses
import math
import unittest

@dataclasses.dataclass
class Vector2D():
    """
    A 2D vector with x and y values.
    """

    x: float = 0
    y: float = 0

    def __add__(self, o):
        return Vector2D(self.x + o.x, self.y + o.y)


    def __sub__(self, o):
        return Vector2D(self.x - o.x, self.y - o.y)


    def __mul__(self, o):
        return Vector2D(self.x * o, self.y * o)


    def __neg__(self):
        return Vector2D(-self.x, -self.y)


    def euclidean_norm(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y))


    def manhattan_norm(self):
        return abs(self.x) + abs(self.y)


    def copy(self):
        return Vector2D(self.x, self.y)



def dot_product(a, b):
    return (a.x * b.x) + (a.y * b.y)


def cross_product(a, b):
    return (a.x * b.y) - (a.y * b.x)


def manhattan_distance(a, b):
    "returns manhattan distance (length of L-shape from a to b)"
    return abs(a.x - b.x) + abs(a.y - b.y)


def euclidean_distance(a, b):
    "returns Euclidean distance (length of straight line between and a b)"
    return math.sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y))


def xy(x, y):
    "shorthand to create a 2d vector"
    return Vector2D(x, y)


class TestVector(unittest.TestCase):
    def test_basic(self):
        v = xy(10, 20)
        self.assertEqual(v.x, 10)
        self.assertEqual(v.y, 20)
        self.assertEqual(v.manhattan_norm(), 30)

    def test_operator(self):
        v = xy(1, 1)
        self.assertEqual( v - xy(1, 1), xy(0, 0) )
        self.assertEqual( v - xy(-1, 10), xy(2, -9) )
        self.assertEqual( v + xy(3, 2), xy(4, 3) )
        self.assertEqual( v * 5, xy(5, 5) )
        self.assertEqual( xy(1, 2) * 5, xy(5, 10) )
        self.assertEqual(-xy(3,-5), xy(-3, 5))
