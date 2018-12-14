def power_level(xpos, ypos, grid_serial):
    """
    (xpos, ypos) are in the 1,300 coordinate system.
    """
    rack_id = xpos + 10
    start_level = rack_id * ypos
    power = start_level + grid_serial
    power *= rack_id
    return int((power % 1000) / 100) - 5


class Grid:
    def __init__(self, grid_serial):
        self.grid = [[0] * 300 for y in range(300)]
        self.grid_serial = grid_serial
        for y in range(300):
            for x in range(300):
                self.grid[y][x] = power_level(x + 1, y + 1, grid_serial)

    def filter(self):
        """
        Convolve with square 3x3 2d summing filter. Filter must fall completely
        inside the grid.
        """
        filtered = [[0] * 300 for y in range(300)]
        for y in range(300):
            for x in range(300):
                for fy in [y - 1, y, y + 1]:
                    if fy < 0 or fy == 300:
                        continue
                    for fx in [x - 1, x, x + 1]:
                        if fx < 0 or fx == 300:
                            continue
                        filtered[y][x] += self.grid[fy][fx]

        return filtered

    def find_max(self):
        filtered = self.filter()

        # Find max, skipping edges, where the filter will have gone outside the
        # grid.
        best = (None, None, None)
        for y in range(1, 299):
            for x in range(1, 299):
                if best[0] is None or filtered[y][x] > best[0]:
                    best = (filtered[y][x], x, y)

        return best


if __name__ == "__main__":
    puzzle_input = 7803
    grid = Grid(puzzle_input)

    print(f"Part1: {grid.find_max()}")
