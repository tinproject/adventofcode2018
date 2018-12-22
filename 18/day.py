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
        self.resource_value_at_minute = {}
        self.resource_value_at_minute[self.minute] = self.get_resource_value()
        self._has_cycle = False

    def _get_acre(self, x, y):
        if 0 <= x < self.max_x and 0 <= y < self.max_y:
            acre = self.area[self.minute][y][x]
        else:
            acre = OPEN_GROUND
        return acre

    def _get_surroundings(self, x, y):
        surroundings = "".join(self._get_acre(i, j) for j in range(y-1, y+2) for i in range(x-1, x+2))
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
        resource_value = self.get_resource_value()
        self.resource_value_at_minute[self.minute] = resource_value
        # print(f"Pass time, minute: {self.minute:03}, resource_value: {resource_value}")

    def grow(self, minutes):
        for _ in range(minutes):
            self.pass_time()

    def get_resource_value_after_minute(self, minute):
        cycle_threshold = 20
        current_num_values = len(set(self.resource_value_at_minute.values()))
        cycle_counter = 0

        while not self._has_cycle:
            if minute <= self.minute:
                # Prevent go further that the asked minute
                break

            self.pass_time()
            # Detect that we have atr least a cycle of cycle_threshold consecutive values
            num_values = len(set(self.resource_value_at_minute.values()))
            if num_values != current_num_values:
                current_num_values = num_values
                cycle_counter = 0
                continue
            else:
                cycle_counter += 1
                if cycle_counter <= cycle_threshold:
                    continue

            if len(set(self.resource_value_at_minute.values())) == num_values:
                value = self.resource_value_at_minute[self.minute]
                end_cycle_minute = self.minute
                start_cycle_minute = list(filter(lambda x: x[1] == value, self.resource_value_at_minute.items()))[0][0]
                self._has_cycle = True
                self._start_cycle_minute = start_cycle_minute
                self._cycle_minutes = end_cycle_minute - start_cycle_minute

        if minute in self.resource_value_at_minute:
            return self.resource_value_at_minute[minute]

        # Check for bigger values
        minutes = minute - self._start_cycle_minute
        num_cycles, remanent = divmod(minutes, self._cycle_minutes)
        return self.resource_value_at_minute[self._start_cycle_minute + remanent]

    def get_wooden_acres_value(self):
        wooden_acres = sum(1 for y in self.area[self.minute] for x in y if x == TREES)
        return wooden_acres

    def get_lumberyards_value(self):
        lumberyards = sum(1 for y in self.area[self.minute] for x in y if x == LUMBERYARD)
        return lumberyards

    def get_resource_value(self):
        resource_value = self.get_wooden_acres_value() * self.get_lumberyards_value()
        self.resource_value_at_minute[self.minute] = resource_value
        return resource_value

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
    print("Initial state:", lumber_area)
    lumber_area.grow(10)
    print(lumber_area)
    resource_value_after_10_minutes = lumber_area.get_resource_value()
    print(f"Part1 - The resource value after 10 minutes is: {resource_value_after_10_minutes}")

    # Part 2
    minutes = 1000000000
    resource_value_after_n_minutes = lumber_area.get_resource_value_after_minute(minutes)
    print(f"Part2 - The resource value after {minutes} minutes is: {resource_value_after_n_minutes}")


if __name__ == "__main__":
    solve()
