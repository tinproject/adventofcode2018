import pytest


from day import Point, Velocity, LightPoint, get_lightpoints, get_points_at_ts, get_message_ts


@pytest.fixture()
def example_data():
    example_input = """
    position=< 9,  1> velocity=< 0,  2>
    position=< 7,  0> velocity=<-1,  0>
    position=< 3, -2> velocity=<-1,  1>
    position=< 6, 10> velocity=<-2, -1>
    position=< 2, -4> velocity=< 2,  2>
    position=<-6, 10> velocity=< 2, -2>
    position=< 1,  8> velocity=< 1, -1>
    position=< 1,  7> velocity=< 1,  0>
    position=<-3, 11> velocity=< 1, -2>
    position=< 7,  6> velocity=<-1, -1>
    position=<-2,  3> velocity=< 1,  0>
    position=<-4,  3> velocity=< 2,  0>
    position=<10, -3> velocity=<-1,  1>
    position=< 5, 11> velocity=< 1, -2>
    position=< 4,  7> velocity=< 0, -1>
    position=< 8, -2> velocity=< 0,  1>
    position=<15,  0> velocity=<-2,  0>
    position=< 1,  6> velocity=< 1,  0>
    position=< 8,  9> velocity=< 0, -1>
    position=< 3,  3> velocity=<-1,  1>
    position=< 0,  5> velocity=< 0, -1>
    position=<-2,  2> velocity=< 2,  0>
    position=< 5, -2> velocity=< 1,  2>
    position=< 1,  4> velocity=< 2,  1>
    position=<-2,  7> velocity=< 2, -2>
    position=< 3,  6> velocity=<-1, -1>
    position=< 5,  0> velocity=< 1,  0>
    position=<-6,  0> velocity=< 2,  0>
    position=< 5,  9> velocity=< 1, -2>
    position=<14,  7> velocity=<-2,  0>
    position=<-3,  6> velocity=< 2, -1>
    """

    return [line.strip() for line in example_input.splitlines() if line.strip()]


def test_lightpoint_from_input():
    input_data = "position=< 9,  1> velocity=< 0,  2>"
    expected_point = Point(9, 1)
    expected_velocity = Velocity(0, 2)

    result = LightPoint.from_input(input_data)

    assert result.origin == expected_point
    assert result.velocity == expected_velocity


def test_lightpoint_position_at_t0():
    input_data = "position=< 9,  1> velocity=< 0,  2>"
    ts = 0

    lp = LightPoint.from_input(input_data)

    result = lp.position_at_time(ts)

    assert result == lp.origin


def test_get_lightpoints(example_data):
    lp = LightPoint(Point(-2, 2), Velocity(2, 0))

    result = get_lightpoints(example_data)

    assert lp in result


def test_get_points_at_ts(example_data):
    lightpoints = get_lightpoints(example_data)
    ts = 0
    point = Point(-2, 2)

    result, _, _ = get_points_at_ts(lightpoints, ts)

    assert point in result


def test_get_points_at_ts_boundary(example_data):
    lightpoints = get_lightpoints(example_data)
    ts = 3
    expected_dx = 10
    expected_dy = 8

    _, dx, dy = get_points_at_ts(lightpoints, ts)

    assert (dx, dy) == (expected_dx, expected_dy)


def test_get_message_ts(example_data):
    lightpoints = get_lightpoints(example_data)
    expected_message_ts = 3

    result = get_message_ts(lightpoints)

    assert result == expected_message_ts
