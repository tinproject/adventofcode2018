import pytest


from day import parse_data, get_highest_score, calc_circular_index


@pytest.fixture()
def example_data():
    example_input = """
    412 players; last marble is worth 71646 points
    """
    return [line.strip() for line in example_input.splitlines() if line.strip()]


def test_parse_data(example_data):
    expected_players = 412
    expected_last_marble_points = 71646

    result = parse_data(example_data[0])

    assert result == (expected_players, expected_last_marble_points)


@pytest.mark.parametrize("players, last_marble_points, highest_score", [
    (9, 25, 32),
    (10, 1618, 8317),
    (13, 7999, 146373),
    (17, 1104, 2764),
    (21, 6111, 54718),
    (30, 5807, 37305),
])
def test_get_highest_score(players, last_marble_points, highest_score):

    result = get_highest_score(players, last_marble_points)

    assert result == highest_score


@pytest.mark.parametrize("playground, current_marble_index, delta, index", [
    ([0], 0, +2, 1),
    ([0, 1], 1, +2, 1),
    ([0, 2, 1, 3], 3, +2, 1),
    ([0, 4, 2, 1, 3], 1, +2, 3),
])
def test_calc_circular_index(playground, current_marble_index, delta, index):

    result = calc_circular_index(playground, current_marble_index, delta)

    assert result == index
