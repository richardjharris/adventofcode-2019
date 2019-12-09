from enum import Enum
import copy
import unittest
from dataclasses import dataclass

@dataclass
class Op:
    """
    Holds metadata for an operation.

    :param args: Number of arguments operator accepts
    :param posArgs: Out of the above, the number of arguments that
                    are positions (for writing output)
    """
    args: int = 0
    posArgs: int = 0

    def inputs(self):
        """
        Returns the number of input arguments.
        """
        return self.args - self.posArgs

class Opcode(int, Enum):
    """
    Represents an Opcode: an integer, name and metadata.
    """

    # Map each opcode name to its opcode int and metadata
    ADD             = (1,  Op(args=3, posArgs=1)),
    MULTIPLY        = (2,  Op(args=3, posArgs=1)),
    INPUT           = (3,  Op(args=1, posArgs=1)),
    OUTPUT          = (4,  Op(args=1)),
    JUMP_IF_TRUE    = (5,  Op(args=2)),
    JUMP_IF_FALSE   = (6,  Op(args=2)),
    LESS_THAN       = (7,  Op(args=3, posArgs=1)),
    EQUALS          = (8,  Op(args=3, posArgs=1)),
    END             = (99, Op()),

    def __new__(cls, arg):
        code, op = arg
        obj = int.__new__(cls, code)
        obj._value_ = code
        obj.op = op
        return obj

class ParameterMode(Enum):
    """
    Represents a parameter mode: how a parameter should be interpreted.

    POSITION: parameter is an address
    IMMEDIATE: parameter is an integer value
    """

    POSITION = 0
    IMMEDIATE = 1

class IntcodeSim:
    """
    Parses and executes Intcode.
    """

    def __init__(self, code):
        """
        Create an IntcodeSim executor. Each executor can only be run
        once, and allows introspection of outputs and the memory state.

        :param code: intcode, as a list of ints or a comma-separated string.
        :attribute arr: The current intcode state. This may be modified as the code
                        is executed.
        :attribute pos: The instruction pointer: position of next intcode to execute
        :attribute finished: Boolean, true if the intcode has finished executing
        :attribute queuedInputs: List of inputs to use if requested by intcode
                                 (lower indexes are used first)
        :attribute outputs: List of outputs emitted by the intcode, earliest first.
        :attribute inputFn: If set, inputs will be retrieved by calling this function,
                            which should return an integer. (If queuedInputs is non-empty,
                            values will be pulled from there first)
        :attribute outputFn: If set, will be called with a single integer argument for
                             for each output value. Values will also be added to 'outputs'
        """

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
        self.inputFn = None
        self.outputFn = None

    def queueInput(self, value):
        """
        Queues an input value, which will be used (FIFO) when the intcode
        program requests an input. If the queue is empty, the executor will
        prompt the user on STDIN instead.

        :param value: Value to enqueue
        :return: Returns self, for chaining.
        """
        self.queuedInputs.append(value)
        return self

    def __getInput(self):
        if len(self.queuedInputs):
            return self.queuedInputs.pop(0)
        elif self.inputFn is not None:
            return self.inputFn()
        else:
            value = input('Enter value: ')
            return int(value)

    def __putOutput(self, value):
        self.outputs.append(value)
        if self.outputFn is not None:
            self.outputFn(value)

    @classmethod
    def fromFile(cls, filename):
        """
        Creates an IntcodeSim with intcode loaded from the specified file.

        :param filename: The file to load.
        """
        arr = []
        with open(filename, 'r') as f:
            for line in f:
                arr += cls.split(line.rstrip('\n'))
        return cls(arr)
    
    @staticmethod
    def split(string):
        """ 
        Converts CSV intcode to a list of integers.
        """
        return list([int(x) for x in string.split(',')])

    @staticmethod
    def parseOpcode(fullOpcode):
        """
        Parses a full opcode, such as 1102, returning an Opcode object
        representing the operation, and a list of ParameterModes representing
        the parameter mode for each argument.

        :param fullOpcode: The integer opcode to parse
        :return: tuple of opcode, parameterModes
        """
        opcode = Opcode(fullOpcode % 100)
        fullOpcode //= 100

        parameterModes = []
        for v in range(0, opcode.op.inputs()):
            parameterModes.append(ParameterMode(fullOpcode % 10))
            fullOpcode //= 10

        return opcode, parameterModes

    def run(self):
        """
        Execute the intcode until the program finishes.

        :return: Self, for chaining
        """
        while not self.finished:
            self.__runStep()
        return self
    
    def __runStep(self):
        # Execute a single instruction.
        if self.finished:
            return

        opcode, parameterModes = self.parseOpcode(self.arr[self.pos])
        self.pos += 1

        # Build arguments
        args = []
        for i in range(0, opcode.op.args):
            value = self.arr[self.pos]
            self.pos += 1

            # posArgs are always treated as immediate
            if i < opcode.op.inputs() and \
                parameterModes[i] == ParameterMode.POSITION:
                args.append( self.arr[value] )
            else:
                args.append( value )

        # Execute opcode
        if opcode == Opcode.ADD:
            self.arr[args[2]] = args[0] + args[1]

        elif opcode == Opcode.MULTIPLY:
            self.arr[args[2]] = args[0] * args[1]
        
        elif opcode == Opcode.INPUT:
            self.arr[args[0]] = self.__getInput()

        elif opcode == Opcode.OUTPUT:
            self.__putOutput(args[0])

        elif opcode == Opcode.JUMP_IF_TRUE:
            if args[0] != 0:
                self.pos = args[1]

        elif opcode == Opcode.JUMP_IF_FALSE:
            if args[0] == 0:
                self.pos = args[1]

        elif opcode == Opcode.LESS_THAN:
            self.arr[args[2]] = 1 if args[0] < args[1] else 0

        elif opcode == Opcode.EQUALS:
            self.arr[args[2]] = 1 if args[0] == args[1] else 0

        elif opcode == Opcode.END:
            self.finished = True
        else:
            raise ValueError("unknown opcode: " + opcode)

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

class TestQ7(unittest.TestCase):
    def test_input_output_fn(self):
        tests = [
            {"input": 8, "output": 1},
            {"input": 7, "output": 0},
        ]
        for test in tests:
            i = IntcodeSim("3,3,1108,-1,8,3,4,3,99")
            i.inputFn = lambda: test["input"]
            def capture(value):
                capture.output = value
            i.outputFn = capture
            i.run()
            self.assertEqual(capture.output, test["output"], str(test["input"]))
