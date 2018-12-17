from day12 import Pots, parse_data

TEST_DATA = [
    "initial state: #..#.#..##......###...###",
    "...## => #",
    "..#.. => #",
    ".#... => #",
    ".#.#. => #",
    ".#.## => #",
    ".##.. => #",
    ".#### => #",
    "#.#.# => #",
    "#.### => #",
    "##.#. => #",
    "##.## => #",
    "###.. => #",
    "###.# => #",
    "####. => #"
]

GENERATIONS = [
    "...#..#.#..##......###...###...........",
    "...#...#....#.....#..#..#..#...........",
    "...##..##...##....#..#..#..##..........",
    "..#.#...#..#.#....#..#..#...#..........",
    "...#.#..#...#.#...#..#..##..##.........",
    "....#...##...#.#..#..#...#...#.........",
    "....##.#.#....#...#..##..##..##........",
    "...#..###.#...##..#...#...#...#........",
    "...#....##.#.#.#..##..##..##..##.......",
    "...##..#..#####....#...#...#...#.......",
    "..#.#..#...#.##....##..##..##..##......",
    "...#...##...#.#...#.#...#...#...#......",
    "...##.#.#....#.#...#.#..##..##..##.....",
    "..#..###.#....#.#...#....#...#...#.....",
    "..#....##.#....#.#..##...##..##..##....",
    "..##..#..#.#....#....#..#.#...#...#....",
    ".#.#..#...#.#...##...#...#.#..##..##...",
    "..#...##...#.#.#.#...##...#....#...#...",
    "..##.#.#....#####.#.#.#...##...##..##..",
    ".#..###.#..#.#.#######.#.#.#..#.#...#..",
    ".#....##....#####...#######....#.#..##."
]

G0 = "#..#.#..##......###...###"
G1 = "...#...#....#............"
R0 = "..#.."
R1 = ".#.#."
R2 = ".##.."


def to_string(pots):
    low, high = min(pots.state), max(pots.state)
    s = ["."] * (high-low+1)
    for pot in pots.state:
        s[pot - low] = "#" if pot in pots.state else "."
    return "".join(s)


def test_parse_data():
    """
    """
    (initial_state, rules) = parse_data(TEST_DATA)

    assert initial_state == "#..#.#..##......###...###"
    line = 1
    for rule in rules:
        assert rule == list(TEST_DATA[line][:5])
        line += 1


def test_g0_g1():
    pots = Pots(list(G0))
    rules = [list(R0), list(R1), list(R2)]
    pots.generate(rules)

    assert to_string(pots).strip(".") == G1.strip(".")


def test_sample_data_set():
    """
    """
    (initial_state, rules) = parse_data(TEST_DATA)

    pots = Pots(initial_state)
    for gen in range(20):
        actual = to_string(pots).strip(".")
        expected = GENERATIONS[gen].strip(".")
        assert actual == expected, f"Failed at gen {gen}"
        pots.generate(rules)

    plants = sum(pots.state)
    assert plants == 325
