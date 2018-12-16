from dataclasses import dataclass
from operator import itemgetter


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


WALL = '#'
EMPTY_SPACE = '.'
ELF = 'E'
GOBLIN = 'G'

ALL_MOBS = (ELF, GOBLIN)


class Mob:
    def __init__(self, battlefield, x, y, mob_type=None, hit_points=200, attack_points=3):
        self.x = x
        self.y = y
        self.attack_points = attack_points
        self.hit_points = hit_points
        if mob_type == ELF:
            self.mob_type = mob_type
            self.enemy = GOBLIN
        elif mob_type == GOBLIN:
            self.mob_type = mob_type
            self.enemy = ELF
        else:
            raise ValueError(f"Unrecognized mob type: '{mob_type}'")
        self.battlefield: BattleField = battlefield
        self.battlefield.set_square(self.x, self.y, mob_type)

    @property
    def coord(self):
        return self.x, self.y

    def play_turn(self):
        # print(f"==> Unit {self} taking it's turn.")
        if self.hit_points <= 0:
            # raise Exception
            return f"{self} | We already died. Skip!"
        # Check if there are any enemies left
        enemies = self.battlefield.get_enemies(self.enemy)
        if len(enemies) <= 0:
            return f"{self} | No more enemies left"

        action = f"{self}"

        # Look if we do not have enemies adjacent to move
        if not any(e in self.enemy for e in self._get_adjacent_squares()):
            # Can we move?
            if self.battlefield.get_empty_squares_coords_around_point(self.coord):
                action += self._move_towards_enemies(enemies)
            else:
                action += f" | Stuck!"

        # Look for enemies in range adjacent to attack
        adjacent_coords = self._get_adjacent_coords()
        enemies_for_attack = []
        for enemy in self.battlefield.get_enemies(self.enemy):
            if enemy.coord in adjacent_coords:
                enemies_for_attack.append(enemy)
        if enemies_for_attack:
            min_hit_points = min(enemies_for_attack, key=lambda e: e.hit_points).hit_points
            enemy_to_attack = sorted(e for e in enemies_for_attack if e.hit_points == min_hit_points)[0]

            action += self.attack(enemy_to_attack)

        return action + f" | End turn"

    def _move_towards_enemies(self, enemies):
        # Find next move
        origin = self.coord
        # get target coords
        targets = set()
        for enemy in enemies:
            targets.update(self.battlefield.get_empty_squares_coords_around_point(enemy.coord))

        empty_mob_adjacent_squares = self.battlefield.get_empty_squares_coords_around_point(origin)

        # Find reachable targets
        nearest_targets = set()
        visited_squares = set(origin)
        distance = 0
        next_to_visit_squares = set(empty_mob_adjacent_squares)
        while (not nearest_targets) and next_to_visit_squares:
            distance += 1
            # print(f"Looking at distance {distance}")
            to_visit_squares = next_to_visit_squares
            next_to_visit_squares = set()
            while to_visit_squares:
                visit = to_visit_squares.pop()
                # print(f"Visiting {visit}")
                visited_squares.add(visit)
                if visit in targets:
                    nearest_targets.add(visit)  # We reach a target
                for coord in self.battlefield.get_empty_squares_coords_around_point(visit):
                    if coord not in visited_squares:
                        next_to_visit_squares.add(coord)

        # print(nearest_targets)
        if not nearest_targets:
            return f" | We can't reach any target. Stay in place!"

        # We can reach a target
        # print(f"At a distance of {distance} there are reachable targets {nearest_targets}")
        # Choose target following top-down left-right order
        chosen_target = sorted(nearest_targets, key=itemgetter(1, 0))[0]
        # print(f"We choose target at {chosen_target}")

        # If chosen target is not adjacent, find paths
        if chosen_target not in empty_mob_adjacent_squares:
            # If there are multiple paths with same distance, choose the order
            origin = chosen_target
            targets = self.battlefield.get_empty_squares_coords_around_point(self.coord)
            nearest_targets = set()
            visited_squares = set(origin)
            distance = 0
            next_to_visit_squares = set(self.battlefield.get_empty_squares_coords_around_point(origin))

            while (not nearest_targets) and next_to_visit_squares:
                distance += 1
                # print(f"Looking at distance {distance}")
                to_visit_squares = next_to_visit_squares
                next_to_visit_squares = set()
                while to_visit_squares:
                    visit = to_visit_squares.pop()
                    # print(f"Visiting {visit}")
                    visited_squares.add(visit)
                    if visit in targets:
                        nearest_targets.add(visit)  # We reach a target
                    for coord in self.battlefield.get_empty_squares_coords_around_point(visit):
                        if coord not in visited_squares:
                            next_to_visit_squares.add(coord)
            chosen_target = sorted(nearest_targets, key=itemgetter(1, 0))[0]

        self.move(chosen_target)
        return f" | Moved to {chosen_target}"

    def _get_adjacent_squares(self):
        adjacent_coords = (
            self.battlefield.get_square(self.x, self.y-1),  # up
            self.battlefield.get_square(self.x-1, self.y),  # left
            self.battlefield.get_square(self.x+1, self.y),  # right
            self.battlefield.get_square(self.x, self.y+1),  # down
        )
        return adjacent_coords

    def _get_adjacent_coords(self):
        adjacent_coords = (
            (self.x, self.y-1),  # up
            (self.x-1, self.y),  # left
            (self.x+1, self.y),  # right
            (self.x, self.y+1),  # down
        )
        return adjacent_coords

    def move(self, to_position):
        self.battlefield.set_square(*self.coord, EMPTY_SPACE)
        if self.battlefield.get_square(*to_position) != EMPTY_SPACE:
            raise ValueError(f"{self} | ERROR: Trying to move to a non empty square.")
        if 1 < abs(to_position[0] - self.x) > 0 or 1 < abs(to_position[1] - self.y) > 0:
            raise Exception
        self.x = to_position[0]
        self.y = to_position[1]
        self.battlefield.set_square(*to_position, self.mob_type)

    def attack(self, other):
        die = other.receive_attack(self.attack_points)
        return f" | Killed: {other}" if die else f" | Attacked: {other}"

    def receive_attack(self, attack_points):
        self.hit_points -= attack_points
        if self.hit_points <= 0:
            # print(f"{self} | Die!")
            self.battlefield.set_square(*self.coord, EMPTY_SPACE)
            self.battlefield.mobs.remove(self)
            return True
        return False

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __eq__(self, other):
        return self.coord == other.coord

    def __repr__(self):
        return f"<{self.mob_type} {self.x},{self.y} HP:{self.hit_points} AP:{self.attack_points}>"


