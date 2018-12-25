import pytest


from day import Cave, ROCKY, WET, NARROW


@pytest.fixture()
def example_cave():
    depth = 510
    mouth = 0, 0
    target = 10, 10

    cave = Cave(depth, target, mouth)

    yield cave


@pytest.mark.parametrize("x, y, expected_geological_index", [
    (0, 0, 0),
    (10, 10, 0),
    (1, 0, 16807),
    (10, 0, 168070),
    (0, 1, 48271),
    (0, 10, 482710),
    (1, 1, 145722555),
])
def test_get_geological_index(x, y, expected_geological_index, example_cave):

    result = example_cave.get_geological_index(x, y)

    assert result == expected_geological_index


@pytest.mark.parametrize("x, y, expected_erosion_level", [
    (0, 0, 510),
    (1, 0, 17317),
    (0, 1, 8415),
    (1, 1, 1805),
    (10, 10, 510),
])
def test_get_erosion_level(x, y, expected_erosion_level, example_cave):

    result = example_cave.get_erosion_level(x, y)

    assert result == expected_erosion_level


@pytest.mark.parametrize("x, y, expected_type", [
    (0, 0, ROCKY),
    (1, 0, WET),
    (0, 1, ROCKY),
    (1, 1, NARROW),
    (10, 10, ROCKY),
])
def test_get_type(x, y, expected_type, example_cave):

    result = example_cave.get_type(x, y)

    assert result == expected_type


def test_risk_level(example_cave):
    expected_risk_level = 114

    result = example_cave.get_risk_level()

    assert result == expected_risk_level


@pytest.mark.skip(reason="Time's up!")
def test_get_fastest_time_to_get_target(example_cave):
    expected_fastest_way = 45

    result = example_cave.get_fastest_time_to_get_target()

    assert result == expected_fastest_way
