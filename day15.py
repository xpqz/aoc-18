from astar import astar
from dataclasses import dataclass
from typing import Tuple


def read_data(filename="data/input15.data"):
    with open(filename) as f:
        return [list(line) for line in f.read().splitlines()]


@dataclass
class Goblin:
    pos: Tuple[int, int]

    def __repr__(self):
        return f"<Goblin pos:{self.pos}>"

    def __str__(self):
        return "G"


@dataclass
class Elf:
    pos: Tuple[int, int]

    def __repr__(self):
        return f"<Elf pos:{self.pos}>"

    def __str__(self):
        return "E"


def neighbours(coord):
    return [
        (coord[0] - 1, coord[1]),  # E
        (coord[0] + 1, coord[1]),  # W
        (coord[0], coord[1] - 1),  # N
        (coord[0], coord[1] + 1),  # S
    ]


class Cave:
    def __init__(self, data, adjacency, elves, goblins, dim):
        self.data = data
        self.adjacency = adjacency
        self.elves = elves
        self.goblins = goblins
        self.dim = dim

    def at(self, coord):
        if coord in self.elves:
            return self.elves[coord]

        if coord in self.goblins:
            return self.goblins[coord]

        if self.data.get(coord, False):
            return "."
        return "#"

    def in_range(self, targets):
        """
        Find all open squares adjacent to an enemy.
        """
        return [
            coord
            for pos in targets.keys()
            for coord in neighbours(pos)
            if self.at(coord) == "."
        ]

    def shortest_path(self, src, dest, visited=[], distances={}, predecessors={}):
        """
        Dijkstra's shortest path algorithm
        http://www.gilles-bertrand.com/2014/03/dijkstra-algorithm-python-example-source-code-shortest-path.html
        """

        if src == dest:
            path = []
            pred = dest
            while pred is not None:
                path.append(pred)
                pred = predecessors.get(pred, None)

            return path

        if not visited:
            distances[src] = 0

        for neighbor in self.adjacency[src]:
            if neighbor not in visited:
                # make left and up costlier?
                new_distance = distances[src] + 1
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = src

        visited.append(src)
        unvisited = {}
        for k in self.adjacency:
            if k not in visited:
                unvisited[k] = distances.get(k, float('inf'))
        x = min(unvisited, key=unvisited.get)

        return self.shortest_path(x, dest, visited, distances, predecessors)

    @classmethod
    def from_data(cls, lines):
        data, elves, goblins = {}, {}, {}
        for y, row in enumerate(lines):
            for x, item in enumerate(row):
                if item == "#":
                    continue
                coord = (x, y)
                data[coord] = True
                if item == "G":
                    goblins[coord] = Goblin(pos=coord)
                elif item == "E":
                    elves[coord] = Elf(pos=coord)

        # build adjacency graph
        graph = {
            coord: {n for n in neighbours(coord) if n in data}
            for coord in data.keys()
        }

        return cls(data, graph, elves, goblins, (x+1, y+1))

    def display(self):
        for r in self.to_str():
            print(''.join(r))

    def to_str(self):
        return [
            [
                str(self.at((x, y)))
                for x in range(self.dim[0])
            ]
            for y in range(self.dim[1])
        ]

    def to_maze(self):
        """
        Show squares only as 0 (empty) or 1 (non-empty)
        """
        return [
            [
                0 if self.at((x, y)) == "." else 1
                for x in range(self.dim[0])
            ]
            for y in range(self.dim[1])
        ]

    def overlay(self, coords, ch):
        s = self.to_str()
        for x, y in coords:
            s[y][x] = ch
        return s


if __name__ == "__main__":
    lines = read_data()

    cave = Cave.from_data(lines)

    path = cave.shortest_path((4, 10), (21, 14))

    for r in cave.overlay(path, "+"):
        print(''.join(r))
