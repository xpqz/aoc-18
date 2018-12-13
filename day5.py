"""
day 5 of Advent of Code 2018
by Stefan Kruger
"""
import concurrent.futures
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


def read_data(filename="data/input5.data"):
    with open(filename) as f:
        return f.read().splitlines()[0].rstrip()


def proc(polymer):
    polymer.reduce_full()
    return polymer.size()


if __name__ == "__main__":
    data = read_data()
    polymer = Polymer(data)
    polymer.reduce_full()
    print(f"Part1: {polymer.size()}")

    polymers = []
    for unit in list(string.ascii_lowercase):
        polymer = Polymer(data)
        polymer.mutate(unit)
        polymers.append(polymer)

    min_size = len(data)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for size in executor.map(proc, polymers):
            if size < min_size:
                print(size)
                min_size = size
