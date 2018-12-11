import pytest

from day import get_total_power, get_max_power_area_for_size, get_max_power_area


@pytest.fixture()
def example_data():
    example_input = """
    """

    return [line.strip() for line in example_input.splitlines() if line.strip()]


@pytest.mark.parametrize("x, y, area_side, serial_number, total_power_level", [
    (3, 5, 1, 8, 4),
    (122, 79, 1, 57, -5),
    (217, 196, 1, 39, 0),
    (101, 153, 1, 71, 4),
    (33, 45, 3, 18, 29),
    (21, 61, 3, 42, 30),
    (90, 269, 16, 18, 113),
    (232, 251, 12, 42, 119),
])
def test_get_total_power(x, y, area_side, serial_number, total_power_level):

    result = get_total_power(serial_number, x, y, area_side)

    assert result == total_power_level


def test_get_max_power_area_for_size():
    serial_number = 18
    area_side = 3
    expected_top_left_fuel_cell = (33, 45, 3, 29)

    result = get_max_power_area_for_size(serial_number, area_side)

    assert result == expected_top_left_fuel_cell


@pytest.mark.parametrize("x, y, area_side, serial_number, total_power_level", [
    (90, 269, 16, 18, 113),
    (232, 251, 12, 42, 119),
])
def test_get_max_power_area(x, y, area_side, serial_number, total_power_level):

    result = get_max_power_area(serial_number)

    assert result == (x, y, area_side, total_power_level)
