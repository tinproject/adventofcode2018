import pytest

from day2 import calc_checksum, get_box_id_num_of_differ_characters, get_letters_in_common


def test_calc_checksum():
    box_ids = ["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"]
    checksum = 12

    result = calc_checksum(box_ids)

    assert result == checksum


@pytest.mark.parametrize("one_box_id,other_box_id,diffenences", [
    ("abcde", "axcye", 2),
    ("fghij", "fguij", 1),
])
def test_get_box_id_num_of_differ_characters(one_box_id, other_box_id, diffenences):
    result = get_box_id_num_of_differ_characters(one_box_id, other_box_id)

    assert result == diffenences


def test_get_letters_in_common():
    box_ids = ["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"]
    answer = "fgij"

    result = get_letters_in_common(box_ids)

    assert result == answer
