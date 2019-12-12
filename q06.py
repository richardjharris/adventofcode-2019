from collections import defaultdict
from copy import deepcopy
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

    def reconstructPath(cameFrom, current):
        totalPath = [ current ]
        while current in cameFrom:
            current = cameFrom[current]
            totalPath.insert(0, current)
        return totalPath

    # Construct a bidirectional graph, as we can go to any object orbiting OR
    # being orbited by our current object.
    neighboursOf = makeBidirectional(graph)

    # Heuristic function. Currently 0 (equivalent to Dijkstra)
    h = lambda x: 0

    # Set of discovered nodes
    openSet = { start }

    # For node n, cameFrom[n] is the node immediately preceding it on the
    # cheapest path from start to n currently known
    cameFrom = {}

    # For node n, gScore[n] is the cost of the cheapest path from start to n
    # currently known
    gScore = defaultdict(lambda: math.inf)
    gScore[start] = 0

    # For node n, fScore[n] = gScore[n] + h(n)
    fScore = defaultdict(lambda: math.inf)
    fScore[start] = h(start)

    while len(openSet) > 0:
        current = min(openSet, key=lambda x: fScore[x])
        if current == goal:
            return reconstructPath(cameFrom, current)

        openSet.remove(current)
        for neighbour in neighboursOf[current]:
            # weights of the edges are all 0 in this case
            tentative_gScore = gScore[current] + 0
            if tentative_gScore < gScore[neighbour]:
                # This path to the neighbour is better than the previous one
                cameFrom[neighbour] = current
                gScore[neighbour] = tentative_gScore
                fScore[neighbour] = gScore[neighbour] + h(neighbour)
                if neighbour not in openSet:
                    openSet.add(neighbour)

    # openset is empty, but goal never reached?
    return None

def minimumTransfersRequired(graph):
    route = findRoute(graph)
    # This looks like: YOU -> A -> B -> C -> SAN
    # This is two transfers (A->B, B->C)  so we need to remove 3 from the total
    return len(route) - 3

graph = loadOrbits("inputs/q06")
print(minimumTransfersRequired(graph))
