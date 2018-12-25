

from day import Maze


def test_maze_1():
    regex = "^ENWWW(NEEE|SSE(EE|N))$"
    expected_maze = """#########
#.|.|.|.#
#-#######
#.|.|.|.#
#-#####-#
#.#.#X|.#
#-#-#####
#.|.|.|.#
#########"""

    result = Maze(regex)

    assert repr(result) == expected_maze


def test_maze_doors_1():
    regex = "^ENWWW(NEEE|SSE(EE|N))$"
    expected_doors = 10

    result = Maze(regex).get_most_doors()

    assert result == expected_doors


def test_maze_2():
    regex = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
    expected_maze = """###########
#.|.#.|.#.#
#-###-#-#-#
#.|.|.#.#.#
#-#####-#-#
#.#.#X|.#.#
#-#-#####-#
#.#.|.|.|.#
#-###-###-#
#.|.|.#.|.#
###########"""

    result = Maze(regex)

    assert repr(result) == expected_maze


def test_maze_doors_2():
    regex = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
    expected_doors = 18

    result = Maze(regex).get_most_doors()

    assert result == expected_doors


def test_maze_3():
    regex = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
    expected_maze = """#############
#.|.|.|.|.|.#
#-#####-###-#
#.#.|.#.#.#.#
#-#-###-#-#-#
#.#.#.|.#.|.#
#-#-#-#####-#
#.#.#.#X|.#.#
#-#-#-###-#-#
#.|.#.|.#.#.#
###-#-###-#-#
#.|.#.|.|.#.#
#############"""

    result = Maze(regex)

    assert repr(result) == expected_maze


def test_maze_doors_3():
    regex = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
    expected_doors = 23

    result = Maze(regex).get_most_doors()

    assert result == expected_doors


def test_maze_4():
    regex = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"
    expected_maze = """###############
#.|.|.|.#.|.|.#
#-###-###-#-#-#
#.|.#.|.|.#.#.#
#-#########-#-#
#.#.|.|.|.|.#.#
#-#-#########-#
#.#.#.|X#.|.#.#
###-#-###-#-#-#
#.|.#.#.|.#.|.#
#-###-#####-###
#.|.#.|.|.#.#.#
#-#-#####-#-#-#
#.#.|.|.|.#.|.#
###############"""

    result = Maze(regex)

    assert repr(result) == expected_maze


def test_maze_doors_4():
    regex = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"
    expected_doors = 31

    result = Maze(regex).get_most_doors()

    assert result == expected_doors
