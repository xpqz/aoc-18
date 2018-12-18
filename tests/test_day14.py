from day14 import ChocolateLab

EXPECTED = [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7, 9, 2]


def test_sample_data():
    l = ChocolateLab()

    for _ in range(15):
        l.advance()

    assert l.generation() == EXPECTED
    assert l.elves() == [8, 4]
