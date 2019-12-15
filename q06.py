from collections import defaultdict
from copy import deepcopy
from util import path_find
import math

def loadOrbits(filename):
    """ load orbits from text file """
    graph = defaultdict(set)

    for line in open(filename, 'r'):
        line = line.rstrip('\n')
        orbitee, orbiter = line.split(')')
        graph[orbitee].add(orbiter)

    return graph

def countOrbits(graph, node='COM', depth=0):
    """ return the number of direct and indirect orbits starting at node """
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

def part1():
    print(totalOrbits(loadOrbits("q6_input")))

def makeBidirectional(graph):
    """ convert a unidirectional graph to a bidirectional by adding B->A
        for every edge A->B in the graph """
    new = deepcopy(graph)
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

    return path_find(start, goal, neighbourFunc)

def minimumTransfersRequired(graph):
    route = findRoute(graph)
    # This looks like: YOU -> A -> B -> C -> SAN
    # This is two transfers (A->B, B->C)  so we need to remove 3 from the total
    return len(route) - 3

graph = loadOrbits("inputs/q06")
print(minimumTransfersRequired(graph))
