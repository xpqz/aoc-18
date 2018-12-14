"""
day 10 of Advent of Code 2018
by Stefan Kruger
"""
import re


def read_data(filename="data/input10.data"):
    with open(filename) as f:
        return [
            [int(n) for n in re.findall(r"-?\d+", l)]
            for l in f.read().splitlines()
        ]


def pos(line, i):
    (x, y, dx, dy) = line
    return [x + i * dx, y + i * dy]


def find_min_bbox(lines):
    """
    Assumption: the points should be converging towards the point where
    the message appears, to then subsequently diverge. The saddle point
    should be at -- or near -- where the message is readable.
    """
    best = (-1, None, None, None, None, None)
    for i in range(15000):
        ipos = [pos(line, i) for line in lines]
        xmin = min(ipos, key=lambda x: x[0])[0]
        xmax = max(ipos, key=lambda x: x[0])[0]
        ymin = min(ipos, key=lambda x: x[1])[1]
        ymax = max(ipos, key=lambda x: x[1])[1]

        val = xmax - xmin + ymax - ymin
        if best[0] == -1 or val < best[1]:
            best = (i, val, xmin, xmax, ymin, ymax)

    return best


if __name__ == "__main__":
    lines = read_data()
    (second, _, xmin, xmax, ymin, ymax) = find_min_bbox(lines)

    # We know the bounding box, so we can allocate a "display" of the
    # right size.
    display = [[" "] * (xmax - xmin + 1) for y in range(ymin, ymax + 1)]

    # Apply the transformation resulting from "second" applications of the
    # linear motion to all points
    for line in lines:
        coord = pos(line, second)
        # shift by (xmin, ymin)
        display[coord[1] - ymin][coord[0] - xmin] = "#"

    print(f"Part1:")
    for row in display:
        print("".join(row))

    print(f"Part2: Best iteration: {second}")
