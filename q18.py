import grid
import sys
from collections import defaultdict

"""
Only one entrance (marked @) is present among the open passages (marked .) and stone walls (#),
but you also detect an assortment of keys (shown as lowercase letters) and doors (shown as
uppercase letters). Keys of a given letter open the door of the same letter: a opens A, b opens
B, and so on. You aren't sure which key you need to disable the tractor beam, so you'll need
to collect all of them.

OBJECTIVE: find all keys
"""

sys.setrecursionlimit(2000)

def main():
    g = grid.from_docstring("""
        ########################
        #...............b.C.D.f#
        #.######################
        #.....@.a.B.c.d.A.e.F.g#
        ########################
    """)
    grid.set_collision('#', True)

    points = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@"
    for point in points:
        start = g.find(point)
        if start is None:
            continue
        walk_grid(grid, pos=start)

    # We need to try each combination of a-z in order. To help select:
    # - eliminate routes that don't exist (set contains a door we don't
    #   have the key for
    # - otherwise try all of them.

def walk_grid(grid, pos, routes=None, came_from=None):
    """
    Returns a route distance index.
    This maps each start location (@ or a key) to a end location (key)
    with distance, 

    Exploits the fact the map is effectively a tree with no loops or
    open areas of width > 1 (so we don't need to 'path find').

    (start,dest) -> (distance, keys/doors)
    """

    if routes is None:
        routes = defaultdict(defaultdict)

    for neighbour, direction in pos.neighbours(exclude=came_from):
        square = neighbour.value
        if 'a' <= square <= 'z':
            pass
        elif 'A' <= square <= 'Z':
            pass

        # Recurse
        walk_grid(grid,
            pos=neighbour,
            routes=routes,
            came_from=direction.reverse())
    
    return routes

main()
