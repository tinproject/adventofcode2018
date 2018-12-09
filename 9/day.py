from itertools import cycle


def get_data():
    with open('./input', 'rt') as f:
        values = [line.strip() for line in f.readlines()]
    return values


def parse_data(data):
    tokens = data.split(" ")
    num_players = int(tokens[0].strip())
    last_marble_points = int(tokens[6].strip())
    return num_players, last_marble_points


def calc_circular_index(playground, current_marble_index, delta):
    playground_size = len(playground)
    if playground_size == 1:
        return 1
    new_index = current_marble_index + delta
    return new_index % len(playground)


def get_highest_score(num_players, last_marble_points):
    playground = [0]
    current_marble_index = 0

    players = cycle(range(1, num_players + 1))
    player_scores = [0 for _ in range(num_players + 1)]

    for marble in range(1, last_marble_points + 1):
        player = next(players)

        if marble % 23 == 0:
            next_marble_index = calc_circular_index(playground, current_marble_index, -7)
            marble_removed = playground.pop(next_marble_index)
            player_scores[player] += marble
            player_scores[player] += marble_removed
        else:
            next_marble_index = calc_circular_index(playground, current_marble_index, +2)
            playground.insert(next_marble_index, marble)

        current_marble_index = next_marble_index

    return max(player_scores)


def solve():
    data = get_data()

    # Part 1
    num_players, last_marble_points = parse_data(data[0])
    highest_score = get_highest_score(num_players, last_marble_points)
    print(f"Part1 - The hights score in the game is: {highest_score}")

    # Part 2
    highest_score = get_highest_score(num_players, last_marble_points * 100)
    print(f"Part2 - The hights score in the game with 100 times marbles is: {highest_score}")


if __name__ == "__main__":
    solve()
