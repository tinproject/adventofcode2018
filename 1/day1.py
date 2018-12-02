from itertools import cycle


def get_values():
    with open('./input', 'rt') as f:
        values = f.readlines()
    return [int(value) for value in values if value]


def calibration(calibration_values, initial_frequency=0):
    return sum(calibration_values, initial_frequency)


def find_duplicate_frequency(calibration_values, initial_frequency=0):
    frequencies_found = {initial_frequency}
    frequency = initial_frequency
    for value in cycle(calibration_values):
        frequency += value
        if frequency not in frequencies_found:
            frequencies_found.add(frequency)
        else:
            break
    return frequency


def calibrate():
    calibration_values = get_values()

    # Parti 1
    frequency = calibration(calibration_values)
    print(f"Part1 - Calibrate with frequency: {frequency}")

    # Part 2
    dup_frequency = find_duplicate_frequency(calibration_values)
    print(f"Part2 - The first duplicated frequency is: {dup_frequency}")


if __name__ == "__main__":
    calibrate()
