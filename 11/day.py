from functools import lru_cache
from itertools import product
from operator import itemgetter


@lru_cache(maxsize=None)
def get_power_level(serial_number, x, y):
    rack_id = x + 10
    power_level = ((((rack_id * y + serial_number) * rack_id) // 100) % 10) - 5
    return power_level


def get_data():
    with open('./input', 'rt') as f:
        values = [int(line.strip()) for line in f.readlines()]
    return values[0]


def get_total_power(serial_number, x, y):
    total_power = sum(get_power_level(serial_number, i, j) for i in range(x, x+3) for j in range(y, y+3))
    return total_power


def get_max_power_area(serial_number):
    grid_side = 300

    power_areas = []
    for y, x in product(range(1, grid_side-2), range(1, grid_side-2)):
        power_areas.append((x, y, get_total_power(serial_number, x, y)))

    return max(power_areas, key=itemgetter(2))


def solve():
    data = get_data()

    # Part 1
    max_power_area = get_max_power_area(data)
    print(f"Part1 - The largest total power is {max_power_area[2]} for "
          f"top-left corner: {max_power_area[0]},{max_power_area[1]}")

    # Part 2
    print(f"Part2 - ... is: {None}")


if __name__ == "__main__":
    solve()
