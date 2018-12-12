import re


def get_data():
    with open('./input', 'rt') as f:
        values = [line.strip() for line in f.readlines()]
    return values


RE_INITIAL_STATE = re.compile(r"^initial state: (?P<initial_state>[.#]+)$")
RE_SPREAD_PATTERN = re.compile(r"^(?P<spread_pattern>[.#]{5})\s=>\s(?P<next_state>[.#])$")


def parse_input(data):
    initial_state = None
    spread_patterns = dict()

    for l in data:
        ini = RE_INITIAL_STATE.match(l)
        if ini:
            initial_state = ini.group('initial_state')
        pat = RE_SPREAD_PATTERN.match(l)
        if pat:
            spread_patterns[pat.group('spread_pattern')] = pat.group('next_state')

    if not initial_state and len(initial_state) > 0:
        raise ValueError(f"Non proper initial state: {initial_state}")
    if len(spread_patterns) != 32:
        raise ValueError(f"We lack of spread patterns: {spread_patterns}")

    return initial_state, spread_patterns


def get_next_state(initial_state, spread_patterns):
    pattern_size = 5
    side = 5
    border = '.' * side
    working = border + initial_state + border
    next_state = "".join(
        spread_patterns[working[3+i:3+i+pattern_size]] for i in range(len(working)-pattern_size-side)
    )
    return next_state


def get_pot_number_sums_after_n_gens(initial_state, spread_patterns, gens=20):
    end_state = gens
    border_size = gens
    border = '.' * border_size
    state = border + initial_state + border

    states = [state]  # initial state
    for t in range(1, end_state+1):
        state = get_next_state(state, spread_patterns)
        states.append(state)

    pot_number_sums = []
    for state in states:
        pot_number_sums.append(sum(
            pot for i, pot in enumerate(range(-border_size, len(state)-border_size))
            if state[i] == '#'
        ))

    for i, s in enumerate(states):
        print(f"{i:2}", f"{pot_number_sums[i]:8}", s)

    return pot_number_sums


def solve_second_part(initial_state, spread_patterns, generations=100):
    end_state = 110
    border_size = end_state
    border = '.' * border_size
    state = border + initial_state + border

    states = [state]  # initial state
    for t in range(1, end_state+1):
        state = get_next_state(state, spread_patterns)
        states.append(state)

    pot_number_sums = []
    pot_numbers = []
    for state in states:
        pot_numbers.append([
            pot for i, pot in enumerate(range(-border_size, len(state)-border_size))
            if state[i] == '#'
        ])
        pot_number_sums.append(sum(pot_numbers[-1]))

    # From generation 100 the plants do not grow or shrink in number, just move right on pot number increase
    # from pot number 0, so at

    pot_numbers_at_100 = pot_numbers[100]
    min_pot_number_per_gen_100 = min(pot_numbers_at_100)
    num_of_pots_at_gen_100 = len(pot_numbers_at_100)
    pot_number_sum_at_gen_100 = pot_number_sums[100]

    pot_number_sum_at_gen_n = pot_number_sum_at_gen_100 + \
        (generations - 100 - min_pot_number_per_gen_100) * num_of_pots_at_gen_100
    return pot_number_sum_at_gen_n


def solve():
    data = get_data()

    initial_state, spread_patterns = parse_input(data)
    pot_number_sums = get_pot_number_sums_after_n_gens(initial_state, spread_patterns, 101)

    # Part 1
    print(f"Part1 - The sum of pot numbers after iteration 10 is: {pot_number_sums[2]}")

    # Part 2
    input_part_2 = 50000000000
    solution = solve_second_part(initial_state, spread_patterns, input_part_2)
    print(f"Part2 - The sum of pot numbers after iteration {input_part_2} is: {solution}")


if __name__ == "__main__":
    solve()
