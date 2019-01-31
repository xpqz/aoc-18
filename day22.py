"""
day 22 of Advent of Code 2018
by Stefan Kruger
"""
def erosion_level(t, depth):
    return (t + depth) % 20183

def geo_index(pos, target, depth):
    vals = {(0, 0): 0, target: 0}
    for y in range(0, pos[1]+1):
        for x in range(0, pos[0]+1):
            this = (x, y)
            if this == target:
                continue
            if this[1] == 0:
                vals[this] = this[0] * 16807
            elif this[0] == 0:
                vals[this] = this[1] * 48271
            else:
                vals[this] = (
                    (vals[(this[0]-1, this[1])] + depth) % 20183 * 
                    (vals[(this[0], this[1]-1)] + depth) % 20183
                )

    return vals[pos]    

if __name__ == "__main__":

    depth = 10689
    target = (11, 722)

    risk = 0
    for y in range(0, target[1]+1):
        for x in range(0, target[0]+1):
            if (x, y) in {(0, 0), target}:
                continue
            gi = geo_index((x, y), target, depth)
            risk += erosion_level(gi, depth) % 3
                
    print(f"Part1: {risk}")


