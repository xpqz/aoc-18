"""
day 18 of Advent of Code 2018
by Stefan Kruger
"""
import re
from collections import Counter

OPEN = "."
LUMBER = "#"
TREE = "|"

def read_data(filename="data/input18.data"):
    with open(filename) as f:
        return f.read().splitlines()

class Forest:
    def __init__(self, data):
        self.data = data
        self.counter = None
        
    
    @classmethod
    def from_data(cls, lines):
        return cls([list(line) for line in lines])

    def display(self):
        for y in self.data:
            print("".join(y))

    def evolve(self, x, y):
        """
        Return new state at (x, y)
        """
        neighbours = Counter()
        for yy in [-1, 0, 1]:
            ypos = y+yy
            if ypos < 0: 
                continue

            for xx in [-1, 0, 1]:
                xpos = x+xx
                if xpos < 0 or (xx == 0 and yy == 0):
                    continue

                try:
                    item = self.data[ypos][xpos]
                except IndexError:
                    continue

                neighbours[item] += 1


        if self.data[y][x] == OPEN and neighbours[TREE] >= 3:
            return TREE

        if self.data[y][x] == TREE and neighbours[LUMBER] >= 3:
            return LUMBER

        if self.data[y][x] == LUMBER and neighbours[LUMBER] >= 1 and neighbours[TREE] >= 1:
            return LUMBER

        if self.data[y][x] == LUMBER:
            return OPEN

        return self.data[y][x]

    def generate(self):

        d = [["."]*len(self.data) for _ in range(len(self.data))]
        c = Counter()
        for y, row in enumerate(self.data):
            for x, _ in enumerate(row):
                d[y][x] = self.evolve(x, y)
                c[d[y][x]] += 1

        self.data = d
        self.counter = c
 

if __name__ == "__main__":
    lines = read_data()

    forest = Forest.from_data(lines)

    for i in range(1, 11):
        forest.generate()

    print(f"Part1: {forest.counter[TREE] * forest.counter[LUMBER]}")

    # Part 2, what's the value after a beeeeellioooon iterations?
    # 
    # Too large to actually run, but all "game of life"-style cellular
    # automata fall into certain patterns, especially as this one is
    # constrained to a 50x50 grid.
    # 
    # We can assume that it will either converge to a stable state, or 
    # become periodic.
    #
    # By just letting this run and looking at the visualisation, it's 
    # clear that it very quickly becomes periodic (period 28). The value 
    # at 1_000_000_000 generations should be the same as the value at 1_000.

    forest = Forest.from_data(lines)
    for i in range(1, 1_001):
        forest.generate()

    print(f"Part2: {forest.counter[TREE] * forest.counter[LUMBER]}")


