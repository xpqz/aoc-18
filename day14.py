from copy import copy


class ChocolateLab:
    def __init__(self):
        self.gen = {0: ([3, 7], [0, 1])}
        self.current = 0

    def generation(self, g=None):
        if g is None:
            g = self.current
        return copy(self.gen[g][0])

    def elves(self, g=None):
        if g is None:
            return self.gen[self.current][1]
        return self.gen[g][1]

    def show(self, g=None):
        if g is None:
            g = self.current
        l = self.generation(g)
        elves = self.elves(g)
        l[elves[0]] = f"({l[elves[0]]})"
        l[elves[1]] = f"[{l[elves[1]]}]"
        return l

    def advance(self):
        recipes, elves = self.gen[self.current]
        s = recipes[elves[0]] + recipes[elves[1]]
        recipes.extend([int(d) for d in str(s)])
        for e in [0, 1]:
            advancement = (1 + recipes[elves[e]])
            elves[e] = (elves[e] + advancement) % len(recipes)

        self.current += 1
        self.gen[self.current] = (recipes, elves)


if __name__ == "__main__":
    l = ChocolateLab()

    for i in range(15):
        l.advance()
        print(l.show())
