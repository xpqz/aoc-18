"""
day 9 of Advent of Code 2018
by Stefan Kruger

Solution using actual linked list to avoid O(n) insertion behaviour that
cripples part 2.

An alternative approach could have used a deque:

https://stackoverflow.com/questions/39522787/time-complexity-of-random-access-in-deque-in-python
"""

from collections import Counter
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    item: int
    left: Any = None
    right: Any = None
    start: bool = False


class CircularList:
    def __init__(self):
        self.cursor = None
        self.scores = Counter()

    def moveleft(self, steps):
        for _ in range(steps):
            self.cursor = self.cursor.left

    def moveright(self, steps):
        for _ in range(steps):
            self.cursor = self.cursor.right

    def insert_at_cursor(self, item):
        node = Node(item)

        if self.cursor is None:
            node.left = node
            node.right = node
            node.start = True
            self.cursor = node
            return

        node.right = self.cursor
        node.left = self.cursor.left

        # Single node
        if self.cursor.start and self.cursor.right.start:
            self.cursor.right = node

        self.cursor.left.right = node
        self.cursor.left = node
        self.cursor = node

    def remove_at_cursor(self):
        item = self.cursor.item
        is_start = self.cursor.start
        self.cursor.left.right = self.cursor.right
        self.cursor.right.left = self.cursor.left
        self.cursor = self.cursor.right
        self.cursor.start = is_start
        return item

    def place(self, player, marble):
        if marble % 23 == 0:
            self.moveleft(7)
            removed = self.remove_at_cursor()
            self.scores[player] += marble + removed
        else:
            self.moveright(2)
            self.insert_at_cursor(marble)

    def winner(self):
        return self.scores.most_common(1)


if __name__ == "__main__":
    circle = CircularList()

    # Set the zero marble; does not belong to a player
    circle.insert_at_cursor(0)

    marble = 1
    max_marble = 71588  # * 100   # Part2: times 100
    while marble < max_marble:
        for player in range(430):
            circle.place(player, marble)
            marble += 1
            if marble > max_marble:
                break

    print(circle.winner())
