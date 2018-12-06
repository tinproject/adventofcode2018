import pytest


from day import compact_units, get_polymer_units, react


@pytest.mark.parametrize("input1,input2,output", [
    ("a", "A", True),
    ("A", "a", True),
    ("a", "b", False),
    ("a", "a", False),
    ("A", "A", False),
])
def test_react(input1, input2, output):

    result = react(input1, input2)

    assert result == output


@pytest.mark.parametrize("input,output", [
    ("aA", ""),
    ("abBA", ""),
    ("abAB", "abAB"),
    ("aabAAB", "aabAAB"),
    ("aAa", "a"),
    ("baAa", "ba"),
    ("aAab", "ab"),
    ("dabAcCaCBAcCcaDA", "dabCBAcaDA"),
])
def test_compact_units(input, output):
    result = compact_units(input)

    assert result == output


def test_get_polymer_units():
    polymer = "dabAcCaCBAcCcaDA"
    expected_units = 10

    resutl = get_polymer_units(polymer)

    assert resutl == expected_units

