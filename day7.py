"""
day 7 of Advent of Code 2018
by Stefan Kruger
"""
from collections import defaultdict
import json
import re


def read_data(filename="input7.data"):
    with open(filename) as f:
        return f.read().splitlines()


def parse_data(lines):
    patt = re.compile(r'Step (.) must be finished before step (.) can begin.')
    result = []
    for line in lines:
        m = patt.search(line)
        if m:
            result.append((m.group(1), m.group(2)))

    return result


class DAG:
    def __init__(self, edge_list):
        self.graph = defaultdict(list)
        self.vertexes = set()
        self.prereqs = defaultdict(list)
        for edge in edge_list:
            self.graph[edge[0]].append(edge[1])
            self.vertexes.add(edge[0])
            self.vertexes.add(edge[1])
            self.prereqs[edge[1]].append(edge[0])

    def display(self):
        print(json.dumps(self.graph, indent=4))

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]  # no .append()!
        if start == end:
            return [path]
        if start not in self.graph:
            return []
        paths = []
        for vertex in self.graph[start]:
            if vertex not in path:
                newpaths = self.find_all_paths(vertex, end, path)
                for newpath in newpaths:
                    paths.append(newpath)

        return paths

    def stepping_order(self):
        (start_list, end) = self.find_start_end()
        paths = []
        for start in start_list:
            paths.extend(self.find_all_paths(start, end))

        order = []
        while True:
            available = {path[0] for path in paths if path}
            if not available:
                break
            for s in sorted(available, reverse=True):
                if set(self.prereqs[s]).issubset(order):
                    step = s

            for path in paths:
                if path and path[0] == step:
                    path.remove(step)
            order.append(step)

        return order

    def find_start_end(self):
        """
        Assume single endpoint. Note: start is a list!
        """
        has_deps = set()
        is_dep = set()
        for vertex in self.vertexes:
            if vertex in self.graph:
                has_deps.add(vertex)
                for node in self.graph[vertex]:
                    is_dep.add(node)

        return (sorted(list(has_deps - is_dep)), list(is_dep - has_deps)[0])


if __name__ == "__main__":
    data = read_data()
    # data = [
    #     "Step C must be finished before step A can begin.",
    #     "Step C must be finished before step F can begin.",
    #     "Step A must be finished before step B can begin.",
    #     "Step A must be finished before step D can begin.",
    #     "Step B must be finished before step E can begin.",
    #     "Step D must be finished before step E can begin.",
    #     "Step F must be finished before step E can begin."
    # ]

    dag = DAG(parse_data(data))

    print(f'Part1: {"".join(dag.stepping_order())}')
