"""
day 20 of Advent of Code 2018
by Stefan Kruger
"""
def read_data(filename="data/input20.data"):
    with open(filename) as f:
        return f.read().splitlines()[0]

offset = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

stack = []
x, y = 0, 0
prev_x, prev_y = x, y
dist = {(x, y): 0}

pattern = read_data()

for c in pattern[1:-1]:
    if c == "(":
        stack.append((x, y))
    elif c == ")":
        x, y = stack.pop()
    elif c == "|":
        x, y = stack[-1]
    else:
        dx, dy = offset[c]
        x, y = x+dx, y+dy
        if (x, y) in dist:
            dist[(x, y)] = min(dist[(x, y)], dist[(prev_x, prev_y)]+1)
        else:
            dist[(x, y)] = dist[(prev_x, prev_y)]+1
        
    prev_x, prev_y = x, y

print(f"Part1: {max(dist.values())}")
print(f"Part2: {len([x for x in dist.values() if x >= 1000])}")