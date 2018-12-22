from collections import Counter

OPEN_GROUND = '.'
TREES = '|'
LUMBERYARD = '#'


def lumber_area_transition(area):
    c = Counter(area)
    current_acre_index = 4
    current_acre = area[current_acre_index]

    transitions = {
        OPEN_GROUND: lambda x: TREES if c[TREES] >= 3 else x[current_acre_index],
        TREES: lambda x: LUMBERYARD if c[LUMBERYARD] >= 3 else x[current_acre_index],
        LUMBERYARD: lambda x: LUMBERYARD if c[TREES] >= 1 and c[LUMBERYARD] >= 2 else OPEN_GROUND,
    }
    return transitions[current_acre](area)


class LumberArea:
    def __init__(self, lumber_area_input):
        self.init_area = []
        for line in lumber_area_input:
            self.init_area.append(line)
        self.max_x = len(self.init_area[0])
        self.max_y = len(self.init_area)
        self.minute = 0
        self.area = {0: self.init_area}
        # print(self)
        # print(self.max_x, self.max_y)

    def _get_surroundings(self, x, y):
        def get_acre(x, y):
            if 0 <= x < self.max_x and 0 <= y < self.max_y:
                acre = self.area[self.minute][y][x]
            else:
                acre = OPEN_GROUND
            return acre

        surroundings = "".join(get_acre(i, j) for j in range(y-1, y+2) for i in range(x-1, x+2))
        return surroundings

    def _get_acre_transform(self, x, y):
        new_acre_state = lumber_area_transition(self._get_surroundings(x, y))
        return new_acre_state

    def pass_time(self):
        current_area = self.area[self.minute]
        new_area = []
        for y, line in enumerate(current_area):
            new_line = []
            for x, _ in enumerate(line):
                new_line.append(self._get_acre_transform(x, y))
            new_area.append("".join(new_line))
        self.minute += 1
        self.area[self.minute] = new_area

    def grow(self, minutes):
        for _ in range(minutes):
            self.pass_time()

    def get_wooden_acres_value(self):
        wooden_acres = sum(1 for y in self.area[self.minute] for x in y if x == TREES)
        return wooden_acres

    def get_lumberyards_value(self):
        lumberyards = sum(1 for y in self.area[self.minute] for x in y if x == LUMBERYARD)
        return lumberyards

    def get_resource_value(self):
        return self.get_wooden_acres_value() * self.get_lumberyards_value()

    def __repr__(self):
        text_lines = [f"Minute: {self.minute:03} Resurce value: {self.get_resource_value()}"] + \
                     [line for line in self.area[self.minute]] + [""]
        return "\n".join(text_lines)


def get_data():
    with open('./input', 'rt') as f:
        values = [line.strip() for line in f.readlines()]
    return values


def solve():
    data = get_data()

    # Part 1
    lumber_area = LumberArea(data)
    print(lumber_area)
    lumber_area.grow(10)
    print(lumber_area)
    resource_value_afte_10_minutes = lumber_area.get_resource_value()
    print(f"Part1 - The resource value after 10 minutes is: {resource_value_afte_10_minutes}")

    # Part 2
    print(f"Part2 - ... is: {None}")


if __name__ == "__main__":
    solve()
