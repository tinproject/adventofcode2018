from collections import Counter


def calc_checksum(box_ids):
    # Get a generator or the numbers of max letter repetition in the boxId
    letter_counters = [Counter(box_id) for box_id in box_ids]
    # Aggregate max letter repetition from all box_ids
    repetition_counter = [Counter(v.values()) for v in letter_counters]

    exactly_two_repetitions = sum((1 for c in repetition_counter if c[2] > 0))
    exactly_three_repetitions = sum((1 for c in repetition_counter if c[3] > 0))

    checksum = exactly_three_repetitions * exactly_two_repetitions
    return checksum


def get_box_id_num_of_differ_characters(one_box_id, other_box_id):
    return sum((1 for x, y in zip(one_box_id, other_box_id) if x != y))


def get_letters_in_common(box_ids):
    differences = []

    for i, first_box_id in enumerate(box_ids):
        for j, second_box_id in enumerate(box_ids[i+1:], i+1):
            num_different_letters = get_box_id_num_of_differ_characters(first_box_id, second_box_id)
            if num_different_letters == 1:
                differences.append((i, j))
    if not differences:
        raise ValueError("We can't find two box Ids with only one letter of difference.")

    # assume we only have two different box ids with one letter of difference
    first_box_id = box_ids[differences[0][0]]
    second_box_id = box_ids[differences[0][1]]
    common_letters = "".join(x for x, y in zip(first_box_id, second_box_id) if x == y)
    return common_letters


def get_values():
    with open('./input', 'rt') as f:
        values = f.readlines()
    return [value.strip() for value in values if value]


def solve():
    box_ids = get_values()

    # Part 1
    checksum = calc_checksum(box_ids)
    print(f"Part1 - The checksum is: {checksum}")

    # Part 2
    common_letters = get_letters_in_common(box_ids)
    print(f"Part2 - The letters in common are: {common_letters}")


if __name__ == "__main__":
    solve()
