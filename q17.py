import intcode
import enum

program = intcode.IntcodeSim.fromFile("inputs/q17")

class Direction(enum.IntEnum):
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

def print_grid(grid):
    for row in grid:
        print("".join(row))

def mark_intersections(grid):
    parameter_sum = 0

    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            if all(grid[y][x] == '#' for (y,x) in [(y+1,x), (y-1,x), (y,x+1), (y,x-1), (y,x)]):
                grid[y][x] = 'O'
                parameter_sum += (y * x)

    return parameter_sum

program.run()

x, y = 0, 0
grid = [[' '] * 45 for _ in range(33)]
for char in program.outputs:
    if char == 10:
        y += 1
        x = 0
    else:
        grid[y][x] = chr(char)
        x += 1

print_grid(grid)

print(mark_intersections(grid))
print_grid(grid)

# The path was manually generated, then I ran an algorithm to try various prefix
# values for A and suffix values for C. When that algorithm didn't work immediately,
# I poked at it manually for a few minutes and found them.
A = "R,12,L,8,R,10"
B = "R,8,L,12,R,8"
C = "R,8,L,8,L,8,R,8,R,10"
# I thought we might need to convert distances to multiples of 2 e.g. 2,2,2,2
# but it wasn't needed.
Movement = "B,A,A,B,C,B,B,C,A,C"

program = intcode.IntcodeSim.fromFile("inputs/q17")
# Wake robot up
assert program.arr[0] == 1
program.setMemory(0, 2)

# Send movement functions on start
for function in [Movement, A, B, C]:
    for char in function:
        program.queueInput(ord(char))

    program.queueInput(10)

# Indicate if we want the video feed
program.queueInput(ord('y')).queueInput(10)

def clearScreen():
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')

buf = ""
def handleOutput(char):
    "handle screen rendering and final dust value"
    global buf
    if char == 10 and buf.endswith("\n"):
        clearScreen()
        print(buf)
        buf = ""
    elif char > 255:
        print(f"Dust: {char}")
    else:
        buf += chr(char)

program.outputFn = handleOutput
clearScreen()
program.run()
print("finished")
