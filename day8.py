"""
day 8 of Advent of Code 2018
by Stefan Kruger
"""
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, List

import json
import re


def read_data(filename="input8.data"):
    with open(filename) as f:
        return f.read().splitlines()[0]


def parse_data(data):
    return [
        int(item)
        for item in data.split(" ")
    ]


# read_node(numbers, 0, len(numbers))

def read_node(numbers, start, end, acc=0):  # inclusive

    if not numbers or end <= start:
        return acc

    child_nodes = numbers[start]
    meta_count = numbers[start + 1]

    if child_nodes == 0:
        # metadata is directly after meta_count, so can increase start
        meta_items = numbers[start + 2:start + 2 + meta_count]
        start = start + 2 + meta_count
        new_end = end
    else:
        new_end = end - meta_count
        start = start + 2
        meta_items = numbers[new_end + 1:end + 1]

    # print(
    #     f'\nNumbers: {numbers}\n'
    #     f'Start-end: {start}-{end}\n'
    #     f'Span: {numbers[start:end+1]}\n'
    #     f'Metacount: {meta_count}\n'
    #     f'Metaitems: {meta_items}\n'
    #     f'Newend:{new_end}'
    # )

    return read_node(numbers, start, new_end, acc+sum(meta_items))


if __name__ == "__main__":
    data = read_data()
    # --- TEST DATA
    data = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    # --- TEST DATA END
    numbers = parse_data(data)
    print(read_node(numbers, 0, len(numbers)-1))
