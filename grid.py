from __future__ import annotations
import collections
import dataclasses
import inspect
import unittest
import vector

@dataclasses.dataclass
class Cell():
    """
    cursor into a value in a grid. also allows manipulation of neighbouring
    cells
    """
    x: int
    y: int
    val = property()
    grid: Grid

    @property
    def val(self):
        return self.grid[self.coord()]


    @val.setter
    def val(self, value):
        self.grid[self.coord()] = value 


    def __repr__(self):
        # Omit grid reference, as it is typically known
        return f"Cell(x={self.x}, y={self.y}, val={self.val})"


    def coord(self):
        return (self.x, self.y)


    def vector(self):
        return vector.Vector2D(x=self.x, y=self.y)


    def neighbour_values(self, and_me=False):
        """
        return the values of the values of cells adjacent to this one in four
        directions, plus our own value (if here=True)
        """
        x, y = self.x, self.y
        for pos in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            yield self.grid[pos]

        if and_me:
            yield self.grid[x,y]


class Grid():
    def __init__(self, default=None):
        self.default = default
        self.data = {}


    def __getitem__(self, index):
        if isinstance(index, tuple):
            x, y = index
            if not isinstance(x, int):
                raise TypeError('x has invalid type')
            if not isinstance(y, int):
                raise TypeError('y has invalid type')
            return self.get(x, y)
        else:
            raise TypeError('invalid argument type')


    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            x, y = index
            if not isinstance(x, int):
                raise TypeError('x has invalid type')
            if not isinstance(y, int):
                raise TypeError('y has invalid type')
            self.set(x, y, value)
        else:
            raise TypeError('invalid argument type')


    def get(self, x, y):
        if (x,y) in self.data:
            return self.data[(x,y)]
        else:
            return self.default


    def set(self, x, y, value):
        self.data[(x,y)] = value


    def at(self, x, y):
        return Cell(x=x, y=y, grid=self)


    def cells(self):
        "iterator returning all cells, as Cell objects"
        for xy in self.data.keys():
            yield self.at(xy[0], xy[1])


    def count(self, *values):
        "return count of grid cells which contain any of the given values"
        count = 0
        for cell in self.cells():
            if cell.val in values:
                count += 1
        return count


    def find(self, *targets):
        "return first cell containing any value in targets, otherwise None"
        for cell in self.cells():
            if cell.val in targets:
                return cell
        return None


    def bounds(self):
        """
        return vectors indicating top left and bottom right corners of
        the grid
        """
        min_x = min(x for x, _ in self.data.keys())
        max_x = max(x for x, _ in self.data.keys())
        min_y = min(y for _, y in self.data.keys())
        max_y = max(y for _, y in self.data.keys())

        return vector.xy(min_x, min_y), vector.xy(max_x, max_y)


    def render(self):
        "render grid to screen"

        # Check if we're empty
        if not self.data:
            return ""

        top_left, bottom_right = self.bounds()
        out = []
        for y in range(top_left.y, bottom_right.y + 1):
            chars = (self[x,y] for x in range(top_left.x, bottom_right.x + 1))
            out.append("".join(chars))

        return "\n".join(out)
        

    @classmethod
    def from_docstring(cls, s):
        # Remove common intentation and trailing newlines
        return cls.from_string(inspect.cleandoc(s))


    @classmethod
    def from_string(cls, s):
        g = Grid()
        x, y = 0, 0
        for line in s.split('\n'):
            for char in line:
                g[x,y] = char
                x += 1
            x = 0
            y += 1
        return g


    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


    def __str__(self):
        return self.render()


class TestGrid(unittest.TestCase):
    def test_basic(self):
        g = Grid(default=False)
        g[1,1] = True
        g[2,2] = True
        g[-3,1] = True
        self.assertEqual(g[0,0], False)
        self.assertEqual(g[1,1], True)
        self.assertEqual(g[2,2], True)
        self.assertEqual(g[1,2], False)
        self.assertEqual(g[-3,1], True)

    def test_count(self):
        g = Grid()
        g[0,1] = '!'
        g[0,2] = '!'
        self.assertEqual(g.count('!'), 2)
        self.assertEqual(g.count('#'), 0)

    def test_from_docstring(self):
        g = Grid.from_docstring("""
            123
            456
            789
        """)
        self.assertEqual(g[1,1], '5')
        self.assertEqual(g[0,1], '4')
        self.assertEqual(g[1,2], '8')


    def test_find(self):
        g = Grid()
        g[1,1] = 'a'
        g[1,2] = 'b'
        g[1,3] = 'c'
        self.assertEqual(g.find('a').x, 1)
        self.assertEqual(g.find('a').y, 1)
        self.assertEqual(g.find('c').x, 1)
        self.assertEqual(g.find('c').y, 3)


    def test_render(self):
        g = Grid(default = '.')
        g[1,1] = 'x'
        g[1,2] = 'y'
        self.assertEqual(g.bounds(), (vector.xy(1,1), vector.xy(1,2)))
        self.assertEqual(str(g), "x\ny")

        g = Grid(default = '.')
        g[-1,-1] = 'x'
        g[-1,0] = 'y'
        g[-1,1] = 'z'
        g[0,1] = 't'
        self.assertEqual(g.bounds(), (vector.xy(-1,-1), vector.xy(0,1)))
        self.assertEqual(str(g), "x.\ny.\nzt")
