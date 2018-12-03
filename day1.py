
from collections import Counter


def read_data(filename="input1.data"):
    with open(filename) as f:
        lines = f.read().splitlines()

    return [
        int(item)
        for item in lines
    ]


def part1(data):
    return sum(data)


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
    print(part1(data))
    print(part2(data))
