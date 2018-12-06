import pytest

from day import (
    get_coordinates, get_bounding_box, point_has_infinite_area, get_points_with_infinite_area,
    distance, get_largest_area, get_region_size_with_less_distance, get_cumulative_distance
)


input_data = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""


def test_get_coordinates():
    coords = get_coordinates(input_data.splitlines())

    assert len(coords) == 6
    assert (1, 1) in coords


def test_get_bounding_box():
    coords = get_coordinates(input_data.splitlines())

    result = get_bounding_box(coords)

    assert result == [(1, 1), (8, 9)]


@pytest.mark.parametrize("point, output", [
    ((1, 1), True),
    ((1, 6), True),
    ((8, 3), True),
    ((3, 4), False),
    ((5, 5), False),
    ((8, 9), True),
])
def test_point_has_infinite_area(point, output):
    coords = get_coordinates(input_data.splitlines())

    result = point_has_infinite_area(coords, point)

    assert result == output


def test_get_points_with_infinite_area():
    coords = get_coordinates(input_data.splitlines())
    expected_points = [(1, 1), (1, 6), (8, 3), (8, 9)]

    result = get_points_with_infinite_area(coords)

    assert result == expected_points


@pytest.mark.parametrize("p1, p2, output", [
    ((1, 1), (0, 0), 2),
    ((1, 1), (1, 2), 1),
    ((1, 1), (2, 1), 1),
    ((1, 1), (2, 2), 2),
    ((1, 1), (3, 3), 4),
    ((2, 2), (1, 1), 2),
    ((0, 0), (1, 1), 2),
    ((1, 3), (4, 2), 4),
    ((1, 3), (4, 4), 4),
    ((1, 3), (-2, 4), 4),
    ((4, 2), (1, 3), 4),
])
def test_distance(p1, p2, output):
    result = distance(p1, p2)

    assert result == output


def test_get_largest_area():
    coords = get_coordinates(input_data.splitlines())
    largest_area = 17

    result = get_largest_area(coords)

    assert result == largest_area


def test_get_region_size_with_less_distance():
    coords = get_coordinates(input_data.splitlines())
    max_cum_distance = 32
    resgion_size = 16

    result = get_region_size_with_less_distance(coords, max_cum_distance)

    assert result == resgion_size


def test_get_cumulative_distance():
    points = get_coordinates(input_data.splitlines())
    place = (4, 3)
    cum_distance = 30

    result = get_cumulative_distance(place, points)

    assert result == cum_distance
