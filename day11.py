import concurrent.futures


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

    def filterN(self, filter_size):
        """
        Square NxN 2d summing filter. Filter must fall completely inside the
        grid.
        """
        filtered = [[0] * 300 for y in range(300)]
        for y in range(300):
            for x in range(300):
                for fy in range(y, y+filter_size):
                    if fy >= 300:
                        continue
                    for fx in range(x, x+filter_size):
                        if fx >= 300:
                            continue
                        filtered[y][x] += self.grid[fy][fx]

        return filtered

    def find_max(self, filter_size):
        filtered = self.filterN(filter_size)

        best = (None, None, None)
        for y in range(0, 300):
            for x in range(0, 300):
                if best[0] is None or filtered[y][x] > best[0]:
                    best = (filtered[y][x], x, y)

        return (best[0], best[1]+1, best[2]+1, filter_size)


def proc(task):
    return task[0].find_max(task[1])


if __name__ == "__main__":
    puzzle_input = 7803

    grid = Grid(puzzle_input)
    best = grid.find_max(3)

    print(f"Part1: {best}")

    # for size in range(1, 301):
    #     candidate = grid.find_max(size)
    #     if candidate[0] > best[0]:
    #         best = candidate

    # print(f"Part2: {best}")

    tasks = [(grid, i) for i in range(1, 301)]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for candidate in executor.map(proc, tasks):
            if candidate[0] > best[0]:
                best = candidate
                print(best)
