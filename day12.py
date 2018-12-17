def read_data(filename="data/input12.data"):
    with open(filename) as f:
        return f.read().splitlines()


def parse_data(lines):
    return (
        lines[0][len("initial state: "):],
        [list(line[:5]) for line in lines[1:] if line[-1] == "#"]
    )


class Pots:
    def __init__(self, state):
        self.state = {i for i, p in enumerate(state) if p == "#"}

    def to_string(self):
        d = list(self.state)
        if not d:
            return ""

        low, high = min(d), max(d)
        s = ["."] * (high-low+1)
        for pot in d:
            s[pot - low] = "#" if pot in self.state else "."
        return "".join(s)

    def matches(self, rule, centre):
        """
        Check if rule matches around the index pot.
        This means check all indexes from [-2,-1,0,1,2] around centre.
        """
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
