import pytest


from day import get_data, Coord, Cart, solve_part_one, RailTypes, CartDir


@pytest.fixture()
def example_data():
    filename = './test_input'

    return get_data(filename)


def test_input_data(example_data):
    carts, rails = example_data

    assert len(carts) == 2
    assert len(rails) == 48
    assert rails[Coord(0, 0)] == RailTypes.INVERSE_CURVE
    assert rails[Coord(0, 4)] == RailTypes.NORMAL_CURVE
    assert rails[Coord(4, 2)] == RailTypes.INTERSECTION
    assert rails[Coord(0, 1)] == RailTypes.VERTICAL_STRAIGH
    assert rails[Coord(9, 3)] == RailTypes.VERTICAL_STRAIGH
    assert rails[Coord(1, 0)] == RailTypes.HORIZONTAL_STRAIGH
    assert rails[Coord(2, 0)] == RailTypes.HORIZONTAL_STRAIGH


def test_cart(example_data):
    carts, rails = example_data
    expected_position = Coord(2, 0)
    expected_vector = Coord(1, 0)
    cart = Cart(2, 0, '>', rails)

    assert cart.position == expected_position
    assert cart.dir_vector == expected_vector

    expected_new_position = Coord(3, 0)

    cart.tick()

    assert cart.position == expected_new_position


@pytest.mark.parametrize("x, y, c, expected_position, expected_direction", [
    (0, 1, '^', Coord(0, 0), CartDir.RIGHT),
    (0, 0, '>', Coord(1, 0), CartDir.RIGHT),
    (3, 0, '>', Coord(4, 0), CartDir.DOWN),
    (4, 0, 'v', Coord(4, 1), CartDir.DOWN),
    (4, 1, 'v', Coord(4, 2), CartDir.RIGHT),
    (4, 3, 'v', Coord(4, 4), CartDir.LEFT),
    (1, 4, '<', Coord(0, 4), CartDir.UP),
    (0, 4, '^', Coord(0, 3), CartDir.UP),
    (0, 3, 'v', Coord(0, 4), CartDir.RIGHT),
    (3, 4, '>', Coord(4, 4), CartDir.UP),
    (4, 1, '^', Coord(4, 0), CartDir.LEFT),
    (1, 0, '<', Coord(0, 0), CartDir.DOWN),
])
def test_cart_position(x, y, c, expected_position, expected_direction, example_data):
    _, rails = example_data
    cart = Cart(x, y, c, rails)
    cart.tick()

    assert cart.position == expected_position
    assert cart.direction == expected_direction


def test_intersections(example_data):
    _, rails = example_data
    cart = Cart(4, 1, 'v', rails)
    cart.tick()

    assert cart.position == Coord(4, 2)
    assert cart.direction == CartDir.RIGHT

    cart.tick()
    cart.tick()
    cart.tick()

    assert cart.position == Coord(7, 2)
    assert cart.direction == CartDir.RIGHT

    cart.tick()
    cart.tick()
    cart.tick()
    assert cart.direction == CartDir.DOWN

    cart.tick()

    assert cart.position == Coord(9, 4)
    assert cart.direction == CartDir.LEFT

    cart.tick()
    cart.tick()
    cart.tick()

    assert cart.direction == CartDir.UP

    cart.tick()

    assert cart.position == Coord(7, 2)
    assert cart.direction == CartDir.LEFT


def test_solve_part_one(example_data):
    carts, rails = example_data
    expected_point = Coord(7, 3)

    result = solve_part_one(carts, rails)

    assert result == expected_point
