from collections import deque
from copy import copy
from dataclasses import dataclass
from operator import attrgetter
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
        coords = self.ground.keys()
        self.min = Coord(min(coords, key=attrgetter('x')).x, min(coords, key=attrgetter('y')).y)
        self.max = Coord(max(coords, key=attrgetter('x')).x, max(coords, key=attrgetter('y')).y)
        self.water_spring = water_spring
        self.ground[water_spring] = WATER_SPRING

    def self_is(self, coord, *args):
        return self[coord] in args

    def up_is(self, coord, *args):
        return self[coord.up()] in args

    def down_is(self, coord, *args):
        return self[coord.down()] in args

    def left_is(self, coord, *args):
        return self[coord.left()] in args

    def right_is(self, coord, *args):
        return self[coord.right()] in args

    def water_flow(self, start=None):
        if start is None:
            start: Coord = self.water_spring

        flow_to_process = deque([start])
        # print(f"min {self.min} max {self.max}")

        while flow_to_process:
            current = flow_to_process.popleft()
            # print(f"=======>>> Processing {current}")

            # if self.self_is(current, WATER_SPRING):
            #     print(f"==> Don't process water spring {current}")
            #     continue

            if self.self_is(current, FLOWING_WATER) and self.down_is(current, FLOWING_WATER):
                # print(f"**** Ignore current point: {current}")
                # print(f"****   {self[current.up()]}")
                # print(f"****  {self[current.left()]}{self[current]}{self[current.right()]}")
                # print(f"****   {self[current.down()]}")

                continue

            if self.self_is(current, STILL_WATER):
                # print(f"==> Process current already drowned {current}")
                while self.up_is(current, STILL_WATER):
                    current = current.up()
                if self.up_is(current, FLOWING_WATER):
                    # print(f"==============>> Append to process up {current.up()}")
                    flow_to_process.append(current.up())
                continue

            if self.down_is(current, SAND, FLOWING_WATER):
                # print(f"==> Water flowing down in {current}")
                down = current.down()

                while self.down_is(down, SAND, FLOWING_WATER):
                    # print(down)
                    self[down] = FLOWING_WATER
                    if down.y >= self.max.y:
                        # print(f"Out of range!!! {down}")
                        break
                    down = down.down()
                self[down] = FLOWING_WATER
                if not down.y >= self.max.y:
                    flow_to_process.append(down)
                    # print(f"==============>> Append to process down {down}")
                continue

            if self.down_is(current, CLAY, STILL_WATER):
                # print(f"==> Water flowing sides in {current}")
                while self.down_is(current, CLAY, STILL_WATER):

                    # print(f"Looking rigth from {current}")
                    coord = copy(current)
                    right_end = None
                    for x in range(current.x, self.max.x+2):
                        if self.right_is(coord, SAND, FLOWING_WATER) and self.down_is(coord, CLAY, STILL_WATER):
                            coord = coord.right()
                            continue
                        else:
                            # found right end
                            right_end = coord
                            break
                    # print(f"Looking left from {current}")
                    coord = copy(current)
                    left_end = None
                    for x in range(current.x, self.min.x-1, -1):
                        if self.left_is(coord, SAND, FLOWING_WATER) and self.down_is(coord, CLAY, STILL_WATER):
                            coord = coord.left()
                            continue
                        else:
                            # found right end
                            left_end = coord
                            break

                    # print(f"Water spans Left {left_end} {self[left_end]} Right {right_end} {self[right_end]}")
                    if self[left_end.left()] == CLAY and self[right_end.right()] == CLAY:
                        # print(f"Filling with water")
                        for x in range(left_end.x, right_end.x+1):
                            self[Coord(x, left_end.y)] = STILL_WATER
                        current = current.up()
                        # print(f"Up {current}")
                    else:
                        # print(f"Flowing water")
                        for x in range(left_end.x, right_end.x+1):
                            self[Coord(x, left_end.y)] = FLOWING_WATER

                        if self[left_end.left()] in (SAND, FLOWING_WATER):
                            # print(f"==============>> Append to process left {left_end}")
                            flow_to_process.append(left_end)
                        if self[right_end.right()] in (SAND, FLOWING_WATER):
                            # print(f"==============>> Append to process right {right_end}")
                            flow_to_process.append(right_end)
                        break
                continue

            # print(f"**** Can't process current point: {current}")
            # print(f"****   {self[current.up()]}")
            # print(f"****  {self[current.left()]}{self[current]}{self[current.right()]}")
            # print(f"****   {self[current.down()]}")

            continue

    def get_water_tiles_count(self):
        count = sum(1 for t, v in self.ground.items() if
                    self.min.y <= t.y <= self.max.y and v in (STILL_WATER, FLOWING_WATER))
        return count

    def get_still_water_tiles_count(self):
        count = sum(1 for t, v in self.ground.items() if
                    self.min.y <= t.y <= self.max.y and v in (STILL_WATER))
        return count

    def __getitem__(self, item):
        return self.ground.get(item, SAND)

    def __setitem__(self, key, value):
        self.ground[key] = value

    def __repr__(self):
        lines = [
            "      " + "".join(str(x % 1000 // 100) for x in range(self.min.x-3, self.max.x+3 + 1)),
            "      " + "".join(str(x % 100 // 10) for x in range(self.min.x-3, self.max.x+3 + 1)),
            "      " + "".join(str(x % 10) for x in range(self.min.x-3, self.max.x+3 + 1)),
        ]
        # for y in range(60):  # self.max.y+1):
        for y in range(self.max.y+10):
            lines.append(f"L{y:04} " + "".join(self[Coord(x, y)] for x in range(self.min.x-3, self.max.x+3+1)))
        return "\n".join(lines)


def solve():
    data = get_data()

    # Part 1
    ground = Ground(data)
    ground.water_flow()
    water_tiles = ground.get_water_tiles_count()
    ground_slice = repr(ground)
    print(ground_slice)
    print("")
    print(f"Part1 - The number of tiles the water can reach is: {water_tiles}")

    # Part 2
    still_water_tiles = ground.get_still_water_tiles_count()
    print(f"Part2 - The number of water tiles after draining is: {still_water_tiles}")


if __name__ == "__main__":
    solve()
