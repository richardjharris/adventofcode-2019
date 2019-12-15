'Day 6 - Universal Orbit Map'
import collections
import copy
import math
import unittest
import util

def loadOrbits(filename):
    """ load orbits from text file """
    graph = collections.defaultdict(set)

    with open(filename, 'r') as fh:
        for line in fh:
            line = line.rstrip('\n')
            orbitee, orbiter = line.split(')')
            graph[orbitee].add(orbiter)

    return graph


def countOrbits(graph, node='COM', depth=0):
    """ return the number of direct and indirect orbits starting at node """
    graph = collections.defaultdict(set, graph)

    direct, indirect = 0, 0

    for orbiter in graph[node]:
        direct += 1
        indirect += depth

        subDirect, subIndirect = countOrbits(graph, node=orbiter, depth=depth + 1)
        direct += subDirect
        indirect += subIndirect

    return direct, indirect


def totalOrbits(graph):
    """ return the total number of orbits in the graph """
    direct, indirect = countOrbits(graph)
    return direct + indirect


def makeBidirectional(graph):
    """ convert a unidirectional graph to a bidirectional by adding B->A
        for every edge A->B in the graph """
    new = collections.defaultdict(set, copy.deepcopy(graph))
    for fromNode, toNodes in graph.items():
        for toNode in toNodes:
            new[toNode].add(fromNode)
    return new


def findRoute(graph, start='YOU', goal='SAN'):
    """ find minimal route from start to goal along graph """

    # Construct a bidirectional graph, as we can go to any object orbiting OR
    # being orbited by our current object.
    neighboursOf = makeBidirectional(graph)
    def neighbourFunc(node):
        return neighboursOf[node]

    return util.path_find(start, goal, neighbourFunc)


def minimumTransfersRequired(graph):
    route = findRoute(graph)
    # This looks like: YOU -> A -> B -> C -> SAN
    # This is two transfers (A->B, B->C)  so we need to remove 3 from the total
    return len(route) - 3


class TestQ6(unittest.TestCase):

    def test_count_basic(self):
        graph = {
            'COM': { 'BBB' },
        }
        self.assertEqual(totalOrbits(graph), 1)

        graph = {
            'COM': { 'BBB' },
            'BBB': { 'CCC' },
        }
        # AAA -> BBB, AAA -> CCC, BBB -> CCC
        self.assertEqual(totalOrbits(graph), 3)


    def test_count_example(self):
        graph = {
            'COM': { 'B' },
            'B': { 'C', 'G' },
            'C': { 'D' },
            'D': { 'E', 'I' },
            'E': { 'F', 'J' },
            'G': { 'H' },
            'J': { 'K' },
            'K': { 'L' },
        }
        self.assertEqual(totalOrbits(graph), 42)


    def test_part1(self):
        graph = loadOrbits("inputs/q06")
        self.assertEqual(totalOrbits(graph), 273985)


    def test_transfer_example(self):
        graph = {
            'COM': { 'B' },
            'B': { 'C', 'G' },
            'C': { 'D' },
            'D': { 'E', 'I' },
            'E': { 'F', 'J' },
            'G': { 'H' },
            'I': { 'SAN' },
            'J': { 'K' },
            'K': { 'L', 'YOU' },
        }
        self.assertEqual(minimumTransfersRequired(graph), 4)


    def test_part2(self):
        graph = loadOrbits("inputs/q06")
        self.assertEqual(minimumTransfersRequired(graph), 460)
        
