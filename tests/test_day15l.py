import pytest  # type: ignore

from day15l import Cave, Elf, Goblin


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
    list('#...G......#............#.######'),
    list('#.......#....G.......G.##..#...#'),
    list('#.....G.......#####...####...#.#'),
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

def test_multiple_shortest_paths_example_():
    c = Cave.from_data(MAP4)
    paths = c.bfs_paths((2,1), (4, 2))
    
    best = None
    for p in paths:
        if best is None:
            best = len(p)
        if len(p) > best:
            break
        print(p)



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

TEST_MAP = [
    list('##########################'),
    list('#######.....#########....#'),
    list('#######...G..#######G....#'),
    list('#######...C...#####.EG...#'),
    list('###.#....#.....E.E...EG..#'),
    list('###......#......E.....E..#'),
    list('##...........#.......E...#'),
    list('##.......................#'),
    list('##########################')
]

def test_movement2():
    state = Cave.from_data(TEST_MAP)
    # state.move((17, 4))
    # assert (17, 5) in state.elves

    paths = state.bfs_paths((17,14), (11,2))
    
    best = None
    for p in paths:
        if best is None:
            best = len(p)
        if len(p) > l:
            break

        print(p)
        

COMBAT_MAP = [
    list('#######'),
    list('#.G...#'),
    list('#...EG#'),
    list('#.#.#G#'),
    list('#..G#E#'),
    list('#.....#'),
    list('#######')
]


COMBAT_MAP2 = [
    list('#######'),
    list('#G..#E#'),
    list('#E#E.E#'),
    list('#G.##.#'),
    list('#...#E#'),
    list('#...E.#'),
    list('#######')
]


COMBAT_MAP3 = [
    list('#######'),
    list('#E..EG#'),
    list('#.#G.E#'),
    list('#E.##E#'),
    list('#G..#.#'),
    list('#..E#.#'),
    list('#######'),
]

COMBAT_MAP4 = [
    list('#######'),
    list('#E.G#.#'),
    list('#.#G..#'),
    list('#G.#.G#'),
    list('#G..#.#'),
    list('#...E.#'),
    list('#######')
]

COMBAT_MAP5 = [
    list('#######'),
    list('#.E...#'),
    list('#.#..G#'),
    list('#.###.#'),
    list('#E#G#G#'),
    list('#...#G#'),
    list('#######')
]

COMBAT_MAP6 = [
    list('#########'),
    list('#G......#'),
    list('#.E.#...#'),
    list('#..##..G#'),
    list('#...##..#'),
    list('#...#...#'),
    list('#.G...G.#'),
    list('#.....G.#'),
    list('#########')
]

COMBAT_R1 = [
    list('#######'),
    list('#..G..#'),
    list('#...EG#'),
    list('#.#G#G#'),
    list('#...#E#'),
    list('#.....#'),
    list('#######')
]

GAME_OVER = [
    list('#######'),
    list('#G....#'),
    list('#.G...#'),
    list('#.#.#G#'),
    list('#...#.#'),
    list('#....G#'),
    list('#######')
]

BAD_MOVE_TEST = [
    (list('################################'), []),
    (list('#########....#..#####.......####'), []),
    (list('###########.......###..##..#####'), []),
    (list('###########.....#.###......#####'), []),
    (list('###############.#...#.......####'), []),
    (list('###############..#.G...G.....###'), [200, 197]),
    (list('############.##...#.G..G...#####'), [200, 200]),
    (list('############.##.........G..#####'), [182]),
    (list('###########..##...G....GE.######'), [200, 110, 26]),
    (list('#..####.##...##....#....GE######'), [125, 200]),
    (list('#..........#............#.######'), []),
    (list('#.......#..............##..#...#'), []),
    (list('#..........G..#####...####...#.#'), [200]),
    (list('#........#G..#######..#####....#'), [200]),
    (list('#.##........#########.#######..#'), []),
    (list('#...........#########.#######.##'), []),
    (list('####........#########.##########'), []),
    (list('##.#........#########.##########'), []),
    (list('##..........#########.##########'), []),
    (list('##.........G.#######EG##########'), [200, 140, 80]),
    (list('#....#......G.#####..E##########'), [200, 200]),
    (list('#......#.......GE.....##########'), [143, 8]),
    (list('###.#.........GE.....###########'), [200, 188]),
    (list('###............GE....###.#######'), [89, 167]),
    (list('####..........GE......#....#####'), [200, 2]),
    (list('####.####......G####......######'), [200]),
    (list('####..#####.....####......######'), []),
    (list('#############..#####......######'), []),
    (list('#####################.....######'), []),
    (list('#####################..#..######'), []),
    (list('#####################.##########'), []),
    (list('################################'), [])
]

# def test_strange_move():
#     state = Cave.from_data_(BAD_MOVE_TEST)
#     state.display_full()
#     state.execute_turn()
#     state.display_full()

def test_game_over():
    state = Cave.from_data(GAME_OVER)
    assert state.game_over()


def test_combat():
    state = Cave.from_data(COMBAT_MAP)
    r1 = Cave.from_data(COMBAT_R1)
    r1.goblins[(5, 2)].hitpoints = 197
    r1.goblins[(5, 3)].hitpoints = 197
    r1.elves[(4, 2)].hitpoints = 197
    r1.elves[(5, 4)].hitpoints = 197

    for piece in state.pieces():
        new_pos = state.move(piece)
        state.attack(new_pos)

    assert state.goblins == r1.goblins
    assert state.elves == r1.elves


@pytest.mark.parametrize(
    "combat_map,full_turns,hp_remaining",
    [
        (COMBAT_MAP, 47, 590),
        (COMBAT_MAP2, 37, 982),
        (COMBAT_MAP3, 46, 859),
        (COMBAT_MAP4, 35, 793),
        (COMBAT_MAP5, 54, 536),
        (COMBAT_MAP6, 20, 937)
    ]
)
def test_combat_full(combat_map, full_turns, hp_remaining):
    state = Cave.from_data(combat_map)

    turns = 1
    game_over = False
    while turns < full_turns + 3:
        for piece in state.pieces():
            if state.game_over():
                game_over = True
                break
            new_pos = state.move(piece)
            state.attack(new_pos)
        if game_over:
            break
        turns += 1

    # state.display()

    assert turns-1 == full_turns

    hp = state.hitpoints_remaining()
    assert hp["goblins"] + hp["elves"] == hp_remaining
