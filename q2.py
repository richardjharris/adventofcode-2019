from enum import IntEnum
import sys
import copy

class Opcode(IntEnum):
    add = 1
    mul = 2
    end = 99

def loadInput(filename):
    """ load input filename into list of integers """
    arr = []
    with open(filename, 'r') as f:
        for line in f:
            arr += splitIncodeLine(line)
    return arr

def splitIncodeLine(string):
    """ split a string and return its integer components as a list """
    return list([int(x) for x in string.split(',')])

def runIntcode(arr):
    """ execute intcode from array of integers """
    pos = 0
    exiting = False
    # We're going to overwrite arr, so copy it
    arr = copy.copy(arr)
    while not exiting:
        op = arr[pos]
        if op == Opcode.add:
            inputPos1 = arr[pos+1]
            inputPos2 = arr[pos+2]
            outputPos = arr[pos+3]
            pos += 4

            arr[outputPos] = arr[inputPos1] + arr[inputPos2]

        elif op == Opcode.mul:
            inputPos1 = arr[pos+1]
            inputPos2 = arr[pos+2]
            outputPos = arr[pos+3]
            pos += 4

            arr[outputPos] = arr[inputPos1] * arr[inputPos2]

        elif op == Opcode.end:
            exiting = True
        else:
            print "unknown opcode: " + str(op)
            exiting = True

    # Return output state
    return arr

# exampleIntcode = "1,9,10,3,2,3,11,0,99,30,40,50"
# exampleIntcode = "1,1,1,4,99,5,6,0,99"

def part1():
    intcode = loadInput('inputs/q02')
    # Patch code as directed
    intcode[1] = 12
    intcode[2] = 2

    print runIntcode(intcode)

def part2():
    """ figure out the inputs required to generate an specified output """
    targetOutput = 19690720
    for input1 in xrange(0,99):
        for input2 in xrange(0,99):
            intcode = loadInput('inputs/q02')
            intcode[1] = input1
            intcode[2] = input2
            result = runIntcode(intcode)
            if result[0] == targetOutput:
                print "Got result with input1=" + str(input1) + " input2=" + str(input2)
                print "Answer code = " + str(input1 * 100 + input2)
                sys.exit(0)

part2()
