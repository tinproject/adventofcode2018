from functools import lru_cache
from itertools import product
from operator import itemgetter


GRID_SIZE = 300


def get_data():
    with open('./input', 'rt') as f:
        values = [int(line.strip()) for line in f.readlines()]
    return values[0]


@lru_cache(maxsize=2 ** 22)
def get_total_power(serial_number, x, y, area_side=3):
    if area_side == 1:
        rack_id = x + 10
        total_power = ((((rack_id * y + serial_number) * rack_id) // 100) % 10) - 5
    elif 1 < area_side <= GRID_SIZE and area_side % 2 != 0:
        total_power = get_total_power(serial_number, x, y, area_side-1)
        for i in range(x, x+area_side):
            total_power += get_total_power(serial_number, i, y+area_side-1, 1)
        for j in range(y, y+area_side-1):
            total_power += get_total_power(serial_number, x+area_side-1, j, 1)
        return total_power
    elif 1 < area_side <= GRID_SIZE and area_side % 2 == 0:
        middle_side = area_side // 2
        total_power = get_total_power(serial_number, x, y, middle_side)
        total_power += get_total_power(serial_number, x+middle_side, y, middle_side)
        total_power += get_total_power(serial_number, x, y+middle_side, middle_side)
        total_power += get_total_power(serial_number, x+middle_side, y+middle_side, middle_side)
    else:
        raise ValueError
    return total_power


def get_max_power_area_for_size(serial_number, area_side=3):
    power_areas = []
    for y, x in product(range(1, GRID_SIZE-area_side+2), range(1, GRID_SIZE-area_side+2)):
        power_areas.append((x, y, area_side, get_total_power(serial_number, x, y, area_side)))

    return max(power_areas, key=itemgetter(3))


def get_max_power_area(serial_number):
    max_power_areas = []

    for area_side in range(1, GRID_SIZE+1):
        max_power_areas.append(get_max_power_area_for_size(serial_number, area_side))

    return max(max_power_areas, key=itemgetter(3))


def solve():
    data = get_data()

    # Part 1
    max_power_area = get_max_power_area_for_size(data)
    print(f"Part1 - The largest total power is {max_power_area[3]} for "
          f"top-left corner: {max_power_area[0]},{max_power_area[1]}")

    # Part 2
    max_power_area = get_max_power_area(data)
    print(f"Part1 - The largest total power is {max_power_area[3]} for "
          f"top-left corner/size: {max_power_area[0]},{max_power_area[1]},{max_power_area[2]}")


if __name__ == "__main__":
    solve()
