from array import array
from itertools import repeat
import re


class Observation:
    BEGIN_SHIFT = 0
    FELT_ASLEEP = 1
    WAKE_UP = 2

    _re_action_begins_shift = re.compile(r"Guard #(?P<guard_id>\d+) begins shift")

    def __init__(self, log_entry):
        self.date = log_entry[1:11]
        self.time = log_entry[12:17]
        action = log_entry[19:]
        begin_shift = self._re_action_begins_shift.match(action)
        if begin_shift:
            self.type = self.BEGIN_SHIFT
            self.guard_id = int(begin_shift.group('guard_id'))
        elif action == "falls asleep":
            self.type = self.FELT_ASLEEP
            self.guard_id = None
        elif action == "wakes up":
            self.type = self.WAKE_UP
            self.guard_id = None
        else:
            raise ValueError(f"Unrecogniced observation type: {log_entry}")

    def is_begin_shift(self):
        return self.type == self.BEGIN_SHIFT

    def is_felt_asleep(self):
        return self.type == self.FELT_ASLEEP

    def is_wake_up(self):
        return self.type == self.WAKE_UP


class GuardShift:
    TIMETABLE_MINUTES = 60
    STATE_NOT_PRESENT = 0
    STATE_AWAKE = 1
    STATE_ASLEEP = 2

    def __init__(self, observation):
        if observation.guard_id is None:
            raise ValueError("We need an operation of begin shift with a valid guard_id")
        self.guard_id = observation.guard_id
        self.timetable = array('i', repeat(self.STATE_NOT_PRESENT,  self.TIMETABLE_MINUTES))
        self.observations = [observation]
        self.processed = False

    def observe(self, action):
        self.observations.append(action)

    def _get_efective_minute(self, observation):
        if observation.time[:2] == "23":
            minutes = 0
        elif observation.time[:2] == "00":
            minutes = int(observation.time[3:])
        else:
            raise ValueError(f"Don't know how to process this time: {observation.time}")
        return minutes

    def _record_span(self, start, end, state):
        for i in range(start, end):
            self.timetable[i] = state

    def process_shift(self):
        current_state = self.STATE_NOT_PRESENT
        last_state = self.STATE_NOT_PRESENT
        # We suppose observations are ordered, as we orde the input
        for observation in self.observations:
            if observation.is_begin_shift():
                if current_state != self.STATE_NOT_PRESENT:
                    raise ValueError("Can't start a shift if is already present")
                last_state, current_state = current_state, self.STATE_AWAKE
                self._record_span(self._get_efective_minute(observation), self.TIMETABLE_MINUTES, current_state)
                last_observation = observation

            elif observation.is_felt_asleep():
                if current_state != self.STATE_AWAKE:
                    raise ValueError(f"Bad previous status {last_state}")
                last_state, current_state = current_state, self.STATE_ASLEEP
                last_observation = observation

            elif observation.is_wake_up():
                if current_state != self.STATE_ASLEEP:
                    raise ValueError(f"Bad previous status {last_state}")
                last_state, current_state = current_state, self.STATE_AWAKE
                self._record_span(
                    self._get_efective_minute(last_observation),
                    self._get_efective_minute(observation),
                    last_state,
                )
                last_observation = observation
            else:
                raise ValueError(f"Unknown observation: {observation}")
        self.processed = True

    def get_asleep_minutes(self):
        if not self.processed:
            self.process_shift()
        return self.timetable.count(self.STATE_ASLEEP)

    def get_state_for_minute(self, minute):
        return self.timetable[minute]


def get_guard_shifts(log_entries):
    guard_shifts = []
    current_guard_shift = None

    for log_entry in log_entries:
        observation = Observation(log_entry)

        if observation.is_begin_shift():
            current_guard_shift = GuardShift(observation)
            guard_shifts.append(current_guard_shift)

        elif observation.is_felt_asleep() or observation.is_wake_up():
            current_guard_shift.observe(observation)
    return guard_shifts


def get_minutes_sleep(guard_shifts):
    minutes_sleep = {}
    for g, m in map(lambda x: (x.guard_id, x.get_asleep_minutes()), guard_shifts):
        minutes_sleep[g] = minutes_sleep.get(g, 0) + m

    return minutes_sleep


def get_max_sleep_guard(minutes_sleep):
    max_sleep = 0
    guard_id = None
    for g, m in minutes_sleep.items():
        if m >= max_sleep:
            max_sleep = m
            guard_id = g
    return guard_id


def get_minute_more_sleep(guard_id, guard_shifts):
    guard_duty = (s for s in guard_shifts if s.guard_id == guard_id)
    minutes = list(0 for _ in range(GuardShift.TIMETABLE_MINUTES))

    for shift in guard_duty:
        for i in range(len(minutes)):
            sleep = 1 if shift.get_state_for_minute(i) == GuardShift.STATE_ASLEEP else 0
            minutes[i] += sleep

    return max(enumerate(minutes), key=lambda x: x[1])[0]


def get_minute_more_sleep_for_max_guard_sleeper(guard_shifts):
    minutes_sleep = get_minutes_sleep(guard_shifts)
    max_sleeper = get_max_sleep_guard(minutes_sleep)

    minute_most_sleep = get_minute_more_sleep(max_sleeper, guard_shifts)

    return max_sleeper * minute_most_sleep


def get_data():
    with open('./input', 'rt') as f:
        values = sorted(line.strip() for line in f.readlines())
    return values


def solve():
    data = get_data()

    guard_shifts = get_guard_shifts(data)

    code = get_minute_more_sleep_for_max_guard_sleeper(guard_shifts)

    # Part 1
    print(f"Part1 - The solution is: {code}")

    # Part 2
    print(f"Part2 - ... is: {None}")


if __name__ == "__main__":
    solve()
