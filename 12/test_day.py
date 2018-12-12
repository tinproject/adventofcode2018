import pytest


from day import parse_input, get_next_state, get_pot_number_sums_after_n_gens


@pytest.fixture()
def example_data():
    example_input = """
    initial state: #..#.#..##......###...###

    ..... => .
    ....# => .
    ...#. => .
    ...## => #
    ..#.. => #
    ..#.# => .
    ..##. => .
    ..### => .
    .#... => #
    .#..# => .
    .#.#. => #
    .#.## => #
    .##.. => #
    .##.# => .
    .###. => .
    .#### => #
    #.... => .
    #...# => .
    #..#. => .
    #..## => .
    #.#.. => .
    #.#.# => #
    #.##. => .
    #.### => #
    ##... => .
    ##..# => .
    ##.#. => #
    ##.## => #
    ###.. => #
    ###.# => #
    ####. => #
    ##### => .

    """
    return [line.strip() for line in example_input.splitlines() if line.strip()]


def test_parse_data(example_data):

    expected_initial_value = "#..#.#..##......###...###"

    initial_value, spread_patterns = parse_input(example_data)

    assert initial_value == expected_initial_value
    assert '.#..#' in spread_patterns
    assert spread_patterns['#.###'] == '#'


def test_get_next_state(example_data):
    initial_state, spread_patterns = parse_input(example_data)
    expected_state = "#...#....#.....#..#..#..#"

    result = get_next_state(initial_state, spread_patterns)

    assert result == expected_state


def test_get_pot_number_sum_after_n_gens(example_data):
    initial_state, spread_patterns = parse_input(example_data)
    expected_value = 325
    gen = 20
    pot_number_sums = get_pot_number_sums_after_n_gens(initial_state, spread_patterns, gen)

    result = pot_number_sums[gen]

    assert result == expected_value
