import intcode
import enum
import grid

grid = grid.Grid(default='x')
x, y = 0, 0
def handle_output(char):
    global x, y, grid
    if char == 10:
        y += 1
        x = 0
    else:
        grid[x,y] = chr(char)
        x += 1

def mark_intersections(grid):
    parameter_sum = 0

    for cell in grid.cells():
        if all(v == '#' for v in cell.neighbour_values(and_me=True)):
            cell.val = 'O'
            parameter_sum += (cell.y * cell.x)

    return parameter_sum

program = intcode.IntcodeSim.fromFile("inputs/q17")
program.outputFn = handle_output
program.run()
print(str(grid))
print(mark_intersections(grid))
print(str(grid))

import sys; sys.exit(0)

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
program.queueInput(ord('n')).queueInput(10)

def clearScreen():
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')

buf = ""
def handleOutput(char):
    "handle screen rendering and final dust value"
    global buf
    if char == 10 and buf.endswith("\n"):
        #clearScreen()
        print(buf)
        buf = ""
    elif char > 255:
        print(f"Dust: {char}")
    else:
        buf += chr(char)

program.outputFn = handleOutput
#clearScreen()
program.run()
print("finished")
