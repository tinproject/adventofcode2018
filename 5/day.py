from collections import Counter


def react(unit1, unit2):
    if unit1.lower() != unit2.lower():
        # Not the same letter
        return False
    if unit1 != unit2:
        # same letter, different capitalization
        return True
    # same letter, same capitalization
    return False


def compact_units(polymer):
    if len(polymer) < 2:
        return polymer

    new_polymer = ""
    pointer = 0
    while pointer < len(polymer):
        if len(new_polymer) == 0:
            new_polymer += polymer[pointer]
        else:
            if react(new_polymer[-1], polymer[pointer]):
                new_polymer = new_polymer[:-1]
            else:
                new_polymer += polymer[pointer]
        # print(new_polymer, pointer)
        pointer += 1

    return new_polymer


def get_polymer_units(polymer):
    stable_polymer = compact_units(polymer)
    return len(stable_polymer)


def get_data():
    with open('./input', 'rt') as f:
        values = f.readline().strip()
    return values


def solve():
    data = get_data()

    # Part 1
    part1 = get_polymer_units(data)
    print(f"Part1 - The solution is: {part1}")

    # Part 2
    part2 = None
    print(f"Part2 - The solution is: {part2}")


if __name__ == "__main__":
    solve()
