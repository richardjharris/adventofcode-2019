# From this point on, we're using Python 3.

from enum import IntEnum
import sys
import copy

class Opcode(IntEnum):
    add = 1
    mul = 2
    input = 3
    output = 4
    jump_if_true = 5
    jump_if_false = 6
    less_than = 7
    equals = 8
    end = 99

class ParameterMode(IntEnum):
    position = 0
    immediate = 1

def loadInput(filename):
    """ load input filename into list of integers """
    arr = []
    with open(filename, 'r') as f:
        for line in f:
            arr += splitIntcode(line.rstrip('\n'))
    return arr

def splitIntcode(string):
    """ split a string and return its integer components as a list """
    return list([int(x) for x in string.split(',')])

def parseOpcode(opcode):
    """ split an opcode into an Opcode value and an array of three
        ParameterModes (one per opcode parameter) """
    op = Opcode(opcode % 100)
    opcode //= 100

    parameterModes = []
    while opcode != 0:
        parameterModes.append(ParameterMode(opcode % 10))
        opcode //= 10

    return op, parameterModes

def runIntcode(arr):
    """ execute intcode from array of integers """
    pos = 0
    exiting = False
    # We're going to overwrite arr, so copy it
    arr = copy.copy(arr)

    while not exiting:
        op, parameterModes = parseOpcode(arr[pos])
        print(op, parameterModes)
        pos += 1

        # Lambda to get argument at position n (1~) for value x
        def arg(n, x):
            print(n, x, parameterModes)
            mode = parameterModes[n-1] if n <= len(parameterModes) \
                else ParameterMode.position

            if mode == ParameterMode.position:
                return arr[x]
            elif mode == ParameterMode.immediate:
                return x
            else:
                raise ValueError("invalid ParameterMode")

        if op == Opcode.add:
            input1 = arr[pos]
            input2 = arr[pos+1]
            outputPos = arr[pos+2]
            pos += 3

            # NB: output positions are always immediate.
            arr[outputPos] = arg(1, input1) + arg(2, input2)

        elif op == Opcode.mul:
            input1 = arr[pos]
            input2 = arr[pos+1]
            outputPos = arr[pos+2]
            pos += 3

            arr[outputPos] = arg(1, input1) * arg(2, input2)
        
        elif op == Opcode.input:
            outputPos = arr[pos]
            pos += 1

            value = input('Enter value: ')
            arr[outputPos] = int(value)

        elif op == Opcode.output:
            input1 = arr[pos]
            pos += 1

            value = arg(1, input1)
            print(value)

        elif op == Opcode.jump_if_true:
            input1 = arr[pos]
            location = arr[pos+1]
            pos += 2

            if arg(1, input1) != 0:
                pos = arg(2, location)

        elif op == Opcode.jump_if_false:
            input1 = arr[pos]
            location = arr[pos+1]
            pos += 2

            if arg(1, input1) == 0:
                pos = arg(2, location)

        elif op == Opcode.less_than:
            a = arr[pos]
            b = arr[pos+1]
            outputPos = arr[pos+2]
            pos += 3

            arr[outputPos] = 1 if arg(1, a) < arg(2, b) else 0

        elif op == Opcode.equals:
            a = arr[pos]
            b = arr[pos+1]
            outputPos = arr[pos+2]
            pos += 3

            arr[outputPos] = 1 if arg(1, a) == arg(2, b) else 0

        elif op == Opcode.end:
            exiting = True
        else:
            raise ValueError("unknown opcode: " + op)

    # Return output state
    return arr

# Part 1
#testProgram = open('q5_input').read().rstrip('\n')
#intCode = splitIntcode(testProgram)
#runIntcode(intCode)

# Part 1 testing
# mulitply value at addr 4 (33) + imm. 3. Write 99 to addr 4.
#test = "1002,4,3,4,33"
#print(runIntcode(splitIntcode(test)))

# Part 2 testing
#runIntcode(splitIntcode("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"))

# Output 999 is < 8, 1000 is =8, 1001 if > 8
#test = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
#runIntcode(splitIntcode(test))

testProgram = open('inputs/q05').read().rstrip('\n')
intCode = splitIntcode(testProgram)
runIntcode(intCode)
