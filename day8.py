"""
day 8 of Advent of Code 2018
by Stefan Kruger
"""


class DataProvider:
    def __init__(self, data):
        self.cursor = 0
        self.data = data

    @classmethod
    def read_file(cls, filename="input8.data"):
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


if __name__ == "__main__":
    data = DataProvider.read_file()
    # data = DataProvider([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2])
    tree = Node.make_node(data)

    print(tree.meta_sum())
