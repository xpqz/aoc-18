from copy import copy
from collections import deque
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


def adj(p):
    return {(p[0] - 1, p[1]), (p[0] + 1, p[1]), (p[0], p[1] - 1), (p[0], p[1] + 1)}


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

    def game_over(self):
        """
        Game is over if one creature type is extinct
        """
        return not self.goblins or not self.elves

    def hitpoints_remaining(self):
        return (
            sum([i.hitpoints for i in self.goblins.values()]) + 
            sum([i.hitpoints for i in self.elves.values()])
        )

    def valid_moves(self, p, my_team):
        """
        A valid move from p is either a step to an adjacent empty square or an attack.
        """
        return sorted([
            n 
            for n in adj(p) 
            if n in self.adjacency 
            if n not in my_team
        ], key=lambda x: (x[1], x[0]))
    
    def find_move(self, start, my_team, enemies):
        queue = deque([(start, [])])
        max_depth = math.inf
        visited = {start}
        while queue:
            node, path = queue.popleft()
            for n in self.valid_moves(node, my_team):
                if n in visited:
                    continue
                visited.add(n)
                if len(path) <= max_depth:    
                    if n in enemies:
                        max_depth = len(path)
                        yield path
                    else:
                        queue.append((n, path + [n]))
                elif max_depth < math.inf:
                    return


    @classmethod
    def from_data(cls, lines):
        elves, goblins = {}, {}
        data = set()
        for y, row in enumerate(lines):
            for x, item in enumerate(row):
                if item == "#":
                    continue
                p = (x, y)
                data.add(p)
                if item == "G":
                    goblins[p] = Goblin(pos=p)
                elif item == "E":
                    elves[p] = Elf(pos=p)

        # build adjacency graph
        graph = {
            p: {n for n in adj(p) if n in data}
            for p in data
        }

        return cls(graph, elves, goblins, (x+1, y+1))

    def display(self, print_hp=True):
        for y in range(self.dim[1]):
            hp = []
            for x in range(self.dim[0]):
                c = self.at((x, y))
                if isinstance(c, Goblin) or isinstance(c, Elf):
                    hp.append(c.hitpoints)
                print(str(c), end="")
            if hp and print_hp:
                print("    ", " ".join([str(h) for h in hp]), end="")
            print()

    def teams(self, pos):
        if pos in self.elves:
            return self.elves, self.goblins

        if pos in self.goblins:
            return self.goblins, self.elves

        return None, None

    def first_move_available(self, pos):
        for n in adj(pos):
            if self.at(n) == ".":
                return True

        return False

    def in_range(self, targets):
        """
        Return True if any open squares exist in an attacking position.
        """
        for pos in targets.keys():
            if self.first_move_available(pos):
                return True

        return False

    def move(self, start):
        """
        Move piece at start one step along the shortest path to an attackable
        position. If already in attacking position, piece won't move. Returns
        position after move (may be the start pos).
        """

        # Sanity check that we're still here.
        if start not in self.goblins and start not in self.elves:
            return start

        my_team, enemies = self.teams(start)

        # If no open attacking squares exist, we can't move. This doesn't imply
        # game over, as attacks may be in progress.
        if not self.in_range(enemies):
            return start

        # If I'm already in an attacking position, I don't move.
        for n in adj(start):
            if n in enemies:
                return start

        # If there are no open squares around me, I can't move.
        if not self.first_move_available(start):
            return start

        paths = list(self.find_move(start, my_team, enemies))

        if not paths:
            return start

        next_square = sorted(list({path[0] for path in paths}), key=lambda x: (x[1], x[0]))[0]

        piece = my_team.pop(start)
        piece.pos = next_square
        my_team[next_square] = piece

        return next_square

    def attack(self, pos):
        """
        If pos is in an attacking position, execute the attack. Return True if
        an kill was made, False if not. 
        """

        # Sanity check: we may have already been killed.
        if pos not in self.goblins and pos not in self.elves: 
            return False, None

        my_team, enemies = self.teams(pos)

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
                return True, enemies

        return False, None

    def pieces(self):
        """
        Return coordinates of all elves and goblins in "read order"
        """
        p = list(self.elves.keys())
        p.extend(list(self.goblins.keys()))
        return sorted(p, key=lambda k: (k[1], k[0]))

    def execute_turn(self, shortcircuit=None):
        moved = set()
        game_over = False
        killed, team = False, None
        for piece in self.pieces():
            if self.game_over():
                game_over = True
                break
            if piece not in moved:
                new_pos = self.move(piece)
                killed, team = self.attack(new_pos)
                moved.add(new_pos)
                if killed and shortcircuit == team:
                    break

        return game_over, killed, team

if __name__ == "__main__":
    lines = read_data()
    cave = Cave.from_data(lines)
    turns = 1
    game_over = False
    while not game_over:
        game_over, _, _ = cave.execute_turn()
        if game_over:
            break
        turns += 1

    hp = cave.hitpoints_remaining()

    print(f"Part1: {(turns-1)*hp}")

    # Part2: Vary the Elves attacking strength until no Elves are lost.

    for ap in range(4, 200):
        cave = Cave.from_data(lines)
        for elf in cave.elves.values():
            elf.attack = ap
        elf_count_before = len(cave.elves)
        turns = 1
        game_over = False
        while not game_over:
            game_over, killed, team = cave.execute_turn(shortcircuit=cave.elves)
            if killed and team == cave.elves or game_over:
                break
            turns += 1
        if game_over:
            hp = cave.hitpoints_remaining()
            print(f"Part2: {(turns-1)*hp} Elves win with attackpoints at {ap} after {turns-1}")
            break            

    


