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
