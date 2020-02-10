from __future__ import annotations
from dataclasses import dataclass
from direction import Direction, directions
import vector

@dataclass
class GridCell():
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


    def collides(self, from_dir=None) -> bool:
        return self.grid.collides(self.x, self.y, from_dir=from_dir)


    def neighbour(self, direction):
        return self.grid.at(self.vector() + direction)


    def left(self):
        return self.neighbour(Direction.left)

    def right(self):
        return self.neighbour(Direction.right)

    def up(self):
        return self.neighbour(Direction.up)

    def down(self):
        return self.neighbour(Direction.down)


    def neighbours(self, exclude=set(), collision=True):
        """
        return GridCells for this cell's neighbours
        """
        pos = self.vector()
        for direction in directions():
            if direction in exclude:
                continue
            neighbour = self.neighbour(direction)
            if collision and neighbour.collides():
                continue

            yield neighbour, direction



