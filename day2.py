from collections import Counter


def read_data(filename="input2.data"):
    with open(filename) as f:
        lines = f.read().splitlines()

    return lines


def check(item):
    freq = Counter()
    for letter in list(item):
        freq[letter] += 1

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

    if len(result):
        mystr = ""
        found = list(result)
        (item1, item2) = list(found[0])
        l1 = list(item1)
        l2 = list(item2)
        for index in range(0, len(l1)):
            if l1[index] == l2[index]:
                mystr += l1[index]

        return mystr

    return ''


if __name__ == "__main__":
    data = read_data()
    print(part1(data))
    print(part2(data))
