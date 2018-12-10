from collections import namedtuple
from dataclasses import dataclass
from operator import itemgetter, attrgetter
import re


Velocity = namedtuple('Point', ['dx', 'dy'])


@dataclass(eq=True, order=True)
class Point:
    x: int
    y: int


class LightPoint:
    def __init__(self, origin, velocity):
        self.origin = origin
        self.velocity = velocity

    _RE = re.compile(r".*position=<\s*(?P<x>-?\d+),\s+(?P<y>-?\d+).*velocity=<\s*(?P<dx>-?\d+),\s+(?P<dy>-?\d+).*$")

    @classmethod
    def from_input(cls, input_data):
        m = cls._RE.match(input_data)
        x = int(m.group('x'))
        y = int(m.group('y'))
        dx = int(m.group('dx'))
        dy = int(m.group('dy'))
        return cls(Point(x, y), Velocity(dx, dy))

    def position_at_time(self, t):
        x = self.origin.x + self.velocity.dx * t
        y = self.origin.y + self.velocity.dy * t
        return Point(x, y)

    def __eq__(self, other):
        return self.origin == other.origin and self.velocity == other.velocity

    def __lt__(self, other):
        # Not much sense physically
        return self.origin < other.origin and self.velocity < other.velocity


def get_data():
    with open('./input', 'rt') as f:
        values = [line.strip() for line in f.readlines()]
    return values


def get_lightpoints(data):
    lightpoints = []
    for input_data in data:
        lightpoints.append(LightPoint.from_input(input_data))
    return lightpoints


def get_points_at_ts(lightpoints, ts):
    points = [lp.position_at_time(ts) for lp in lightpoints]

    x_coords = [p.x for p in points]
    y_coords = [p.y for p in points]
    dx = abs(max(x_coords) - min(x_coords) + 1)
    dy = abs(max(y_coords) - min(y_coords) + 1)

    return points, dx, dy


def get_message_ts(lightpoints):
    variations = []
    for ts in range(20000):
        _, dx, dy = get_points_at_ts(lightpoints, ts)
        if dy <= 50:
            v = (dx, dy, ts)
            variations.append(v)

    message_ts = min(variations, key=itemgetter(1))[2]
    return message_ts


def get_sky_at_ts(ligthpoints, ts):
    points, _, _ = get_points_at_ts(ligthpoints, ts)

    min_x = min(points, key=attrgetter('x')).x - 1
    max_x = max(points, key=attrgetter('x')).x + 1
    dx = max_x - min_x + 1
    min_y = min(points, key=attrgetter('y')).y - 1
    max_y = max(points, key=attrgetter('y')).y + 1
    dy = max_y - min_y + 1

    print(dx, dy)

    sky = []
    for _ in range(dy):
        sky.append(['_'] * dx)

    for point in points:
        sky[point.y - min_y][point.x - min_x] = "#"

    for i, l in enumerate(sky):
        sky[i] = "".join(l)
        print(sky[i])


def solve():
    data = get_data()
    lightpoints = get_lightpoints(data)
    # Part 1
    message_ts = get_message_ts(lightpoints)
    print(f"Part1 - The message will show at time ts={message_ts}. The solution is... (read the message)")
    get_sky_at_ts(lightpoints, message_ts)

    # Part 2
    print(f"Part2 - ... is: {None}")


if __name__ == "__main__":
    solve()
