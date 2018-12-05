"""
day 5 of Advent of Code 2018
by Stefan Kruger
"""
import re
import string


class Polymer:
    def __init__(self, composition):
        self.composition = composition
        self.pattern = re.compile(
            r"(aA|bB|cC|dD|eE|fF|gG|hH|iI|jJ|kK|lL|mM|"
            r"nN|oO|pP|qQ|rR|sS|tT|uU|vV|wW|xX|yY|zZ|"
            r"Aa|Bb|Cc|Dd|Ee|Ff|Gg|Hh|Ii|Jj|Kk|Ll|Mm|"
            r"Nn|Oo|Pp|Qq|Rr|Ss|Tt|Uu|Vv|Ww|Xx|Yy|Zz)"
        )

    def react(self):
        result = re.subn(self.pattern, "", self.composition)
        self.composition = result[0]
        return result[1] != 0

    def reduce_full(self):
        reaction = self.react()
        while reaction:
            reaction = self.react()

    def size(self):
        return len(self.composition)

    def mutate(self, unit):
        self.composition = re.sub(
            unit, '', self.composition, flags=re.IGNORECASE)


def read_data(filename="input5.data"):
    with open(filename) as f:
        return f.read().splitlines()[0].rstrip()


if __name__ == "__main__":
    data = read_data()
    polymer = Polymer(data)
    polymer.reduce_full()
    print(f"Part1: {polymer.size()}")

    best = (len(data), None)
    for unit in list(string.ascii_lowercase):
        polymer = Polymer(data)
        polymer.mutate(unit)
        polymer.reduce_full()
        if polymer.size() < best[0]:
            best = (polymer.size(), unit)

    print(f"Part2: {best[1]} -> {best[0]}")
