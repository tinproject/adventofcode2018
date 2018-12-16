from unittest.mock import Mock

from day import Mob, BattleField, run_elves_simulation


def test_mob_order():
    battlefield = Mock()
    m = Mob(battlefield, 2, 2, 'E')
    m1 = Mob(battlefield, 1, 1, 'E')
    m2 = Mob(battlefield, 4, 1, 'E')
    m3 = Mob(battlefield, 1, 2, 'E')
    m4 = Mob(battlefield, 3, 2, 'E')
    m5 = Mob(battlefield, 1, 4, 'E')
    m6 = Mob(battlefield, 4, 4, 'E')

    assert m1 < m
    assert m2 < m
    assert m3 < m
    assert m4 > m
    assert m5 > m
    assert m6 > m


def parse_battle_field_input(example_input):
    return [line.strip() for line in example_input.splitlines() if line.strip()]


def test_battle_outcome_0():
    battle_input = """
    #########
    #G..G..G#
    #.......#
    #.......#
    #G..E..G#
    #.......#
    #.......#
    #G..G..G#
    #########
    """
    battle_outcome = 27828
    battlefield = BattleField(parse_battle_field_input(battle_input))
    battlefield.run_battle()

    result = battlefield.get_battle_outcome()

    assert result == battle_outcome


def test_battle_outcome_1():
    battle_input = """
    #######
    #.G...#
    #...EG#
    #.#.#G#
    #..G#E#
    #.....#
    #######
    """
    battle_outcome = 27730
    battlefield = BattleField(parse_battle_field_input(battle_input))
    battlefield.run_battle()

    result = battlefield.get_battle_outcome()

    assert result == battle_outcome


def test_battle_outcome_2():
    battle_input = """
    #######
    #G..#E#
    #E#E.E#
    #G.##.#
    #...#E#
    #...E.#
    #######
    """
    battle_outcome = 36334
    battlefield = BattleField(parse_battle_field_input(battle_input))
    battlefield.run_battle()

    result = battlefield.get_battle_outcome()

    assert result == battle_outcome


def test_battle_outcome_3():
    battle_input = """
    #######
    #E..EG#
    #.#G.E#
    #E.##E#
    #G..#.#
    #..E#.#
    #######
    """
    battle_outcome = 39514
    battlefield = BattleField(parse_battle_field_input(battle_input))
    battlefield.run_battle()

    result = battlefield.get_battle_outcome()

    assert result == battle_outcome


def test_battle_outcome_4():
    battle_input = """
    #######
    #E.G#.#
    #.#G..#
    #G.#.G#
    #G..#.#
    #...E.#
    #######
    """
    battle_outcome = 27755
    battlefield = BattleField(parse_battle_field_input(battle_input))
    battlefield.run_battle()

    result = battlefield.get_battle_outcome()

    assert result == battle_outcome


def test_battle_outcome_5():
    battle_input = """
    #######
    #.E...#
    #.#..G#
    #.###.#
    #E#G#G#
    #...#G#
    #######
    """
    battle_outcome = 28944
    battlefield = BattleField(parse_battle_field_input(battle_input))
    battlefield.run_battle()

    result = battlefield.get_battle_outcome()

    assert result == battle_outcome


def test_battle_outcome_6():
    battle_input = """
    #########
    #G......#
    #.E.#...#
    #..##..G#
    #...##..#
    #...#...#
    #.G...G.#
    #.....G.#
    #########
    """
    battle_outcome = 18740
    battlefield = BattleField(parse_battle_field_input(battle_input))
    battlefield.run_battle()

    result = battlefield.get_battle_outcome()

    assert result == battle_outcome


def test_battle_outcome_7():
    battle_input = """
    #########
    #G......#
    #.E.#...#
    #..##..G#
    #...##..#
    #...#...#
    #.G...G.#
    #.....G.#
    #########
    """
    battle_outcome = 18740
    battlefield = BattleField(parse_battle_field_input(battle_input))
    battlefield.run_battle()

    result = battlefield.get_battle_outcome()

    assert result == battle_outcome


def test_elves_win_outcome_0():
    battle_input = """
    #######
    #.G...#
    #...EG#
    #.#.#G#
    #..G#E#
    #.....#
    #######
    """
    battle_outcome = 4988
    elves_attack_points = 15

    result = run_elves_simulation(parse_battle_field_input(battle_input))

    assert result == (battle_outcome, elves_attack_points)


def test_elves_win_outcome_1():
    battle_input = """
    #######
    #E..EG#
    #.#G.E#
    #E.##E#
    #G..#.#
    #..E#.#
    #######
    """
    battle_outcome = 31284
    elves_attack_points = 4

    result = run_elves_simulation(parse_battle_field_input(battle_input))

    assert result == (battle_outcome, elves_attack_points)


def test_elves_win_outcome_2():
    battle_input = """
    #######
    #E.G#.#
    #.#G..#
    #G.#.G#
    #G..#.#
    #...E.#
    #######
    """
    battle_outcome = 3478
    elves_attack_points = 15

    result = run_elves_simulation(parse_battle_field_input(battle_input))

    assert result == (battle_outcome, elves_attack_points)


def test_elves_win_outcome_3():
    battle_input = """
    #######
    #.E...#
    #.#..G#
    #.###.#
    #E#G#G#
    #...#G#
    #######
    """
    battle_outcome = 6474
    elves_attack_points = 12

    result = run_elves_simulation(parse_battle_field_input(battle_input))

    assert result == (battle_outcome, elves_attack_points)


def test_elves_win_outcome_4():
    battle_input = """
    #########
    #G......#
    #.E.#...#
    #..##..G#
    #...##..#
    #...#...#
    #.G...G.#
    #.....G.#
    #########
    """
    battle_outcome = 1140
    elves_attack_points = 34

    result = run_elves_simulation(parse_battle_field_input(battle_input))

    assert result == (battle_outcome, elves_attack_points)
