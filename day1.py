"""
day 1 of Advent of Code 2018
by Stefan Kruger
"""
from collections import Counter


def read_data(filename="data/input1.data"):
    with open(filename) as f:
        return [int(item) for item in f.read().splitlines()]


def part2(data):
    freqs = Counter()
    current = 0

    while True:
        for f in data:
            freqs[current] += 1
            if freqs[current] == 2:
                return current

            current += f


if __name__ == "__main__":
    data = read_data()
    print(sum(data))
    print(part2(data))
