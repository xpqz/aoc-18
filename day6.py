"""
day 6 of Advent of Code 2018
by Stefan Kruger
"""
from collections import Counter
from dataclasses import dataclass
import copy
import re


@dataclass
class Point:
    x: int
    y: int
    id: int


class DistanceMap:
    def __init__(self, xsize, ysize):
        self.data = [
            [(None, None) for _ in range(0, xsize)]  # (pid, val)
            for _ in range(0, ysize)
        ]

    def set(self, point):
        self.data[point.y][point.x] = (point.id, 0)

    def compare(self, point, td):
        """
        Compare point with a value of td with any previous values. If this td
        is lower than the previous best, store this point. If equal, the point
        is contended, denoted with a negative.
        """
        if self.data[point.y][point.x][1] is None:
            self.data[point.y][point.x] = (point.id, td)

        elif td == abs(self.data[point.y][point.x][1]):
            self.data[point.y][point.x] = (None, -td)  # many pts with same td

        elif td < abs(self.data[point.y][point.x][1]):
            self.data[point.y][point.x] = (point.id, td)

    def _infinites(self):
        """
        Find the point that has the largest number of winning squares, and
        isn't infinite. We can exclude infinite areas by excluding any number
        on the data boundaries (x|y == 0, x==xmax, y=ymax)
        """
        infinites = {}
        for x in range(0, len(self.data[0])):
            val1 = self.data[0][x]
            val2 = self.data[len(self.data)-1][x]
            if val1[1] is not None and val1[1] >= 0:
                infinites[val1[0]] = True
            if val2[1] is not None and val2[1] >= 0:
                infinites[val2[0]] = True

        for y in range(0, len(self.data)):
            val1 = self.data[y][0]
            val2 = self.data[y][len(self.data[0])-1]
            if val1[1] is not None and val1[1] >= 0:
                infinites[val1[0]] = True
            if val2[1] is not None and val2[1] >= 0:
                infinites[val2[0]] = True

        return infinites

    def areas(self):
        infs = self._infinites()
        squares = Counter()

        for y in range(0, len(self.data)):
            for x in range(0, len(self.data[0])):
                item = self.data[y][x]
                if item[0] is None or item[0] in infs:
                    continue
                squares[item[0]] += 1

        return squares


class Area:
    def __init__(self, points, area, xmin, ymin):
        self.area = area
        self.points = points
        self.xmin = xmin
        self.ymin = ymin

    @classmethod
    def from_coordset(cls, lines):
        patt = re.compile(r'(\d+),\s+(\d+)')

        xmax = None
        ymax = None
        xmin = None
        ymin = None
        points = []

        for index, line in enumerate(lines):
            m = patt.match(line)
            if m:
                p = Point(x=int(m.group(1)), y=int(m.group(2)), id=index)
                if xmax is None or p.x > xmax:
                    xmax = p.x
                if ymax is None or p.y > ymax:
                    ymax = p.y

                if xmin is None or p.x < xmin:
                    xmin = p.x
                if ymin is None or p.y < ymin:
                    ymin = p.y
                points.append(p)

        # We now have a bounding box
        xsize = xmax - xmin + 1
        ysize = ymax - ymin + 1

        area = [[-1]*xsize for _ in range(0, ysize)]

        for point in points:
            xpos = point.x - xmin
            ypos = point.y - ymin
            point.x = xpos
            point.y = ypos

            area[ypos][xpos] = point.id

        return cls(points, area, xmin, ymin)

    def display(self):
        for row in self.area:
            print(row)

    def taxi_distance(self, point, xpos, ypos):
        dx = point.x - xpos
        dy = point.y - ypos
        return abs(dx) + abs(dy)

    def dist_map(self):
        """
        For each point, return a map showing the cab distance at each point
        """
        points_td = {}

        for point in self.points:
            pmap = []
            for ypos in range(0, len(self.area)):
                rowmap = []
                for xpos in range(0, len(self.area[ypos])):
                    if self.area[ypos][xpos] != -1:  # only consider empties
                        rowmap.append(-1)
                        continue
                    td = self.taxi_distance(point, xpos, ypos)
                    rowmap.append(td)
                pmap.append(rowmap)
            points_td[point.id] = pmap

        return points_td

    def find_winners(self, points_td):
        """
        Given a per-point taxi-distance map, find the overall winners.
        """
        winners = DistanceMap(
            xsize=len(self.area[0]),
            ysize=len(self.area)
        )

        for point_id, td_map in points_td.items():
            for y, row in enumerate(td_map):
                for x, value in enumerate(row):
                    winners.compare(Point(x, y, point_id), value)

        for point in self.points:
            winners.set(point)

        return winners

    def safe_region(self, distance_sum):
        """
        Find all squares where the sum of the taxi distance to all points is
        less than or equal to distance.
        """
        region_size = 0
        for ypos in range(0, len(self.area)):
            for xpos in range(0, len(self.area[ypos])):
                point_sum = 0
                for point in self.points:
                    point_sum += self.taxi_distance(point, xpos, ypos)

                if point_sum < distance_sum:
                    region_size += 1

        return region_size


def read_data(filename="input6.data"):
    with open(filename) as f:
        return f.read().splitlines()


if __name__ == "__main__":
    data = read_data()
    area = Area.from_coordset(data)
    points_td = area.dist_map()
    winners = area.find_winners(points_td)
    areas = winners.areas()
    print(f'Part1: {areas.most_common()[0][1]}')
    print(f'Part2: {area.safe_region(10000)}')
