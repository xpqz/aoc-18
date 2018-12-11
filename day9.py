"""
day 9 of Advent of Code 2018
by Stefan Kruger
"""

from copy import copy
from collections import Counter


class CircularList:
    def __init__(self):
        self.data = [0]
        self.cursor = 0
        self.scores = Counter()

    def set_cursor_relative(self, delta):
        self.cursor = (self.cursor + delta) % len(self.data)

    def insert_at_cursor(self, item):
        if self.cursor == 0:  # 0 is the start-end connection point
            self.data.append(item)
            self.cursor = len(self.data) - 1
        else:
            self.data.insert(self.cursor, item)

    def remove_at_cursor(self):
        item = self.data[self.cursor]
        del_idx = self.cursor
        if self.data[self.cursor] == len(self.data) - 1:
            self.cursor = 0
        del self.data[del_idx]

        return item

    def place(self, player, marble):
        if marble % 23 == 0:
            self.set_cursor_relative(-7)
            removed = self.remove_at_cursor()
            self.scores[player] += marble + removed
        else:
            self.set_cursor_relative(2)
            self.insert_at_cursor(marble)

    def winner(self):
        return self.scores.most_common(1)


if __name__ == "__main__":
    circle = CircularList()

    marble = 1

    max_marble = 71588  # * 100   # Part2: takes 2h...
    while marble < max_marble:
        for player in range(430):
            circle.place(player, marble)
            marble += 1
            if marble > max_marble:
                break

    print(circle.winner())
