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


class PlaygroundLocation:
    __slots__ = ['marble', 'cw', 'ccw']

    def __init__(self, marble, cw=None, ccw=None):
        self.marble = marble
        self.cw = cw
        self.ccw = ccw

    def __repr__(self):
        return f"Marble {self.marble}, cw={self.cw.marble}, ccw={self.ccw.marble}"


class ElfMarbleGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.player_scores = [0 for _ in range(num_players + 1)]
        self.current_marble = PlaygroundLocation(0)
        self.current_marble.cw = self.current_marble
        self.current_marble.ccw = self.current_marble

    def put_marble(self, marble, player):
        if marble % 23 == 0:
            self.player_scores[player] += marble
            rm = self.pop_marble()
            self.player_scores[player] += rm
        else:
            left = self.current_marble.cw
            right = left.cw
            m = PlaygroundLocation(marble, cw=right, ccw=left)
            left.cw = m
            right.ccw = m
            self.current_marble = m

    def pop_marble(self):
        for _ in range(6):
            self.current_marble = self.current_marble.ccw

        rm = self.current_marble.ccw
        right = rm.ccw
        right.cw = self.current_marble
        self.current_marble.ccw = right
        return rm.marble

    def play(self, last_marble_points):
        players = cycle(range(1, self.num_players + 1))

        for marble in range(1, last_marble_points + 1):
            player = next(players)
            self.put_marble(marble, player)

    def get_highest_score(self):
        return max(self.player_scores)


def get_highest_score(num_players, last_marble_points):
    game = ElfMarbleGame(num_players)

    game.play(last_marble_points)

    return game.get_highest_score()


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
