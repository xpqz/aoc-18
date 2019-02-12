
"""
day 23 part 2 of Advent of Code 2018
by Stefan Kruger

This uses the z3 theorem prover from Microsoft.

https://github.com/Z3Prover/z3/wiki/Documentation

This should be valid for all inputs.

"""
import re
from z3 import *

def read_data(filename="data/input23.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    return [list(map(int, re.findall(r"-?\d+", s))) for s in lines]

def zabs(x):
    return If(x >= 0, x, -x)

if __name__ == "__main__":
    bots = parse_data(read_data())

    (x, y, z) = (Int('x'), Int('y'), Int('z'))
    in_ranges = [Int('in_range_' + str(i)) for i in range(len(bots))]

    range_count = Int('sum')
    solver = Optimize()
    for i, bot in enumerate(bots):
        (nx, ny, nz), radius = tuple(bot[:3]), bot[3]
        solver.add(in_ranges[i] == If(zabs(x - nx) + zabs(y - ny) + zabs(z - nz) <= radius, 1, 0))

    solver.add(range_count == sum(in_ranges))
    dist_from_zero = Int('dist')
    solver.add(dist_from_zero == zabs(x) + zabs(y) + zabs(z))
    h1 = solver.maximize(range_count)
    h2 = solver.minimize(dist_from_zero)
    assert str(solver.check()) == "sat"

    assert solver.lower(h2) == solver.upper(h2)

    print(solver.lower(h2))
