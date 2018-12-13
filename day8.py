"""
day 8 of Advent of Code 2018
by Stefan Kruger
"""


class DataProvider:
    def __init__(self, data):
        self.cursor = 0
        self.data = data

    @classmethod
    def read_file(cls, filename="data/input8.data"):
        with open(filename) as f:
            return cls([int(item) for item in f.read().split(" ")])

    def next(self):
        self.cursor += 1
        return self.data[self.cursor - 1]


class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    @classmethod
    def make_node(cls, data):
        node_count = data.next()
        meta_count = data.next()

        children = []
        metadata = []

        for _ in range(node_count):
            children.append(cls.make_node(data))

        for _ in range(meta_count):
            metadata.append(data.next())

        return cls(children, metadata)

    def meta_sum(self):
        s = sum(self.metadata)
        for c in self.children:
            s += c.meta_sum()

        return s

    def value(self):
        """
        If a node has no child nodes, its value is the sum of its metadata
        entries.

        However, if a node does have child nodes, the metadata entries become
        indexes which refer to those child nodes. A metadata entry of 1 refers
        to the first child node, 2 to the second, 3 to the third, and so on.
        The value of this node is the sum of the values of the child nodes
        referenced by the metadata entries. If a referenced child node does not
        exist, that reference is skipped. A child node can be referenced
        multiple time and counts each time it is referenced. A metadata entry
        of 0 does not refer to any child node.
        """

        if not self.children:
            return sum(self.metadata)

        v = 0
        for index in self.metadata:
            child = index - 1
            if child < 0 or child >= len(self.children):
                continue

            v += self.children[child].value()

        return v


if __name__ == "__main__":
    data = DataProvider.read_file()
    # data = DataProvider([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2])
    tree = Node.make_node(data)

    print(f'Part1: {tree.meta_sum()}')
    print(f'Part2: {tree.value()}')
