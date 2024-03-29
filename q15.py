import enum
import math
import sys
from intcode import IntcodeSim
from dataclasses import dataclass, field
from collections import defaultdict
from util import path_find

# Functional programming: am I a joke to you?
sys.setrecursionlimit(2000)


class Status(enum.Enum):
    hit_wall = 0
    moved = 1
    moved_to_goal = 2


# Characters for map rendering (and logic)
WALL = '██'
ROUTE = '░░'
CLEAR = '  '
DROID = '🤖'
OXYGEN = '🎄'

# Empty tiles only appear as part of walls that we cannot see, so it
# looks nicer to render them as walls
EMPTY = WALL

movement = [
    (0, -1),  # 1 = North
    (0, 1),   # 2 = South
    (-1, 0),  # 3 = West
    (1, 0),   # 4 = East
]
reverse_movement = [1,0,3,2]

def apply_movement(pos, code):
    "apply movement code to position and return new position"
    return (pos[0] + movement[code][0], pos[1] + movement[code][1])


@dataclass
class BotHandler():
    """
    controls the droid. we don't make any assumptions about the type
    of world we're in. We simply probe in all four directions depth-
    first, backtracking once we run out of ways to go.

    The code is pretty sub-optimal, but works.
    """
    # Position of the bot, relative to the starting point (0,0)
    position = (0,0)
    # Mapping of (x,y) to a char indicating what is there
    world: dict = field(default_factory=dict)
    # Code of last move sent from input handler (0-indexed). Used in the output handler.
    last_move_code = None
    # Location of oxygen system, if known
    oxygen_system = None
    # History of moves made so far, used when backtracking.
    move_history: list = field(default_factory=list)
    # Set of (x,y) tuples we've already moved to. Used to avoid cycles.
    done: set = field(default_factory=set)
    # Keep track of min/max co-ordinates seen. Used when rendering the map.
    minX: int = 0
    minY: int = 0
    maxX: int = 0
    maxY: int = 0
    # Flag indicating if our last input command was a backtrack. If so, the output
    # handler skips most of its logic.
    backtracked: bool = False

    def handleInput(self):
        "send the robot a movement command"
        # Are there unknown squares around our position?
        for code in range(4):
            target = apply_movement(self.position, code)
            if target not in self.done:
                if target not in self.world or self.world[target] != WALL:
                    # Go in that direction
                    self.last_move_code = code
                    return code + 1

        # Can we backtrack?
        if self.move_history:
            last_code = self.move_history.pop()
            reversed_code = reverse_movement[last_code]
            self.last_move_code = reversed_code
            self.backtracked = True
            return reversed_code + 1

        # We've covered the whole map. Terminate execution.
        return None
             

    def handleOutput(self, status):
        "indicates status of last movement"
        if self.backtracked:
            # We've already been here, so we don't need to handle
            # anything except updating our position
            self.position = apply_movement(self.position, self.last_move_code)
            self.backtracked = False
            self.last_move_code = None
            return

        status = Status(status)
        assert self.last_move_code is not None
        target = apply_movement(self.position, self.last_move_code)
        self.done.add(target)

        if status == Status.hit_wall:
            self.world[target] = WALL
        elif status == Status.moved or status == Status.moved_to_goal:
            self.world[target] = CLEAR
            self.position = target
            if status == Status.moved_to_goal:
                self.oxygen_system = target
            # Add the last_move_code to history, so we can undo
            self.move_history.append(self.last_move_code)
            self.last_move_code = None

        self.minX = min(self.minX, target[0])
        self.maxX = max(self.maxX, target[0])
        self.minY = min(self.minY, target[1])
        self.maxY = max(self.maxY, target[1])


    def paintMap(self, route=[]):
        for y in range(self.minY, self.maxY + 1):
            for x in range(self.minX, self.maxX + 1):
                pos = (x,y)
                c = EMPTY
                if self.position == pos:
                    c = DROID
                elif self.oxygen_system == pos:
                    c = OXYGEN
                elif pos in route:
                    c = ROUTE
                elif pos in self.world:
                    c = self.world[pos]
                print(c, end='')
            print('')
        print('')


    def neighboursOf(self, point):
        "given a co-ordinate, return its neighbours (i.e. non-wall pieces)"
        n = set()
        for code in range(4):
            target = apply_movement(point, code)
            if target in self.world and self.world[target] is not WALL:
                n.add(target)
        return n

    def findRoute(self, start, goal):
        """
        Return minimal route from start to goal along the maze.

        """
        return path_find(
            start=start,
            goal=goal,
            neighbour_func=lambda p: self.neighboursOf(p),
        )

    def spreadOxygen(self):
        """
        Returns the number of minutes required to spread oxygen through
        the entire map, starting from the oxygen system.

        As it takes a minute to spread oxygen from a point to its neighbours,
        and the maze layout is a tree (no loops) of corridors with width=1,
        this is equal to the largest distance from the oxygen system to
        a dead end.
        """
        def distanceToDeadEnd(point, cameFrom=None):
            "returns the distance from point to a dead-end"
            neighbours = self.neighboursOf(point)
            neighbours.discard(cameFrom)
            if neighbours:
                return 1 + max(distanceToDeadEnd(n, point) for n in neighbours)
            else:
                # We reached a dead-end: 
                return 0

        return distanceToDeadEnd(self.oxygen_system)


handler = BotHandler()
i = IntcodeSim.fromFile("inputs/q15")
i.inputFn = lambda: handler.handleInput()
i.outputFn = lambda status: handler.handleOutput(status)
i.run()
handler.paintMap()

# Now work out distance from droid to oxygen handler, using A*
droid_position = (0,0)
oxygen_position = handler.oxygen_system
print(f"droid at {droid_position}, oxygen at {oxygen_position}")
assert droid_position is not None
assert oxygen_position is not None
route = handler.findRoute(start=droid_position, goal=oxygen_position)
handler.paintMap(route=route)
print(route)
# Route length should not include the droid
print(len(route) - 1)

# Now do oxygen stuff
print(handler.spreadOxygen())
