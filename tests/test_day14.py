import pytest  # type: ignore

from day14 import ChocolateLab

EXPECTED = [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7, 9, 2]


def test_sample_data():
    l = ChocolateLab("51589")

    for _ in range(15):
        l.advance()

    assert l.recipes == EXPECTED
    assert l.elves == [8, 4]


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("51589", 9),
        ("01245", 5),
        ("92510", 18),
        ("59414", 2018)
    ]
)
def test_p2_samples(pattern, expected):
    l = ChocolateLab(pattern)
    gen = 0
    found = False

    while gen < expected + len(pattern):
        (match, offset) = l.advance()
        if match:
            pos = len(l.recipes) - len(pattern) - offset
            assert pos == expected
            found = True
            break
        gen += 1

    assert found
