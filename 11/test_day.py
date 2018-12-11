import pytest

from day import get_power_level, get_total_power, get_max_power_area


@pytest.fixture()
def example_data():
    example_input = """
    """

    return [line.strip() for line in example_input.splitlines() if line.strip()]


@pytest.mark.parametrize("x, y, serial_number, power_level", [
    (3, 5, 8, 4),
    (122, 79, 57, -5),
    (217, 196, 39, 0),
    (101, 153, 71, 4),
])
def test_get_power_level(serial_number, x, y, power_level):

    result = get_power_level(serial_number, x, y)

    assert result == power_level


@pytest.mark.parametrize("x, y, serial_number, total_power_level", [
    (33, 45, 18, 29),
    (21, 61, 42, 30),
])
def test_get_total_power(x, y, serial_number, total_power_level):

    result = get_total_power(serial_number, x, y)

    assert result == total_power_level


def test_get_max_power_area():
    serial_number = 18
    expected_top_left_fuel_cell = (33, 45, 29)

    result = get_max_power_area(serial_number)

    assert result == expected_top_left_fuel_cell
