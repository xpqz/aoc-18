
"""
day 23 of Advent of Code 2018
by Stefan Kruger
"""

import re
import math
from dataclasses import dataclass
from typing import Tuple
from queue import PriorityQueue

@dataclass
class Bot:
    pos: Tuple[int, int, int]
    radius: int

    @classmethod
    def from_string(cls, s):
        data = list(map(int, re.findall(r"-?\d+", s)))
        return cls(tuple(data[:3]), data[3])

def read_data(filename="data/input23.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    strongest = None
    data = []
    for line in lines:
        b = Bot.from_string(line)
        if strongest is None or b.radius > strongest.radius:
            strongest = b
        data.append(b)

    return (strongest, data)

def manhattan_distance(a, b):
    distance = 0
    for i in range(len(a)):
        distance += abs(b[i]-a[i])

    return distance

if __name__ == "__main__":
    lines = read_data()
    (strongest, data) = parse_data(lines)

    reachable = 0
    for p in data:
        d = manhattan_distance(strongest, p)
        if d <= strongest.radius:
            reachable += 1

    print(f"Part1: {reachable}")

    # This isn't a general solution, but exploits the fact that the data
    # consists of massively overlapping bots.
    #
    # The elegance is blinding, but credit does not belong to me.
    #
    #  https://www.reddit.com/r/adventofcode/comments/a8s17l/2018_day_23_solutions/ecdqzdg/
    #
    # Consider a 1-D projection of the bots, and find the min and max distance
    # from the origin.
    #
    # Find the point that has the most overlaps.
    #
    q = PriorityQueue()
    for bot in data:
        d = abs(bot.pos[0]) + abs(bot.pos[1]) + abs(bot.pos[2])
        q.put((max(0, d - bot.radius), 1))
        q.put((d + bot.radius + 1, -1))

    count = 0
    max_count = 0
    result = 0
    while not q.empty():
        dist, e = q.get()
        count += e
        if count > max_count:
            result = dist
            max_count = count

    print(f"Part2: {result}")
