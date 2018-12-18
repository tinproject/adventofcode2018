from collections import deque
from copy import copy
from dataclasses import dataclass
from operator import itemgetter, attrgetter
import re


@dataclass(eq=True, order=True)
class Coord:
    x: int
    y: int

    def up(self):
        return Coord(self.x, self.y-1)

    def down(self):
        return Coord(self.x, self.y+1)

    def left(self):
        return Coord(self.x-1, self.y)

    def right(self):
        return Coord(self.x+1, self.y)

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"{self.x},{self.y}"


RE_CLAY_VEIN = re.compile(r"(?P<axis>[xy])=(?P<fix>\d+),\s[xy]=(?P<low>\d+)\.\.(?P<high>\d+)")

SAND = '.'
CLAY = '#'
STILL_WATER = '~'
FLOWING_WATER = '|'
WATER_SPRING = '+'


def get_data():
    with open('./input', 'rt') as f:
        values = [line.strip() for line in f.readlines()]
    return values


def parse_input(data):
    ground = dict()
    for clay_vein in data:
        cv = RE_CLAY_VEIN.match(clay_vein)
        if cv:
            axis = cv.group('axis')
            fix = int(cv.group('fix'))
            low = int(cv.group('low'))
            high = int(cv.group('high'))
            for i in range(low, high+1):
                if axis == 'x':
                    ground[Coord(fix, i)] = CLAY
                else:
                    ground[Coord(i, fix)] = CLAY
    return ground


class Ground:
    def __init__(self, data, water_spring=Coord(500, 0)):
        self.ground = parse_input(data)
        self.water_spring = water_spring
        self.ground[water_spring] = WATER_SPRING
        coords = self.ground.keys()
        self.min = Coord(min(coords, key=attrgetter('x')).x, min(coords, key=attrgetter('y')).y)
        self.max = Coord(max(coords, key=attrgetter('x')).x, max(coords, key=attrgetter('y')).y)

    def water_flow(self, start=None):
        if start is None:
            start: Coord = self.water_spring

        current = start
        for i in range(100):
            current_square = self[current]
            down = current.down()
            bottom_square = self[down]
            if current_square == STILL_WATER:
                current = current.up()
            elif bottom_square == SAND:
                current = down
                self[current] = FLOWING_WATER
            elif bottom_square in (CLAY, STILL_WATER):
                # print(f"Looking rigth from {current}")
                coord = copy(current)
                right_end = None
                for x in range(current.x, self.max.x+1):
                    right_coord = coord.right()
                    right_square = self[right_coord]
                    bottom_square = self[coord.down()]
                    if right_square == SAND and bottom_square in (CLAY, STILL_WATER):
                        coord = right_coord
                        continue
                    else:
                        # found right end
                        right_end = coord
                        break
                # print(f"Looking left from {current}")
                coord = copy(current)
                left_end = None
                for x in range(current.x, self.min.x-1, -1):
                    left_coord = coord.left()
                    left_square = self[left_coord]
                    bottom_square = self[coord.down()]
                    if left_square == SAND and bottom_square in (CLAY, STILL_WATER):
                        coord = left_coord
                        continue
                    else:
                        # found right end
                        left_end = coord
                        break

                # print(f"Left {left_end} Right {right_end}")
                if self[left_end.left()] == CLAY and self[right_end.right()] == CLAY:
                    # Fill with water
                    for x in range(left_end.x, right_end.x+1):
                        self[Coord(x, left_end.y)] = STILL_WATER
                else:
                    # Flowing water
                    for x in range(left_end.x, right_end.x+1):
                        self[Coord(x, left_end.y)] = FLOWING_WATER


    def __getitem__(self, item):
        return self.ground.get(item, SAND)

    def __setitem__(self, key, value):
        self.ground[key] = value

    def __repr__(self):
        lines = []
        for y in range(50):  # self.max.y+1):
            lines.append("".join(self[Coord(x, y)] for x in range(self.min.x-3, self.max.x+3+1)))
        return "\n".join(lines)


def solve():
    data = get_data()

    # Part 1
    ground = Ground(data)
    ground.water_flow()
    print(ground)
    print(f"Part1 - ... is: {None}")

    # Part 2
    print(f"Part2 - ... is: {None}")


if __name__ == "__main__":
    solve()
