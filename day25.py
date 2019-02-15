"""
day 25 of Advent of Code 2018
by Stefan Kruger
"""
import re
import networkx as nx

def read_data(filename="data/input25.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    return [
        tuple(map(int, re.findall(r"-?\d+", line)))
        for line in lines
    ]

def dist(a, b):
    return (
        abs(a[0]-b[0]) +
        abs(a[1]-b[1]) +
        abs(a[2]-b[2]) +
        abs(a[3]-b[3])
    )

if __name__ == "__main__":
    data = parse_data(read_data())

    G = nx.Graph()

    for i in data:
        G.add_node(i)
        for j in data:
            if dist(i, j) <= 3:
                G.add_edge(i, j)

    clusters = list(nx.connected_components(G))

    print(len(clusters))
