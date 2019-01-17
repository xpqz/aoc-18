"""
day 17 of Advent of Code 2018
by Stefan Kruger
"""
import re

def read_data(filename="data/input17.data"):
    with open(filename) as f:
        return f.read().splitlines()

class UniqueStack:
    def __init__(self):
        self.stack = []
        self.seen = set()

    def append(self, item):
        if item not in self.seen:
            self.stack.append(item)
            self.seen.add(item)

    def pop(self):
        return self.stack.pop()

    def empty(self):
        return self.stack == []

class Cave:
    def __init__(self, clay, xdim, ydim):
        self.clay = clay
        self.xdim = xdim
        self.ydim = ydim
        self.settled = set()
        self.wet_sand = set()

    @classmethod
    def from_data(cls, lines):
        """
        Lines hold a fixed coordinate, x or y, and a range for the other, e.g:

        x=413, y=1421..1439
        y=1610, x=208..228
        """
        clay = set()
        for line in lines:
            coords = [int(n) for n in re.findall(r"-?\d+", line)]
            if line.startswith("x"):
                clay.update({(coords[0], y) for y in range(coords[1], coords[2] + 1)})
            else:
                clay.update({(x, coords[0]) for x in range(coords[1], coords[2] + 1)})

        xdim = (min(clay, key=lambda c: c[0])[0]-1,  max(clay, key=lambda c: c[0])[0] + 1)
        ydim = (min(clay, key=lambda c: c[1])[1],  max(clay, key=lambda c: c[1])[1] + 1)

        return cls(clay, xdim, ydim)

    def at(self, x, y):
        pos = (x, y)
        if pos == (500, 0):
            return "+"

        if pos in self.wet_sand:
            return "|"
        
        if pos in self.settled:
            return "~"

        if pos in self.clay:
            return "#" 

        return "."
        
    def neighbours(self, x, y):
        n = {}
        if y > self.ydim[1]:
            return n

        if x > self.xdim[0]:
            n['left'] = (x-1, y)

        if x < self.xdim[1]:
            n['right'] = (x+1, y)

        if y < self.ydim[1]:
            n['down'] = (x, y+1)

        return n

    def settle_from_wall_at(self, pos, heading):
        # Wall at pos, hit whilst travelling "heading". Move in oppsite direction
        # until we hit a wall or a ".". If a wall, can flip segment
        segment = set()
        delta = 1 if heading == "left" else -1  # opposite direction
        n = (pos[0]+delta, pos[1])
        while self.at(*n) == "|":
            segment.add(n)
            n = (n[0]+delta, n[1])

        if self.at(*n) == "#":
            self.settled.update(segment)
            self.wet_sand = self.wet_sand.difference(self.settled)
        
    def fill(self, start, iteration=0): # should start one below the spout
        """
        State machine, with state being the direction of travel.
        """
        stack = UniqueStack()
        stack.append((start, 'down'))

        while not stack.empty():
            (pos, heading) = stack.pop()
            
            # Stop at the edge
            if pos[1] >= self.ydim[1]:
                continue
            
            # What is at pos?
            here = self.at(*pos)
            adj = self.neighbours(*pos)

            if here == ".":
                self.wet_sand.add(pos)

                # If we're moving sidewards and we come to a "." we may
                # need to change to downwards if the space _below_ is also "."
                if heading in {"left", "right"}:
                    if "down" in adj and self.at(*adj["down"]) == ".":
                        stack.append((adj["down"], "down"))
                        continue

                # Ok, just carry on in the direction of travel
                try:
                    stack.append((adj[heading], heading))
                except KeyError:
                    pass
                continue

            if here in {"#", "~"}:
                if heading == "down":
                    # Hit a wall/standing water whilst moving downwards. Need to 
                    # check left and right nodes of my _previous_ location.
                    parent_adj = self.neighbours(pos[0], pos[1]-1)
                    try:
                        stack.append((parent_adj["left"], "left"))
                        stack.append((parent_adj["right"], "right"))
                    except KeyError:
                        pass
                    continue

                # Hit a wall left or right
                if here == "#":
                    self.settle_from_wall_at(pos, heading)
                continue

            if here == "|":
                # If we're moving sidewards and we come to a "|" we may
                # need to change to downwards if the space _below_ is "." or "|"
                if heading in {"left", "right"}:
                    if "down" in adj and self.at(*adj["down"]) in {".", "|"}:
                        stack.append((adj["down"], "down"))
                        continue

                # Ok, just carry on in the direction of travel
                try:
                    stack.append((adj[heading], heading))
                except KeyError:
                    pass
            

if __name__ == "__main__":
    lines = read_data()
    c = Cave.from_data(lines)

    i = 0
    while i < 819:
        c.fill((500, 1))
        i += 1

    s = 0
    for pos in c.wet_sand.union(c.settled):
        if pos[1] in range(c.ydim[0], c.ydim[1]+1):
            s += 1

    print(f"Part1: {s}")
    print(f"Part2: {len(c.settled)}")