class BattleField:
    def __init__(self, initial_state):
        self.round = 0
        self.mobs = []
        self.playground = []
        for y, line in enumerate(initial_state):
            self.playground.append([])
            for pos in line:
                if pos in ALL_MOBS:
                    pos = EMPTY_SPACE
                self.playground[y].append(pos)

        for y, line in enumerate(initial_state):
            for x, pos in enumerate(line):
                if pos in ALL_MOBS:
                    self.mobs.append(Mob(self, x, y, pos))

    def get_battle_outcome(self, max_rounds=100):
        for _ in range(max_rounds):  # Limit rounds
            if self.play_round():
                full_rounds = self.round - 1
                total_points = sum(m.hit_points for m in self.mobs)
                battle_outcome = full_rounds * total_points
                print(self)
                print(f"====> Combat ends at round {self.round}!")
                print(f"====> Full rounds completed: {full_rounds} "
                      f"Total points: {total_points} Outcome: {battle_outcome}")
                return battle_outcome

    def play_round(self):
        self.round += 1
        # print(f"====> Playing Round: {self.round}")
        for mob in sorted(self.mobs):
            turn_result = mob.play_turn()
            # print(turn_result)
            if "No more enemies left" in turn_result:
                return True  # Combat ends
        # print(self)
        return False

    def set_square(self, x, y, square):
        self.playground[y][x] = square

    def get_square(self, x, y):
        return self.playground[y][x]

    def get_mob_at(self, x, y):
        mobs = [m for m in self.mobs if m.x == x and m.y == y]
        if len(mobs) >= 2:
            raise ValueError(f"ERROR: Two mobs at the same square {x},{y}")
        if mobs:
            return mobs[0]

    def get_empty_squares_coords_around_point(self, coord):
        x = coord[0]
        y = coord[1]
        adjacent_coords = (
            (x, y-1),  # up
            (x-1, y),  # left
            (x+1, y),  # right
            (x, y+1),  # down
        )
        return [coord for coord in adjacent_coords if self.get_square(*coord) == EMPTY_SPACE]

    def get_enemies(self, enemies):
        enemies = [m for m in self.mobs if m.mob_type in enemies]
        return enemies

    def __repr__(self):
        playground = "\n".join("".join(line) for line in self.playground)
        mobs = "\n".join(repr(m) for m in sorted(self.mobs))
        return f"===> Playground after {self.round} rounds: \n{playground}\n" \
            f"===> Mobs after {self.round} rounds: \n{mobs}"


def get_data():
    with open('./input', 'rt') as f:
        values = [line.strip() for line in f.readlines()]
    return values


def parse_input(values):
    return BattleField(values)


def solve():
    data = get_data()

    # Part 1
    battlefield = parse_input(data)
    battle_result = battlefield.get_battle_outcome()
    print(f"Part1 - The battle outcome is: {battle_result}")

    # Part 2
    # print(f"Part2 - ... is: {None}")


if __name__ == "__main__":
    solve()
