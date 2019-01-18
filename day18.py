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
        # if y==0 and x==6:
        #     import pdb
        #     pdb.set_trace()

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
        forest.display()
        print()

    print(forest.counter)


    