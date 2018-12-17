"""
day 12 of Advent of Code 2018
by Stefan Kruger

Similar to a Conway's game-of-life cellular automata, in 1D.
"""

from collections import Counter


def read_data(filename="data/input12.data"):
    with open(filename) as f:
        return f.read().splitlines()


def parse_data(lines):
    return (
        lines[0][len("initial state: "):],
        [list(line[:5]) for line in lines[1:] if line and line[-1] == "#"]
    )


class Pots:
    def __init__(self, state):
        self.state = {i for i, p in enumerate(state) if p == "#"}

    def matches(self, rule, centre):
        for i in range(-2, 3):
            pot = centre+i
            if pot in self.state and rule[i+2] == ".":
                return False
            if pot not in self.state and rule[i+2] == "#":
                return False
        return True

    def generate(self, rules):
        next_gen = set()
        for pot in self.state:
            for rule in rules:
                for centre in range(-2, 3):
                    if self.matches(rule, pot + centre):
                        next_gen.add(pot + centre)
                        break

        self.state = next_gen


if __name__ == "__main__":
    (initial_state, rules) = parse_data(read_data())

    pots = Pots(initial_state)
    for gen in range(20):
        pots.generate(rules)

    plants = sum(pots.state)

    print(f"Part1: {plants}")

    # Part 2: 50000000000 generations...
    #
    # Too much to brute-force. Working hypothesis: check for emergent stable
    # pattern. The two simplest potential options are:
    #
    # 1. Constant -- checksum converges to fixed value
    # 2. Constant change -- checksum change converges to fixed value
    #
    # Pretty easy to confirm that that the second case is what we have:

    pots = Pots(initial_state)
    val = sum(pots.state)
    for gen in range(100):
        pots.generate(rules)
        checksum = sum(pots.state)
        print(f"Gen: {gen} checksum: {checksum} checksum diff: {checksum - val}")
        val = checksum

    # # gives:
    # Gen: 92 checksum diff: 157
    # Gen: 93 checksum diff: -61
    # Gen: 94 checksum diff: 101
    # Gen: 95 checksum diff: -5
    # Gen: 96 checksum diff: 48
    # Gen: 97 checksum diff: 48
    # Gen: 98 checksum diff: 51
    # Gen: 99 checksum diff: 51
    # Gen: 100 checksum diff: 51
    # Gen: 101 checksum diff: 51
    # Gen: 102 checksum diff: 51  etc etc etc
    #
    # So we can conclude that after the 97th generation, every subsequent
    # generation adds 51 to the value.

    # Gen: 97 checksum: 6193 checksum diff: 48
    print(f"Part2: {6193+(50000000000-98)*51}")
