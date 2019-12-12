from intcode import IntcodeSim
from util import slurp

def part1():
    boost = slurp('inputs/q09')
    # Run in test mode using input 1
    i = IntcodeSim(boost)
    i.queueInput(1)
    i.run()
    print(i.outputs)

def part2():
    boost = slurp('inputs/q09')
    # Run in sensor boost mode with a value of 2
    i = IntcodeSim(boost).queueInput(2).run()
    print(i.outputs)

part2()

