import pytest


from day import Coord, CLAY, parse_input, Ground


@pytest.fixture()
def example_data():
    example_input = """
    x=495, y=2..7
    y=7, x=495..501
    x=501, y=3..7
    x=498, y=2..4
    x=506, y=1..2
    x=498, y=10..13
    x=504, y=10..13
    y=13, x=498..504
    """

    return [line.strip() for line in example_input.splitlines() if line.strip()]


@pytest.mark.parametrize("coord", [
    (495, 2),
    (495, 5),
    (495, 7),
    (501, 7),
    (500, 13),
])
def test_parse_input(coord, example_data):
    point = Coord(*coord)

    ground = parse_input(example_data)

    assert ground[point] == CLAY


@pytest.mark.parametrize("coord", [
    (495, 2),
    (495, 5),
    (495, 7),
    (501, 7),
    (500, 13),
])
def test_ground_input(coord, example_data):
    water_spring = Coord(500, 0)
    point = Coord(*coord)

    ground = Ground(example_data, water_spring)

    assert ground[point] == CLAY


def test_get_water_tiles_count(example_data):
    water_spring = Coord(500, 0)
    ground = Ground(example_data, water_spring)
    expected_count = 57

    ground.water_flow()
    result = ground.get_water_tiles_count()

    assert result == expected_count
