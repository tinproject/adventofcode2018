import pytest


from day import LumberArea, lumber_area_transition


@pytest.fixture()
def example_data():
    example_input = """
    .#.#...|#.
    .....#|##|
    .|..|...#.
    ..|#.....#
    #.#|||#|#|
    ...#.||...
    .|....|...
    ||...#|.#|
    |.||||..|.
    ...#.|..|.
    """

    return [line.strip() for line in example_input.splitlines() if line.strip()]


@pytest.mark.parametrize("x, y, output", [
    (3, 4, '|#.#||.#.'),
    (0, 0, '.....#...'),
    (1, 0, '....#....'),
])
def test_get_surroundings(x, y, output, example_data):
    area = LumberArea(example_data)

    result = area._get_surroundings(x, y)

    assert result == output


def test_get_resource_value_after_10_minutes(example_data):
    minutes = 10
    area = LumberArea(example_data)
    expected_resource_value = 1147

    area.grow(minutes)
    result = area.get_resource_value()

    assert result == expected_resource_value


@pytest.mark.parametrize("input, output", [
    ('.........', '.'),
    ('|||......', '|'),
    ('.|.|...||', '|'),
    ('....|....', '|'),
    ('#||||||||', '|'),
    ('.#..|..##', '#'),
    ('....#..||', '.'),
    ('#...#..||', '#'),
    ('....#....', '.'),

])
def test_lumber_area_transition(input, output):

    result = lumber_area_transition(input)

    assert result == output
