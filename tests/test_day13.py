import pytest  # type: ignore

from day13 import Cart, Collision, Map, Node

TESTDATA = [
    list('/->-\\'),
    list('|   |  /----\\'),
    list('| /-+--+-\\  |'),
    list('| | |  | v  |'),
    list('\\-+-/  \\-+--/'),
    list('  \\------/')
]


def test_sample_data():
    tracks = Map.from_lines(TESTDATA)

    assert len(tracks.carts) == 2
    assert (2, 0) in tracks.carts
    assert (9, 3) in tracks.carts

    tracks.tick()

    assert len(tracks.carts) == 2
    assert (3, 0) in tracks.carts
    assert (9, 4) in tracks.carts

    # Turn a few corners
    tracks.tick()
    tracks.tick()

    assert len(tracks.carts) == 2
    assert (4, 1) in tracks.carts
    assert (11, 4) in tracks.carts

    # Tick along to first expected collision
    for _ in range(10):
        tracks.tick()

    with pytest.raises(Collision) as err:
        tracks.tick()

    assert err.value.args[0] == {"pos": (7, 3)}
