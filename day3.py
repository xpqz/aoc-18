"""
day 3 of Advent of Code 2018
by Stefan Kruger
"""
from dataclasses import dataclass
from typing import Tuple
import re


@dataclass
class Claim:
    id: str
    origin: Tuple[int, int]
    size: Tuple[int, int]


class Fabric:
    """
    Sparse matrix representing an 'infinite' roll of fabric.
    """

    def __init__(self):
        self.fabric = {}

    def reserve(self, claim):
        """
        Reserve a square claim. The value of each point is the number of
        simultaneous claims at that point.
        """
        for y in range(claim.origin[1], claim.origin[1] + claim.size[1]):
            for x in range(claim.origin[0], claim.origin[0] + claim.size[0]):
                if self.fabric.get((x, y), 0) == 0:
                    self.fabric[(x, y)] = 1
                else:
                    self.fabric[(x, y)] += 1

    def disputed(self):
        """
        Return the number of points that are subject to more than one claim.
        """
        shared = 0
        for value in self.fabric.values():
            if value > 1:
                shared += 1

        return shared

    def is_undisputed(self, claim):
        """
        Return True if the claim is completely undisputed.
        """
        for y in range(claim.origin[1], claim.origin[1] + claim.size[1]):
            for x in range(claim.origin[0], claim.origin[0] + claim.size[0]):
                if self.fabric.get((x, y), 0) != 1:
                    return False

        return True


def read_data(filename="input3.data"):
    """
    Load the raw datafile
    """
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
    """
    Part1: return the total number of disputed points.
    """
    for claim in claims:
        fabric.reserve(claim)

    return fabric.disputed()


def part2(fabric, claims):
    """
    Return any undisputed claims.
    """
    return [claim for claim in claims if fabric.is_undisputed(claim)]


if __name__ == "__main__":
    claims = parse_data(read_data())
    fabric = Fabric()

    print(part1(fabric, claims))
    for undisputed in part2(fabric, claims):
        print(undisputed.id)
