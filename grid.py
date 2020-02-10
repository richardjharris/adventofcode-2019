from __future__ import annotations
import collections
import inspect
import unittest

from gridcell import GridCell
from direction import Direction
import vector

class Grid():
    def __init__(self, default=None):
        self.default = default
        self.data = {}
        self._collision_values = set()


    def __getitem__(self, pos):
        return self.get(pos)


    def __setitem__(self, pos, value):
        self.set(pos, value)


    def get(self, pos):
        x, y = pos
        if (x,y) in self.data:
            return self.data[(x,y)]
        else:
            return self.default


    def set(self, pos, value):
        x, y = pos
        self.data[(x,y)] = value


    def at(self, *pos):
        x, y = pos
        return GridCell(x=x, y=y, grid=self)


    def cells(self):
        "iterator returning all cells, as GridCell objects"
        for xy in self.data.keys():
            yield self.at(xy[0], xy[1])


    def collides(self, x, y, from_dir=None) -> bool:
        # not supported yet
        assert from_dir is None
        return self[x, y] in self._collision_values


    def set_collision(self, value, is_collision=True):
        if is_collision:
            self._collision_values.add(value)
        else:
            self._collision_values.remove(value)


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


    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as fh:
            grid = Grid.from_string(filename.read().rstrip('\n'))
        return grid


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

    def test_collides(self):
        g = Grid.from_string("***\n* *\n***")
        g.set_collision("*")
        self.assertEqual(g.collides(0, 0), True)
        self.assertEqual(g.collides(2, 2), True)
        self.assertEqual(g.collides(1, 1), False)

        g.set_collision("*", False)
        self.assertEqual(g.collides(0, 0), False)
