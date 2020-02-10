import dataclasses
import math
import numbers
import unittest

@dataclasses.dataclass
class Vector2D():
    """
    A 2D vector with x and y values.
    """

    x: float = 0
    y: float = 0

    def __repr__(self):
        return "Vector(%r, %r)" % (self.x, self.y)


    def __iter__(self):
        yield self.x
        yield self.y


    def __abs__(self):
        return self.euclidean_norm()


    def __bool__(self):
        return bool(self.x or self.y)


    def __add__(self, other):
        c = self.copy()
        c += other
        return c


    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self


    def __sub__(self, other):
        c = self.copy()
        c -= other
        return c


    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self


    def __mul__(self, other):
        c = self.copy()
        c *= other
        return c


    def __rmul__(self, other):
        return self * other


    def __imul__(self, other):
        if isinstance(other, numbers.Real):
            return Vector2D(self.x * other, self.y * other)
        else:
            return NotImplemented


    def __matmul__(self, other):
        try:
            return dot_product(self, other)
        except TypeError:
            return NotImplemented


    def __rmatmul__(self, other):
        return self @ other


    def __neg__(self):
        return Vector2D(-self.x, -self.y)


    def __getitem__(self, index):
        if isinstance(index, numbers.Integral):
            if index == 0:
                return self.x
            elif index == 1:
                return self.y
            else:
                raise IndexError()
        else:
            raise TypeError(f"{cls.__name__} indices be integers")


    def atan2(self, n):
        "returns counterclockwise angle between vector and positive x-axis, in radians, -pi .. pi"
        return math.atan2(self.y, self.x)


    def euclidean_norm(self):
        return math.hypot(self.x, self.y)


    def manhattan_norm(self):
        return abs(self.x) + abs(self.y)


    def copy(self):
        return Vector2D(self.x, self.y)


    def minimize(self, other):
        self.x = min(self.x, other.x)
        self.y = min(self.y, other.y)


    def maximize(self, other):
        self.x = max(self.x, other.x)
        self.y = max(self.y, other.y)


def dot_product(a, b):
    return (a.x * b.x) + (a.y * b.y)


def cross_product(a, b):
    return (a.x * b.y) - (a.y * b.x)


def manhattan_distance(a, b):
    "returns manhattan distance (length of L-shape from a to b)"
    return abs(a.x - b.x) + abs(a.y - b.y)


def euclidean_distance(a, b):
    "returns Euclidean distance (length of straight line between and a b)"
    return math.hypot((a.x - b.x), (a.y - b.y))


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

    def test_tuple(self):
        v = xy(42, -100)
        x, y = v
        self.assertEqual(x, 42)
        self.assertEqual(y, -100)
