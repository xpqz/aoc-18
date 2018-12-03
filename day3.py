from dataclasses import dataclass
from typing import Tuple
import re


@dataclass
class Claim:
    id: str
    origin: Tuple[int, int]
    size: Tuple[int, int]


class Fabric:
    def __init__(self):
        self.w, self.h = 1000, 1000
        self.fabric = [[0 for x in range(self.w)] for y in range(self.h)]

    def apply(self, claim):
        for y in range(claim.origin[1], claim.origin[1] + claim.size[1]):
            for x in range(claim.origin[0], claim.origin[0] + claim.size[0]):
                self.fabric[y][x] += 1

    def disputed(self):
        shared = 0
        for y in range(0, len(self.fabric)):
            for x in range(0, len(self.fabric[y])):
                if self.fabric[y][x] > 1:
                    shared += 1

        return shared

    def is_undisputed(self, claim):
        for y in range(claim.origin[1], claim.origin[1] + claim.size[1]):
            for x in range(claim.origin[0], claim.origin[0] + claim.size[0]):
                if self.fabric[y][x] != 1:
                    return False

        return True


def read_data(filename="input3.data"):
    with open(filename) as f:
        lines = f.read().splitlines()

    return lines


def parse_data(lines):
    """
    A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a
    rectangle 3 inches from the left edge, 2 inches from the top edge,
    5 inches wide, and 4 inches tall.

    # 11 @ 49,318: 25x25
    """
    patt = re.compile(r"^(#\s*\d+)\s+@\s+(\d+),(\d+):\s+(\d+)x(\d+)")
    result = []
    for line in lines:
        m = patt.match(line)
        if m:
            result.append(Claim(
                id=m.group(1),
                origin=(int(m.group(2)), int(m.group(3))),
                size=(int(m.group(4)), int(m.group(5)))
            ))

    return result


def part1(fabric, claims):

    for claim in claims:
        fabric.apply(claim)

    return fabric.disputed()


def part2(fabric, claims):
    for claim in claims:
        if fabric.is_undisputed(claim):
            return claim

    return None


if __name__ == "__main__":
    claims = parse_data(read_data())
    fabric = Fabric()

    print(part1(fabric, claims))
    undisputed = part2(fabric, claims)

    if undisputed:
        print(undisputed.id)
