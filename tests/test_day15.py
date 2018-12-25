import pytest  # type: ignore

from day15 import Cave, Elf, Goblin


MAP1 = [
    list('#######'),
    list('#E..G.#'),
    list('#...#.#'),
    list('#.G.#G#'),
    list('#######')
]

MAP2 = [
    list('################################'),
    list('#########....#..#####.......####'),
    list('###########G......###..##..#####'),
    list('###########.....#.###......#####'),
    list('###############.#...#.......####'),
    list('###############..#....E......###'),
    list('############.##...#...G....#####'),
    list('############.##.....G..E...#####'),
    list('###########G.##...GG......######'),
    list('#..####G##..G##..G.#......######'),
    list('#...S......#............#.######'),
    list('#.......#....G.......G.##..#...#'),
    list('#....XG.......#####...####...#.#'),
    list('#.....G..#...#######..#####...E#'),
    list('#.##.....G..#########.#######..#'),
    list('#........G..#########.#######E##'),
    list('####........#########.##########'),
    list('##.#........#########.##########'),
    list('##.G....G...#########.##########'),
    list('##...........#######..##########'),
    list('#.G..#........#####...##########'),
    list('#......#.G.G..........##########'),
    list('###.#................###########'),
    list('###..................###.#######'),
    list('####............E.....#....#####'),
    list('####.####.......####....E.######'),
    list('####..#####.....####......######'),
    list('#############..#####......######'),
    list('#####################EE..E######'),
    list('#####################..#.E######'),
    list('#####################.##########'),
    list('################################')
]

MAP3 = [
    list('#########'),
    list('#G..G..G#'),
    list('#.......#'),
    list('#.......#'),
    list('#G..E..G#'),
    list('#.......#'),
    list('#.......#'),
    list('#G..G..G#'),
    list('#########')
]

MAP4 = [
    list('#######'),
    list('#.E...#'),
    list('#.....#'),
    list('#...G.#'),
    list('#######')
]


@pytest.mark.parametrize(
    "data,elves,goblins",
    [
        (MAP1, [(1, 1)], [(4, 1), (2, 3), (5, 3)]),
        (MAP2, [(16, 24), (21, 28), (22, 5), (22, 28), (23, 7),
                (24, 25), (25, 28), (25, 29), (29, 15), (30, 13)],
         [(2, 20), (3, 18), (6, 12), (6, 13), (7, 9), (8, 18), (9, 14),
          (9, 15), (9, 21), (11, 2), (11, 8), (11, 21), (12, 9), (13, 11),
          (17, 9), (18, 8), (19, 8), (20, 7), (21, 11), (22, 6)])
    ]
)
def test_sample_data1(data, elves, goblins):
    c = Cave.from_data(data)

    for e in elves:
        assert e in c.elves

    for g in goblins:
        assert g in c.goblins


def test_range_finder():
    c = Cave.from_data(MAP1)
    r = c.in_range(c.goblins)

    assert set(r) == {(3, 1), (5, 1), (2, 2), (5, 2), (1, 3), (3, 3)}


def test_multiple_shortest_paths_example():
    c = Cave.from_data(MAP4)
    c.move((2, 1))
    assert set(c.elves.keys()) == {(3, 1)}


def test_multiple_shortest_paths_example2():
    c = Cave.from_data(MAP3)
    c.move((7, 1))
    assert (6, 1) in set(c.goblins.keys())


EXPECTED_3_1 = [
    list('#########'),
    list('#.G...G.#'),
    list('#...G...#'),
    list('#...E..G#'),
    list('#.G.....#'),
    list('#.......#'),
    list('#G..G..G#'),
    list('#.......#'),
    list('#########')
]


EXPECTED_3_2 = [
    list('#########'),
    list('#..G.G..#'),
    list('#...G...#'),
    list('#.G.E.G.#'),
    list('#.......#'),
    list('#G..G..G#'),
    list('#.......#'),
    list('#.......#'),
    list('#########')
]


EXPECTED_3_3 = [
    list('#########'),
    list('#.......#'),
    list('#..GGG..#'),
    list('#..GEG..#'),
    list('#G..G...#'),
    list('#......G#'),
    list('#.......#'),
    list('#.......#'),
    list('#########')
]


def test_movement():
    state = Cave.from_data(MAP3)
    expected = [
        Cave.from_data(EXPECTED_3_1),
        Cave.from_data(EXPECTED_3_2),
        Cave.from_data(EXPECTED_3_3)
    ]

    for result in expected:
        for piece in state.pieces():
            state.move(piece)
        assert set(state.goblins.keys()) == set(result.goblins.keys())
        assert set(state.elves.keys()) == set(result.elves.keys())
