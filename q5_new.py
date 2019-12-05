from enum import IntEnum
import sys
import copy
import unittest

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

class IntcodeSim:
    def __init__(self, code):

        # Allow a string to be passed, for convenience
        if isinstance(code, str):
            code = self.split(code)
        else:
            # We will modify this list, so copy it
            code = copy.copy(code)

        self.arr = code
        self.pos = 0
        self.finished = False
        self.queuedInputs = []
        self.outputs = []

    def queueInput(self, value):
        self.queuedInputs.append(value)
        return self

    def __getInput(self):
        if len(self.queuedInputs):
            return self.queuedInputs.pop(0)
        else:
            value = input('Enter value: ')
            return int(value)

    def __putOutput(self, value):
        self.outputs.append(value)

    @classmethod
    def fromFile(cls, filename):
        """ load input filename into list of integers """
        arr = []
        with open(filename, 'r') as f:
            for line in f:
                arr += cls.split(line.rstrip('\n'))
        return cls(arr)
    
    @staticmethod
    def split(string):
        """ split a string and return its integer components as a list """
        return list([int(x) for x in string.split(',')])

    @staticmethod
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

    def run(self):
        """ execute the intcode until we reach the end """
        while not self.finished:
            self.__runStep()
        return self
    
    def __runStep(self):
        """ execute a single instruction """
        if self.finished:
            return

        op, parameterModes = self.parseOpcode(self.arr[self.pos])
        self.pos += 1

        # Lambda to get argument at position n (1~) for value x
        def arg(n, x):
            mode = parameterModes[n-1] if n <= len(parameterModes) \
                else ParameterMode.position

            if mode == ParameterMode.position:
                return self.arr[x]
            elif mode == ParameterMode.immediate:
                return x
            else:
                raise ValueError("invalid ParameterMode")

        if op == Opcode.add:
            input1 = self.arr[self.pos]
            input2 = self.arr[self.pos+1]
            outputPos = self.arr[self.pos+2]
            self.pos += 3

            # NB: output self.positions are always immediate.
            self.arr[outputPos] = arg(1, input1) + arg(2, input2)

        elif op == Opcode.mul:
            input1 = self.arr[self.pos]
            input2 = self.arr[self.pos+1]
            outputPos = self.arr[self.pos+2]
            self.pos += 3

            self.arr[outputPos] = arg(1, input1) * arg(2, input2)
        
        elif op == Opcode.input:
            outputPos = self.arr[self.pos]
            self.pos += 1

            self.arr[outputPos] = self.__getInput()

        elif op == Opcode.output:
            input1 = self.arr[self.pos]
            self.pos += 1

            value = arg(1, input1)
            self.__putOutput(value)

        elif op == Opcode.jump_if_true:
            input1 = self.arr[self.pos]
            location = self.arr[self.pos+1]
            self.pos += 2

            if arg(1, input1) != 0:
                self.pos = arg(2, location)

        elif op == Opcode.jump_if_false:
            input1 = self.arr[self.pos]
            location = self.arr[self.pos+1]
            self.pos += 2

            if arg(1, input1) == 0:
                self.pos = arg(2, location)

        elif op == Opcode.less_than:
            a = self.arr[self.pos]
            b = self.arr[self.pos+1]
            outputPos = self.arr[self.pos+2]
            self.pos += 3

            self.arr[outputPos] = 1 if arg(1, a) < arg(2, b) else 0

        elif op == Opcode.equals:
            a = self.arr[self.pos]
            b = self.arr[self.pos+1]
            outputPos = self.arr[self.pos+2]
            self.pos += 3

            self.arr[outputPos] = 1 if arg(1, a) == arg(2, b) else 0

        elif op == Opcode.end:
            self.finished = True
        else:
            raise ValueError("unknown opcode: " + op)

