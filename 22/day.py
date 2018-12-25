from itertools import product
from functools import lru_cache


MOUTH = 'M'
TARGET = 'T'
ROCKY = '.'
WET = '='
NARROW = '|'

TOOL_CLIMBING = 'C'
TOOL_TORCH = 'H'
TOOL_NONE = 'N'


class Cave:
    REGION_TYPE = {
        0: ROCKY,
        1: WET,
        2: NARROW,
    }
    RISK_LEVEL = {
        ROCKY: 0,
        MOUTH: 0,
        TARGET: 0,
        WET: 1,
        NARROW: 2,
    }

    def __init__(self, depth, target, mouth=(0, 0)):
        self.depth = depth
        self.target = target
        self.mouth = mouth
        self.tiles = {}
        self[mouth] = MOUTH
        self[target] = TARGET

    @lru_cache()
    def get_geological_index(self, x, y):
        if (x, y) == self.mouth:
            return 0
        if (x, y) == self.target:
            return 0
        if y == 0:
            return x * 16807
        if x == 0:
            return y * 48271

        return self.get_erosion_level(x-1, y) * self.get_erosion_level(x, y-1)

    @lru_cache()
    def get_erosion_level(self, x, y):
        erosion_level = (self.get_geological_index(x, y) + self.depth) % 20183
        return erosion_level

    @lru_cache()
    def get_type(self, x, y):
        erosion_level = self.get_erosion_level(x, y)
        t = erosion_level % 3
        return self.REGION_TYPE[t]

    def get_risk_level(self):
        risk_level = sum(self.RISK_LEVEL[self[(x, y)]] for y, x in product(
            range(self.mouth[1], self.target[1]+1),
            range(self.mouth[0], self.target[0]+1),
        ))
        return risk_level

    def get_fastest_time_to_get_target(self):
        raise NotImplementedError

    def __setitem__(self, point, value):
        self.tiles[point] = value

    def __getitem__(self, point):
        value = self.tiles.get(point, None)
        if value is None:
            value = self.get_type(*point)
            self[point] = value
        return value

    def __repr__(self):
        cave = []
        for y in range(self.mouth[1], self.target[1]+1):
            cave.append("".join(self[(x, y)] for x in range(self.mouth[0], self.target[0]+1)))
        return "\n".join(cave)


def solve():
    depth = 11820
    target = (7, 782)

    # Part 1
    cave = Cave(depth, target)
    print(cave)
    risk_level = cave.get_risk_level()
    print(f"Part1 - The risk level of the smalles rectangle that include the mouth and target is: {risk_level}")

    # Part 2
    fastest_time = cave.get_fastest_time_to_get_target()
    print(f"Part2 - The fewest number of minutes to get the target are: {fastest_time}")


if __name__ == "__main__":
    solve()
