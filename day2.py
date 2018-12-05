"""
day 1 of Advent of Code 2018
by Stefan Kruger
"""
from collections import Counter


def read_data(filename="input2.data"):
    with open(filename) as f:
        return f.read().splitlines()


def check(item):
    freq = Counter(list(item))
    twos = 0
    threes = 0
    for frequency in freq.values():
        if frequency == 2:
            twos = 1
        if frequency == 3:
            threes = 1

    return (twos, threes)


def part1(data):
    two_count = 0
    three_count = 0
    for box_id in data:
        (twos, threes) = check(box_id)
        two_count += twos
        three_count += threes

    return two_count * three_count


def difflen_one(item1, item2):
    diff = 0
    l1 = list(item1)
    l2 = list(item2)
    for index in range(0, len(l1)):
        if l1[index] != l2[index]:
            diff += 1

        if diff >= 2:
            break

    return diff == 1


def part2(data):
    result = set()
    for item1 in data:
        for item2 in data:
            if difflen_one(item1, item2):
                result.add(frozenset([item1, item2]))

    mystr = ""
    if len(result):
        found = list(result)
        (item1, item2) = list(found[0])
        l1 = list(item1)
        l2 = list(item2)
        for index in range(0, len(l1)):
            if l1[index] == l2[index]:
                mystr += l1[index]

    return mystr


if __name__ == "__main__":
    data = read_data()
    print(part1(data))
    print(part2(data))
