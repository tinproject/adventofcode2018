
from day4 import Observation, get_guard_shifts, get_minutes_sleep, get_max_sleep_guard, get_minute_more_sleep, \
    get_minute_more_sleep_for_max_guard_sleeper


example_input_observations = sorted(l.strip() for l in str.splitlines(
"""
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""") if l)


def test_get_minutes_sleep():
    guard_shifts = get_guard_shifts(example_input_observations)

    result = get_minutes_sleep(guard_shifts)

    assert result[10] == 50
    assert result[99] == 30


def test_get_max_sleep_guard():
    guard_shifts = get_guard_shifts(example_input_observations)
    minutes_sleep = get_minutes_sleep(guard_shifts)

    result = get_max_sleep_guard(minutes_sleep)

    assert result == 10


def test_get_minute_more_sleep():
    guard_shifts = get_guard_shifts(example_input_observations)
    minutes_sleep = get_minutes_sleep(guard_shifts)
    max_sleeper = get_max_sleep_guard(minutes_sleep)

    result = get_minute_more_sleep(max_sleeper, guard_shifts)

    assert result == 24


def test_get_minute_more_sleep_for_max_guard_sleeper():
    guard_shifts = get_guard_shifts(example_input_observations)

    result = get_minute_more_sleep_for_max_guard_sleeper(guard_shifts)

    assert result == 240


def test_guard_begins_shift_observation():
    log_entry = "[1518-11-01 00:00] Guard #10 begins shift"

    observation = Observation(log_entry)

    assert observation.type == Observation.BEGIN_SHIFT
    assert observation.guard_id == 10
    assert observation.is_begin_shift()
    assert observation.date == "1518-11-01"
    assert observation.time == "00:00"


def test_guard_falls_asleep_observation():
    log_entry = "[1518-11-01 00:05] falls asleep"

    observation = Observation(log_entry)

    assert observation.type == Observation.FELT_ASLEEP
    assert observation.guard_id is None
    assert observation.is_felt_asleep()
    assert observation.date == "1518-11-01"
    assert observation.time == "00:05"


def test_guard_wake_up_observation():
    log_entry = "[1518-11-01 00:25] wakes up"

    observation = Observation(log_entry)

    assert observation.type == Observation.WAKE_UP
    assert observation.guard_id is None
    assert observation.is_wake_up()
    assert observation.date == "1518-11-01"
    assert observation.time == "00:25"
