import pytest


@pytest.fixture()
def example_data():
    example_input = """
    """

    return [line.strip() for line in example_input.splitlines() if line.strip()]
