import pytest

from day1 import calibration, find_duplicate_frequency


@pytest.mark.parametrize("calibration_values,frequency", [
    ([+1, -2, +3, +1], 3),
    ([+1, +1, +1], 3),
    ([+1, +1, -2], 0),
    ([-1, -2, -3], -6),
])
def test_calibration(calibration_values, frequency):
    result = calibration(calibration_values)

    assert result == frequency


@pytest.mark.parametrize("calibration_values,frequency", [
    ([+1, -1], 0),
    ([+3, +3, +4, -2, -4], 10),
    ([-6, +3, +8, +5, -6], 5),
    ([+7, +7, -2, -7, -4], 14),

])
def test_find_duplicate_frequency(calibration_values, frequency):
    result = find_duplicate_frequency(calibration_values)

    assert result == frequency
