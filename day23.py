
import re
import math
from dataclasses import dataclass
from typing import Tuple

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
    assert len(a.pos) == len(b.pos)
    distance = 0
    for i in range(len(a.pos)):
        distance += abs(b.pos[i]-a.pos[i])

    return distance


if __name__ == "__main__":
    lines = read_data()
    (strongest, data) = parse_data(lines)

    print(strongest.pos, " ", strongest.radius)
    reachable = 0
    for p in data:
        d = manhattan_distance(strongest, p)
        if d <= strongest.radius:
            reachable += 1

    print(f"Part1: {reachable}")
