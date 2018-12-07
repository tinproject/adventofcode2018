import pytest


from day import get_instructions_order, parse_instruction, get_step_time, get_construction_time


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

    return [line.strip() for line in example_input.splitlines() if line.strip()]


def test_get_instructions_order(example_data):
    expected_order = "CABDFE"

    result = get_instructions_order(example_data)

    assert result == expected_order


def test_parse_instruction():
    example_instruction = "Step C must be finished before step A can begin."
    expected_output = ("C", "A")

    result = parse_instruction(example_instruction)

    assert result == expected_output


@pytest.mark.parametrize("step,setup,output", [
    ('A', 60, 61),
    ('A', 0, 1),
    ('Z', 60, 86),
    ('F', 0, 6),
])
def test_get_step_time(step, setup, output):
    result = get_step_time(step, setup)

    assert result == output


def test_get_construction_time(example_data):
    num_workers = 2
    setup_time = 0
    expected_construction_time = 15

    result = get_construction_time(example_data, num_workers, setup_time)

    assert result == expected_construction_time
