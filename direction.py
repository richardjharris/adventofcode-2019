import aenum
import unittest
import vector

class Direction(aenum.Enum, settings=aenum.Unique):
    # In clockwise order
    up      = vector.xy(0, -1)
    right   = vector.xy(1, 0)
    down    = vector.xy(0, 1)
    left    = vector.xy(-1, 0)


    def turn_clockwise(self):
        return self._turn(1)


    def turn_counterclockwise(self):
        return self._turn(-1)


    def reverse(self):
        return self._turn(2)


    def _turn(self, clockwise_turns):
        members = list(self.__class__)
        index = members.index(self)
        return members[(index + clockwise_turns) % len(members)]


def directions():
    return Direction.__members__.values()


class TestVector(unittest.TestCase):
    def test_basic(self):
       up = Direction.up
       self.assertEqual(up.value, vector.xy(0, -1))
       self.assertEqual(up.reverse(), Direction.down)
       self.assertEqual(up.reverse().value, vector.xy(0, 1))
       self.assertEqual(Direction.down.reverse(), Direction.up)
       self.assertEqual(Direction.left.reverse(), Direction.right)
       self.assertEqual(Direction.right.reverse(), Direction.left)


    def test_turn(self):
        self.assertEqual(Direction.up.turn_clockwise(), Direction.right)
        self.assertEqual(Direction.up.turn_counterclockwise(), Direction.left)
        self.assertEqual(Direction.left.turn_clockwise(), Direction.up)
        self.assertEqual(Direction.left.turn_counterclockwise(), Direction.down)
        self.assertEqual(Direction.down.turn_clockwise(), Direction.left)
        self.assertEqual(Direction.down.turn_counterclockwise(), Direction.right)
        self.assertEqual(Direction.right.turn_clockwise(), Direction.down)
        self.assertEqual(Direction.right.turn_counterclockwise(), Direction.up)
