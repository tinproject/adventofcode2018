from functools import reduce
from itertools import product
from operator import itemgetter


INITIAL_ROOM = 'X'
ROOM = '.'
WALL = '#'
UNKNOWN = '?'
VERTICAL_DOOR = '|'
HORIZONTAL_DOOR = '-'
EMPTY = ' '

NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'
OPEN_REGEX = '^'
CLOSE_REGEX = '$'
OPEN_BRANCH = '('
CLOSE_BRANCH = ')'
BRANCH = '|'

class Maze:
    def __init__(self, regex):
        self.regex = regex
        self.initial_position = (0, 0)
        self.tiles = {self.initial_position: INITIAL_ROOM}
        self.distances = {self.initial_position: 0}
        self.map_maze()

    def map_maze(self):
        self.position = self.initial_position
        self._map_pos()
        self.branches = []
        for d in self.regex:
            if d in (OPEN_REGEX, OPEN_BRANCH):
                self.branches.append(self.position)
            elif d in (BRANCH,):
                self.position = self.branches[-1]
            elif d in (CLOSE_REGEX, CLOSE_BRANCH):
                self.branches.pop()
            else:
                self._move(d)
        self._solve_unknowns()
        self.minp = min(self.tiles.keys())
        self.maxp = max(self.tiles.keys())

    def get_most_doors(self):
        return max(self.distances.items(), key=itemgetter(1))[1]

    def get_more_than_tousand_doors(self):
        return sum(1 for i in self.distances.values() if i >= 1000)

    def get_most_doors_regex_try(self):

        elem = ''
        index = 0
        elements = {}
        choosing = {0: False}
        s = ''
        for i, d in enumerate(self.regex):
            # print(d, index, choosing[index], elements, s)
            if d in OPEN_REGEX:
                elements[index] = []
                choosing[index] = False
                s = ''
            elif d in CLOSE_REGEX:
                elements[index].append(s)
                elem = "".join(elements[index])
                break
            elif d in OPEN_BRANCH:
                elements[index].append(s)
                index += 1
                elements[index] = []
                choosing[index] = True
                s = ''
            elif d in BRANCH:
                elements[index].append(s)
                s = ''
            elif d in CLOSE_BRANCH:
                elements[index].append(s)
                longest = sorted(elements[index], reverse=True, key=len)[0]
                choosing[index] = None
                elements[index] = []
                index -= 1

                # print(s, longest, choosing[index])
                if s == '' and self.regex[i-1] == BRANCH:
                    # print("Loop??")
                    longest = s
                if choosing[index]:
                    elements[index][-1] = elements[index][-1] + longest
                else:
                    elements[index].append(longest)

                s = ''
            else:
                s += d
        # print(elem, len(elem))
        return len(elem)

    def _map_pos(self):
        for i, j in product((-1, 1), repeat=2):
            self.tiles[(self.position[0]+i, self.position[1]+j)] = WALL
        for i in (-1, 1):
            horiz = ((self.position[0] + i, self.position[1]))
            self.tiles[horiz] = self.tiles.get(horiz, UNKNOWN)
            vert = ((self.position[0] , self.position[1] + i))
            self.tiles[vert] = self.tiles.get(vert, UNKNOWN)

    def _move(self, direction):
        MOVE2POSINC = {
            NORTH: (0, -2),
            SOUTH: (0, 2),
            EAST: (2, 0),
            WEST: (-2, 0),
        }
        MOVE2DOORPOS = {
            NORTH: (0, 1),
            SOUTH: (0, -1),
            EAST: (-1, 0),
            WEST: (1, 0),
        }
        MOVE2DOOR = {
            NORTH: HORIZONTAL_DOOR,
            SOUTH: HORIZONTAL_DOOR,
            EAST: VERTICAL_DOOR,
            WEST: VERTICAL_DOOR,
        }
        current_distance = self.distances[self.position]

        self.position = tuple(a+b for a, b in zip(self.position, MOVE2POSINC[direction]))
        self.tiles[self.position] = ROOM
        distance = self.distances.get(self.position, None)
        if distance is None:
            self.distances[self.position] = current_distance + 1
        elif distance > current_distance:
            self.distances[self.position] = current_distance + 1

        self.tiles[tuple(a+b for a, b in zip(self.position, MOVE2DOORPOS[direction]))] = MOVE2DOOR[direction]
        self._map_pos()

    def _solve_unknowns(self):
        for k, v in self.tiles.items():
            if v == UNKNOWN:
                self.tiles[k] = WALL

    def __repr__(self):
        maze = []
        for y in range(self.minp[1], self.maxp[1]+1):
            maze.append("".join(self.tiles.get((x, y), EMPTY) for x in range(self.minp[0], self.maxp[0]+1)))
        return "\n".join(maze)


def get_data():
    with open('./input', 'rt') as f:
        values = [line.strip() for line in f.readlines()]
    return values[0]


def solve():
    data = get_data()

    # Part 1
    map = Maze(data)
    most_doors = map.get_most_doors()
    print(f"Part1 - The shortest path to the furthest room includes {most_doors} doors")

    # Part 2
    farthest_than_1000 = map.get_more_than_tousand_doors()
    print(f"Part2 - Rooms number that have at least a distance of 1000 is: {farthest_than_1000}")


if __name__ == "__main__":
    solve()
