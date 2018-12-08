import pytest


from day import parse_input, get_node_metadata, get_metadata_sum, get_node_value


@pytest.fixture()
def example_input():
    example_input = """
    2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
    """

    return [line.strip() for line in example_input.splitlines() if line.strip()]


def test_parse_input(example_input):
    expected_input = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]

    result = parse_input(example_input)

    assert result == expected_input


@pytest.fixture()
def example_data(example_input):
    return parse_input(example_input)


def test_node_metadata(example_data):
    expected_output = [10, 11, 12, 99, 2, 1, 1, 2]
    next_index = 16

    result = get_node_metadata(example_data)

    assert result == (expected_output, next_index)


def test_node_no_child():
    node = [0, 1, 99]
    expected_metadata = [99]
    expected_next_index = 3

    result = get_node_metadata(node)

    assert result == (expected_metadata, expected_next_index)


def test_node_one_child():
    node = [1, 1, 0, 1, 99, 2]
    expected_metadata = [99, 2]
    expected_next_index = 6

    result = get_node_metadata(node)

    assert result == (expected_metadata, expected_next_index)


def test_get_metadata_sum(example_data):
    expected_output = 138

    result = get_metadata_sum(example_data)

    assert result == expected_output


def test_get_node_value(example_data):
    expected_value = 66
    expected_next_index = 16

    result = get_node_value(example_data)

    assert result == (expected_value, expected_next_index)


def test_get_node_value_no_childs():
    node = [0, 3, 10, 11, 12]
    expected_value = 33
    expected_next_index = 5

    result = get_node_value(node)

    assert result == (expected_value, expected_next_index)
