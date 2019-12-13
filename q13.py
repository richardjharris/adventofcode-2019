from dataclasses import dataclass, field
from enum import Enum
from intcode import IntcodeSim
from typing import *

class Tile(Enum):
    empty = 0
    wall = 1
    block = 2
    bat = 3
    ball = 4

class Screen():
    chars = {
        Tile.empty: ' ',
        Tile.wall: '%',
        Tile.block: 'E',
        Tile.bat: '=',
        Tile.ball: '*',
    }

    canvas: List[List[Tile]] = []
    width: int
    height: int

    def __init__(self, width: int = 40, height: int =25):
        self.canvas = []
        self.width = width
        self.height = height
        for y in range(height):
            row = [Tile.empty] * width
            self.canvas.append(row)

    def set(self, x: int, y: int, tile: Tile):
        self.canvas[y][x] = tile

    def get(self, x: int, y: int) -> Tile:
        return self.canvas[y][x]

    def render(self) -> str:
        rows = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += self.chars[self.get(x,y)]
            rows.append(row)
        return "\n".join(rows)

    def countTiles(self, tile: Tile) -> int:
        count = 0
        for y in range(self.height):
            count += self.canvas[y].count(tile)
        return count

def part1():
    screen = Screen()
    state = []
    def handleOutput(output: int):
        nonlocal state
        if len(state) < 3:
            state.append(output)

        if len(state) == 3:
            x, y, tileNo = state
            state = []
            screen.set(x, y, Tile(tileNo))

    i = IntcodeSim.fromFile("inputs/q13")
    i.outputFn = handleOutput
    i.run()
    renderedScreen = screen.render()
    print(renderedScreen)
    blockTiles = screen.countTiles(Tile.block)
    print(blockTiles)
    # 286

def part2():
    screen = Screen()

    @dataclass
    class State():
        args: List[int] = field(default_factory=list)
        score: int = 0
        step: int = 0
        ballPos: Optional[Tuple[int, int]] = None
        batPos: Optional[Tuple[int, int]] = None

    state = State()

    def handleOutput(output: int) -> None:
        if len(state.args) < 2:
            # Record x,y co-ordinates for next call
            state.args.append(output)
            return

        x, y = state.args
        state.args.clear()

        if x == -1 and y == 0:
            state.score = output
        else:
            tile = Tile(output)
            screen.set(x, y, tile)

            # Keep track of bat/ball position
            if tile == Tile.bat:
                state.batPos = (x,y)
            elif tile == Tile.ball:
                state.ballPos = (x, y)

            state.step += 1
            # Have we rendered the initial screen?
            if state.step > 900:
                print(screen.render())
                print("Score: " + str(state.score))

    def handleInput() -> int:
        if state.ballPos is None or state.batPos is None:
            # Don't know what to do yet, stay put
            return 0
        else:
            # Follow the ball
            delta = state.batPos[0] - state.ballPos[0]
            if delta < 0:
                return 1
            elif delta == 0:
                return 0
            else:
                return -1

    i = IntcodeSim.fromFile("inputs/q13")
    # Set machine to 'play for free' mode
    i.setMemory(0, 2)
    i.inputFn = handleInput
    i.outputFn = handleOutput
    i.run()
    print(f"finished with score: {state.score}")

part2()
