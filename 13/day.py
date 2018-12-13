from dataclasses import dataclass
from enum import Enum, auto
from itertools import count, cycle


@dataclass(eq=True, order=True)
class Coord:
    x: int
    y: int

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __hash__(self):
        return hash((self.x, self.y))


class RailTypes(Enum):
    HORIZONTAL_STRAIGH = auto()
    INTERSECTION = auto()
    VERTICAL_STRAIGH = auto()
    INVERSE_CURVE = auto()
    NORMAL_CURVE = auto()


rail_types_repr = {
    '-': RailTypes.HORIZONTAL_STRAIGH,
    '+': RailTypes.INTERSECTION,
    '|': RailTypes.VERTICAL_STRAIGH,
    '/': RailTypes.INVERSE_CURVE,
    '\\': RailTypes.NORMAL_CURVE,
}


class IntersectionAction(Enum):
    TURN_LEFT = auto()
    STRAIGHT = auto()
    TURN_RIGHT = auto()


class CartDir(Enum):
    RIGHT = Coord(1, 0)
    DOWN = Coord(0, 1)
    LEFT = Coord(-1, 0)
    UP = Coord(0, -1)


intersection_actions = {
    IntersectionAction.STRAIGHT: {
        CartDir.RIGHT: CartDir.RIGHT,
        CartDir.DOWN: CartDir.DOWN,
        CartDir.LEFT: CartDir.LEFT,
        CartDir.UP: CartDir.UP,
    },
    IntersectionAction.TURN_LEFT: {
        CartDir.RIGHT: CartDir.UP,
        CartDir.DOWN: CartDir.RIGHT,
        CartDir.LEFT: CartDir.DOWN,
        CartDir.UP: CartDir.LEFT,
    },
    IntersectionAction.TURN_RIGHT: {
        CartDir.RIGHT: CartDir.DOWN,
        CartDir.DOWN: CartDir.LEFT,
        CartDir.LEFT: CartDir.UP,
        CartDir.UP: CartDir.RIGHT,
    },
}

curve_actions = {
    RailTypes.INVERSE_CURVE: {
        CartDir.RIGHT: CartDir.UP,
        CartDir.DOWN: CartDir.LEFT,
        CartDir.LEFT: CartDir.DOWN,
        CartDir.UP: CartDir.RIGHT,
    },
    RailTypes.NORMAL_CURVE: {
        CartDir.RIGHT: CartDir.DOWN,
        CartDir.DOWN: CartDir.RIGHT,
        CartDir.LEFT: CartDir.UP,
        CartDir.UP: CartDir.LEFT,
    },
    RailTypes.HORIZONTAL_STRAIGH: {
        CartDir.RIGHT: CartDir.RIGHT,
        CartDir.LEFT: CartDir.LEFT,
    },
    RailTypes.VERTICAL_STRAIGH: {
        CartDir.DOWN: CartDir.DOWN,
        CartDir.UP: CartDir.UP,
    },
}


class Cart:
    def __init__(self, x, y, cart_char, rails):
        self.position = Coord(x, y)
        self.direction = self._get_dir_vector(cart_char)
        self.intersection_state = cycle((
            IntersectionAction.TURN_LEFT,
            IntersectionAction.STRAIGHT,
            IntersectionAction.TURN_RIGHT
        ))
        self.rails = rails
        self.crashed = False

    def tick(self):
        self.position += self.dir_vector
        self._recalc_direction()

    @property
    def dir_vector(self):
        return self.direction.value

    def _recalc_direction(self):
        rail = self.rails[self.position]
        if rail == RailTypes.INTERSECTION:
            action = next(self.intersection_state)
            direction = intersection_actions[action][self.direction]
        elif rail in RailTypes:
            direction = curve_actions[rail][self.direction]
        else:
            direction = self.direction
        self.direction = direction

    @staticmethod
    def _get_dir_vector(cart_char):
        if cart_char == r'>':
            dir_vector = CartDir.RIGHT
        elif cart_char == r'v':
            dir_vector = CartDir.DOWN
        elif cart_char == r'<':
            dir_vector = CartDir.LEFT
        elif cart_char == r'^':
            dir_vector = CartDir.UP
        else:
            raise ValueError(f"Bad cart: {cart_char}")
        return dir_vector

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.position < other.position

    def __repr__(self):
        return f"Cart at {self.position}, direction: {self.direction}, rail: {self.rails[self.position]}"


def get_data(filename='./input'):
    carts = []
    rails = dict()
    with open(filename, 'rt') as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line):
                if c in "-+|/\\":
                    # rail coord
                    rails[Coord(x, y)] = rail_types_repr[c]
                elif c in "^v":
                    rails[Coord(x, y)] = RailTypes.VERTICAL_STRAIGH
                    carts.append(Cart(x, y, c, rails))
                elif c in "<>":
                    rails[Coord(x, y)] = RailTypes.HORIZONTAL_STRAIGH
                    carts.append(Cart(x, y, c, rails))
                elif c in " ":
                    pass
                elif c in "\n":
                    break
                else:
                    raise ValueError(f"Unkown character {c}")
    return carts, rails


def check_crash(carts):
    sorted_positions = sorted(carts)
    for a, b in zip(sorted_positions[:-1], sorted_positions[1:]):
        if a == b:
            a.crashed = True
            b.crashed = True
            return True
    return False


def solve_part_one(carts, rails):
    for _ in count(1):
        sorted_carts = sorted(carts)
        for cart in sorted_carts:
            cart.tick()
            if check_crash(carts):
                return cart.position


def solve_part_two(carts, rails):
    for _ in count(1):
        carts = sorted(cart for cart in carts if not cart.crashed)
        crashes = []
        for cart in carts:
            cart.tick()
            crashes.append(check_crash(carts))

        if any(crashes) and len(carts) <= 3:
            # Two crashed, only one remaining
            return [cart for cart in carts if not cart.crashed][0]


def solve():
    # Part 1
    carts, rails = get_data()
    crash = solve_part_one(carts, rails)
    print(f"Part1 - The first cart that crash do ti at position: {crash}")

    # Part 2
    carts, rails = get_data()
    cart_remaining = solve_part_two(carts, rails)
    print(f"Part2 - The remaining cart is at position: {cart_remaining.position}")


if __name__ == "__main__":
    solve()
