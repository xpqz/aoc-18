"""
day 14 of Advent of Code 2018
by Stefan Kruger
"""
DIGITS = [
    [0], [1], [2], [3], [4], [5], [6], [7], [8], [9],
    [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5],
    [1, 6], [1, 7], [1, 8]
]


class ChocolateLab:
    def __init__(self, target):
        self.recipes = [3, 7]
        self.elves = [0, 1]
        self.ipattern = [int(l) for l in target]

    def advance(self):
        pl = len(self.ipattern)

        new_recipe = self.recipes[self.elves[0]] + self.recipes[self.elves[1]]
        self.recipes.extend(DIGITS[new_recipe])
        for e in [0, 1]:
            advancement = (1 + self.recipes[self.elves[e]])
            self.elves[e] = (self.elves[e] + advancement) % len(self.recipes)

        # Check for match. As we may have added two recipes, we must check
        # two potential matches.
        if self.recipes[-pl:] == self.ipattern:
            return (True, 0)

        return (self.recipes[-pl-1:-1] == self.ipattern, 1)


if __name__ == "__main__":
    pattern = "765071"
    l = ChocolateLab(pattern)
    while len(l.recipes) < int(pattern) + 10:
        l.advance()

    p1data = l.recipes[int(pattern):int(pattern) + 11]

    print(f"Part1: {''.join([str(d) for d in p1data])}")

    # Part 2 -- takes 35s to run
    l = ChocolateLab(pattern)
    while True:
        (match, offset) = l.advance()
        if match:
            pos = len(l.recipes) - len(pattern) - offset
            print(f"Part2: {pos}")
            break
