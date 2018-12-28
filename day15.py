from copy import copy
from dataclasses import dataclass
import math
from typing import Tuple


def read_data(filename="data/input15.data"):
    with open(filename) as f:
        return [list(line) for line in f.read().splitlines()]


@dataclass
class Goblin:
    pos: Tuple[int, int]
    hitpoints: int = 200
    attack: int = 3

    def __repr__(self):
        return f"<Goblin pos:{self.pos} hp:{self.hitpoints}>"

    def __str__(self):
        return "G"


@dataclass
class Elf:
    pos: Tuple[int, int]
    hitpoints: int = 200
    attack: int = 3

    def __repr__(self):
        return f"<Elf pos:{self.pos} hp:{self.hitpoints}>"

    def __str__(self):
        return "E"


def adj(coord):
    return [
        (coord[0] - 1, coord[1]),  # E
        (coord[0] + 1, coord[1]),  # W
        (coord[0], coord[1] - 1),  # N
        (coord[0], coord[1] + 1),  # S
    ]


class Cave:
    def __init__(self, adjacency, elves, goblins, dim):
        self.adjacency = adjacency
        self.elves = elves
        self.goblins = goblins
        self.dim = dim

    def at(self, coord):
        if coord in self.elves:
            return self.elves[coord]

        if coord in self.goblins:
            return self.goblins[coord]

        if coord in self.adjacency:
            return "."

        return "#"

    def in_range(self, targets):
        """
        Find all open squares adjacent to an enemy.
        """
        return sorted([
            coord
            for pos in targets.keys()
            for coord in self.available_moves(pos)
        ], key=lambda c: (c[1], c[0]))  # "read order", i.e. rows, then cols

    def attacking(self, targets):
        """
        List all team members currently in an attacking position.
        """
        own_team = self.goblins
        if targets == self.goblins:
            own_team = self.elves

        return [
            coord
            for pos in targets.keys()
            for coord in adj(pos)
            if coord in own_team
        ]

    def game_over(self):
        """
        Game is over if there are no attacking squares available, and no
        current attacks in progress.
        """
        if not self.goblins or not self.elves:
            return True

        for targets in [self.goblins, self.elves]:
            if self.in_range(targets) or self.attacking(targets):
                return False

        return True

    def available_moves(self, coord):
        return [
            n
            for n in adj(coord)
            if n in self.adjacency
            if n not in self.elves
            if n not in self.goblins
        ]

    def all_start_squares(self, prev, source, dest):
        """
        prev is an adjacency graph describing a set of paths from source to
        dest of equal lengths. Return a list of all possible starting moves,
        in row-col order.
        """
        check = {dest}
        start_squares = []
        while check:
            c = check.pop()
            try:
                for p in prev[c]:
                    if p == source:
                        start_squares.append(c)
                    else:
                        check.add(p)
            except KeyError:  # No uninpeded path; skip
                break

        return sorted(start_squares, key=lambda x: (x[1], x[0]))

    def multiple_shortest_path(self, source, dest):
        """
        https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        """
        Q = set(self.adjacency.keys())

        dist = {n: math.inf for n in Q}
        prev = {}

        dist[source] = 0

        while Q:
            nd = {l: dist[l] for l in Q}
            u = min(nd, key=nd.get)
            if u == dist:
                break
            Q.remove(u)
            for v in self.available_moves(u):
                alt = dist[u] + 1
                if alt <= dist[v]:
                    dist[v] = alt
                    if v not in prev:
                        prev[v] = set()
                    prev[v].add(u)

        # prev is now an adjacency graph describing all
        # shortest path alternatives between source and
        # dest. But we only care about the first step,
        # so find all edges out of the start node and
        # choose the one that's the "earliest" in row-col
        # order.

        start_options = self.all_start_squares(prev, source, dest)

        if start_options:
            square = start_options[0]
            return square, dist[dest]

        return None, None

    @classmethod
    def from_data(cls, lines):
        elves, goblins = {}, {}
        data = set()
        for y, row in enumerate(lines):
            for x, item in enumerate(row):
                if item == "#":
                    continue
                coord = (x, y)
                data.add(coord)
                if item == "G":
                    goblins[coord] = Goblin(pos=coord)
                elif item == "E":
                    elves[coord] = Elf(pos=coord)

        # build adjacency graph
        graph = {
            coord: {n for n in adj(coord) if n in data}
            for coord in data
        }

        return cls(graph, elves, goblins, (x+1, y+1))

    def display(self):
        for r in self.to_str():
            print(''.join(r))

    def to_str(self):
        return [
            [str(self.at((x, y))) for x in range(self.dim[0])]
            for y in range(self.dim[1])
        ]

    def overlay(self, coords, ch):
        s = self.to_str()
        for x, y in coords:
            s[y][x] = ch
        return s

    def move(self, start):
        """
        Move piece at start one step along the shortest path to an attackable
        position. If already in attacking position, piece won't move. Returns
        position after move (may be the start pos).
        """
        if start in self.elves:
            my_team = self.elves
            enemies = self.goblins
        elif start in self.goblins:
            my_team = self.goblins
            enemies = self.elves
        else:
            return start

        # If I'm in an attacking position, I can't move.
        for n in adj(start):
            if n in enemies:
                return start

        targets = self.in_range(enemies)

        if not targets:
            return start

        best = (math.inf, None)

        for target in targets:
            square, cost = self.multiple_shortest_path(start, target)
            if square and cost < best[0]:
                best = (cost, square)

        if best[1]:
            next_square = best[1]
            piece = my_team.pop(start)
            piece.pos = next_square
            my_team[next_square] = piece
            return next_square

        return start

    def attack(self, pos):
        """
        If pos is in an attacking position, execute the attack. Return True if
        an attack was made, False if not.
        """
        if pos in self.elves:
            my_team = self.elves
            enemies = self.goblins
        elif pos in self.goblins:
            my_team = self.goblins
            enemies = self.elves
        else:
            return False

        # Find any attackable neighbours, ordered by hitpoints in reading order
        attackable = sorted(
            [enemies[n] for n in adj(pos) if n in enemies],
            key=lambda x: (x.hitpoints, x.pos[1], x.pos[0])
        )

        perpetrator = my_team[pos]
        if attackable:
            victim = attackable[0]
            victim.hitpoints -= perpetrator.attack

            if victim.hitpoints <= 0:
                enemies.pop(victim.pos)

            return True

        return False

    def pieces(self):
        """
        Return coordinates of all elves and goblins in "read order"
        """
        p = list(self.elves.keys())
        p.extend(list(self.goblins.keys()))
        return sorted(p, key=lambda k: (k[1], k[0]))


if __name__ == "__main__":
    lines = read_data()

    cave = Cave.from_data(lines)
    cave.display()

    goblins, elves = {}
    for turn in range(5):
        p = cave.pieces()
        cave.move(p[0])
        cave.display()

    elf = (30, 13)
    cave.move(elf)
    cave.display()
    # for r in cave.overlay(best[1], "+"):
    #     print(''.join(r))

    # print(f"Chosen target at {best[1]}")

    # path2 = cave.shortest_path_nr((4, 10), (21, 14))

    # path = [(5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (10, 11), (11, 11), (12, 11), (13, 11),
    #         (14, 11), (15, 11), (16, 11), (17, 11), (18, 11), (19, 11), (19, 12), (20, 12), (20, 13), (21, 13), (21, 14)]

    # for r in cave.overlay(a, "+"):
    #     print(''.join(r))

    # print(path)
    # print(path2)
