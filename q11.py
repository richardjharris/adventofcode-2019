from util import slurp
from intcode import IntcodeSim
from enum import Enum
import sys

class Color(Enum):
    black = 0
    white = 1

class Direction(Enum):
    "each direction is 90' right of the previous"
    up = 0
    right = 1
    down = 2
    left = 3

MOVEMENT = {
    Direction.up: (0, -1),
    Direction.right: (1, 0),
    Direction.left: (-1, 0),
    Direction.down: (0, 1),
}

code = slurp('q11_input')
i = IntcodeSim(code)

# Robot position
pos = (0, 0)
# Robot turning direction
facing = Direction.up
# Dict mapping co-ords to the color painted
painted = {}

# For part2, robot is starting on a white panel instead
# Comment out for part1.
painted[pos] = Color.white

def handleInput():
    "returns color of robot's current panel"
    print(f"asking for input at {pos}")
    if pos in painted:
        return painted[pos].value
    else:
        return Color.black.value

def handleOutput(x):
    global pos
    global facing
    if handleOutput.goingToTurn:
        print(f"going to turn (x={x})")
        newFacing = facing.value + (1 if x == 1 else -1)
        newFacing = newFacing % len(Direction)
        print(f"facing {facing} -> {Direction(newFacing)}")
        facing = Direction(newFacing)

        # Move forward one panel
        move = MOVEMENT[facing]
        pos = (pos[0] + move[0], pos[1] + move[1])
        print(f"pos now {pos} (move={move})")

        # Next output is painting
        handleOutput.goingToTurn = False
    else:
        print(f"going to paint (x={x})")
        painted[pos] = Color(x)
        handleOutput.goingToTurn = True
handleOutput.goingToTurn = False

i.inputFn = handleInput
i.outputFn = handleOutput
i.run()

# Find out how many unique panels were painted (part1)
print(len(painted))

# Print the paint job
# We need the min and max co-ordinates
minX = min(painted, key=lambda p: p[0])[0]
minY = min(painted, key=lambda p: p[1])[1]
maxX = max(painted, key=lambda p: p[0])[0]
maxY = max(painted, key=lambda p: p[1])[1]

for y in range(minY, maxY + 1):
    for x in range (minX, maxX + 1):
        color = painted[(x,y)] if (x,y) in painted else Color.white
        char = "." if color == Color.black else "#"
        sys.stdout.write(char)
    sys.stdout.write("\n")
sys.stdout.flush()