class TestQ2(unittest.TestCase):
    """ tests from Advent Calendar question 2 """
    def test_basic(self):
        tests = [
            ([1,0,0,3,99], [1,0,0,2,99], 'first example'),
            ([1,0,0,0,99], [2,0,0,0,99], '1 + 1 = 2'),
            ([2,3,0,3,99], [2,3,0,6,99], '3 * 2 = 6'),
            ([2,4,4,5,99,0], [2,4,4,5,99,9801], '99 * 99 = 9801'),
            ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99], 'self-modifying code'),
        ]

        for test in tests:
            inputCode, expected, message = test
            i = IntcodeSim(inputCode).run()
            self.assertEqual( i.arr, expected,
                f"{inputCode}{'(' + message + ')' if message else ''}" )

    def test_basic2(self):
        i = IntcodeSim("1,9,10,3,2,3,11,0,99,30,40,50").run()
        self.assertEqual(i.arr, [3500,9,10,70,2,3,11,0,99,30,40,50])

    def test_puzzle_part1(self):
        i = IntcodeSim.fromFile("q2_input")
        i.arr[1] = 12
        i.arr[2] = 2
        i.run()
        self.assertEqual(i.arr[0], 2782414)

    def test_puzzle_part2(self):
        i = IntcodeSim.fromFile("q2_input")
        i.arr[1] = 98
        i.arr[2] = 20
        i.run()
        self.assertEqual(i.arr[0], 19690720)

class TestQ5(unittest.TestCase):
    """ tests from Advent Calendar question 4 """
    def test_param_modes(self):
        # 1002 = 02 (multiplication) with arg 0 in position mode, arg 1 in intermediate
        i = IntcodeSim("1002,4,3,4,33").run()
        self.assertEqual(i.arr[4], 99)

    def test_puzzle_part1(self):
        i = IntcodeSim.fromFile("q5_input").queueInput(1).run()
        self.assertEqual(i.outputs[-1], 7692125, 'correct diagnostic code')
        self.assertTrue(all(x == 0 for x in i.outputs[1:-2]), 'all other outputs are 0')

    def test_jump_positional(self):
        for number in range(-10,10):
            i = IntcodeSim("3,9,8,9,10,9,4,9,99,-1,8")
            i.queueInput(number).run()
            self.assertEqual(i.outputs, [1 if number == 8 else 0])
        for number in range(-10,10):
            i = IntcodeSim("3,9,7,9,10,9,4,9,99,-1,8")
            i.queueInput(number).run()
            self.assertEqual(i.outputs, [1 if number < 8 else 0])
        for number in range(-10,10):
            i = IntcodeSim("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
            i.queueInput(number).run()
            self.assertEqual(i.outputs, [0 if number == 0 else 1])

    def test_jump_immediate(self):
        for number in range(-10,10):
            i = IntcodeSim("3,3,1108,-1,8,3,4,3,99")
            i.queueInput(number)
            i.run()
            self.assertEqual(i.outputs, [1 if number == 8 else 0])
        for number in range(-10,10):
            i = IntcodeSim("3,3,1107,-1,8,3,4,3,99")
            i.queueInput(number)
            i.run()
            self.assertEqual(i.outputs, [1 if number < 8 else 0])
        for number in range(-10,10):
            i = IntcodeSim("3,3,1105,-1,9,1101,0,0,12,4,12,99,1")
            i.queueInput(number)
            i.run()
            self.assertEqual(i.outputs, [0 if number == 0 else 1])

    def test_comparator(self):
        code = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
        def run(inputNumber):
            i = IntcodeSim(code)
            i.queueInput(inputNumber)
            i.run()
            return i.outputs[0]
        self.assertEqual(run(7), 999)
        self.assertEqual(run(8), 1000)
        self.assertEqual(run(9), 1001)

    def test_puzzle_part2(self):
        i = IntcodeSim.fromFile("q5_input")
        i.queueInput(5)
        i.run()
        self.assertEqual(i.outputs, [14340395])
