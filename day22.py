"""
day 22 of Advent of Code 2018
by Stefan Kruger
"""
from functools import lru_cache
import heapq
import math

def erosion_level(t, depth):
    return (t + depth) % 20183

def geo_index(pos, target, depth):
    vals = {(0, 0): 0, target: 0}
    for y in range(0, pos[1]+1):
        for x in range(0, pos[0]+1):
            this = (x, y)
            if this == target:
                continue
            if this[1] == 0:
                vals[this] = this[0] * 16807
            elif this[0] == 0:
                vals[this] = this[1] * 48271
            else:
                vals[this] = (
                    (vals[(this[0]-1, this[1])] + depth) % 20183 *
                    (vals[(this[0], this[1]-1)] + depth) % 20183
                )

    return vals[pos]

@lru_cache(None)
def region(x, y, target, depth):
    gi = geo_index((x, y), target, depth)
    return erosion_level(gi, depth) % 3

def neighbours(x, y, tool, target, depth):
    """
    Return valid neighbours with cost, given hefted tool
    """
    for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        xpos = x+delta[0]
        ypos = y+delta[1]
        if xpos < 0 or ypos < 0:
            continue
        region_tool = region(xpos, ypos, target, depth)
        for new_tool in range(3):
            if region_tool != new_tool:
                cost = 8 if tool != new_tool else 1
                yield xpos, ypos, new_tool, cost

if __name__ == "__main__":

    depth = 10689
    target = (11, 722)

    risk = 0
    for y in range(0, target[1]+1):
        for x in range(0, target[0]+1):
            if (x, y) in {(0, 0), target}:
                continue
            risk += region(x, y, target, depth)

    print(f"Part1: {risk}")

    # Part 2: a breadth-first search, with the tooling constraints.
    # Relying on tool == region type == risk.

    target_tool = (target[0], target[1], 1)

    # (time, xpos, ypos, tool)
    frontier = [(0, 0, 0, 1)]
    result = {(0, 0, 1): 0}
    while frontier:
        (t, x, y, tool) = heapq.heappop(frontier)
        current = (x, y, tool)
        if current == target_tool:
            print(f"Part2: {t-1}")
            break

        if result.get(current, math.inf) < t:
            continue

        # As the graph is 'unlimited', we need a heuristic cut-off
        if x > target[0] * 2 or y > target[1] * 2:
            continue

        for xpos, ypos, new_tool, cost in neighbours(x, y, tool, target, depth):
            if t+cost < result.get((xpos, ypos, new_tool), math.inf):
                result[(xpos, ypos, new_tool)] = t+cost
                heapq.heappush(frontier, (t+cost, xpos, ypos, new_tool))
