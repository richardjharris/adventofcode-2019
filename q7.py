import multiprocessing
import unittest
from itertools import permutations
from intcode import IntcodeSim

def part1():
    """
    Open the Q7 input and calculate the max signal in serial mode
    """
    code = open('q7_input', 'r').read().rstrip('\n')
    print(findMaxSignalPart1(code))

def part2():
    """
    Open the Q7 input and calculate the max signal in feedback mode
    """
    code = open('q7_input', 'r').read().rstrip('\n')
    print(findMaxSignalPart2(code))

def findMaxSignalPart1(code):
    return findMaxSignal(code, getSignal, range(0,5))

def findMaxSignalPart2(code):
    return findMaxSignal(code, getSignalWithFeedback, range(5,10))

def findMaxSignal(code, getSignalFn, allowedPhaseSettings):
    """ find the maximum signal for all permutations of phase settings """
    maxSignal = None
    maxSignalConfiguration = None
    for configuration in permutations(allowedPhaseSettings):
        signal = getSignalFn(code, configuration)
        if maxSignal is None or maxSignal < signal:
            maxSignal = signal
            maxSignalConfiguration = configuration

    return maxSignal, maxSignalConfiguration

def worker(code, inQueue, outQueue):
    """ amplifier worker function. accepts input from inQueue and sends output
        to outQueue """
    sim = IntcodeSim(code)
    sim.inputFn = inQueue.get
    sim.outputFn = outQueue.put
    sim.run()

def looperWorker(inQueue, outQueue, lastOutputValue):
    """ send inQueue to outQueue, tracking the last value received """
    while True:
        val = inQueue.get()
        lastOutputValue.value = val
        outQueue.put(val)

def getSignal(code, phaseSettings, feedback=False):
    """
    start 5 amplifiers running the controller software in series
    A -> B -> C -> D -> E

    Each amplifier first receives a phase setting (0..4) which can be used
    exactly once per amplifier.

    Then they receive the input signal (0 for A, the output of A for B)
    and so on until we receive a final output signal.

    In feedback mode, E's output is not accepted immediately as the final
    result, but rather sent to A as input until all amplifiers have halted.

    """
    threads = []
    queues = []

    # Create the input queue for the first worker, which this thread
    # will manage
    firstQueue = multiprocessing.Queue(maxsize=1)
    queues.append(firstQueue)

    for i in range(5):
        # Create a queue for passing input to the worker
        queue = multiprocessing.Queue(maxsize=1)
        queues.append(queue)

        # Pass the previous queue for input, and the newly-created queue for
        # output
        p = multiprocessing.Process(target=worker, args=(code,queues[i],queue))
        threads.append(p)
        p.start()

    # Send phase settings
    for i in range(5):
        queues[i].put(phaseSettings[i])

    # Send input value for first amplifier
    queues[0].put(0)

    if feedback:
        lastOutput = multiprocessing.Value('i', -1, lock=False)
        # Create a new thread to repeatedly retrieve input from the output queue
        # and pass it back onto the first amplifier
        looper = multiprocessing.Process(target=looperWorker, args=(queues[-1], queues[0], lastOutput))
        looper.start()

        for thread in threads:
            thread.join()
        
        looper.terminate()

        return lastOutput.value
    else :
        # Retrieve output value from last amplifier
        signal = queues[-1].get()

        # At this point all amplifiers should be finished, but let's be polite
        for thread in threads:
            thread.join()

        return signal

def getSignalWithFeedback(code, phaseSettings):
    return getSignal(code, phaseSettings, feedback=True)

class TestQ7Part1(unittest.TestCase):
    def test_one(self):
        signal, sequence = findMaxSignalPart1("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0")
        self.assertEqual(signal, 43210)
        self.assertEqual(sequence, (4,3,2,1,0))

    def test_two(self):
        signal, sequence = findMaxSignalPart1("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0")
        self.assertEqual(signal, 54321)
        self.assertEqual(sequence, (0,1,2,3,4))

    def test_three(self):
        signal, sequence = findMaxSignalPart1("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")
        self.assertEqual(signal, 65210)
        self.assertEqual(sequence, (1,0,4,3,2))

class TestQ7Part2(unittest.TestCase):
    def test_one(self):
        signal, sequence = findMaxSignalPart2("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
        self.assertEqual(signal, 139629729)
        self.assertEqual(sequence, (9,8,7,6,5))

    def test_two(self):
        signal, sequence = findMaxSignalPart2("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10")
        self.assertEqual(signal, 18216)
        self.assertEqual(sequence, (9,7,8,5,6))
