from intcode import IntcodeSim
from util import slurp

def part1():
    boost = slurp('q9_input')
    # Run in test mode using input 1
    i = IntcodeSim(boost)
    i.queueInput(1)
    i.run()
    print(i.outputs)

part1()

