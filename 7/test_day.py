import pytest


@pytest.fixture()
def example_data():
    example_input = """
    Step C must be finished before step A can begin.
    Step C must be finished before step F can begin.
    Step A must be finished before step B can begin.
    Step A must be finished before step D can begin.
    Step B must be finished before step E can begin.
    Step D must be finished before step E can begin.
    Step F must be finished before step E can begin.
    """

    return [line.strip() for line in example_input.splitlines()]


def test_get_instructions_order(example_data):
    pass
