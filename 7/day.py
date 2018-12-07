from collections import deque
from copy import deepcopy


def parse_instruction(data):
    # returns -> task [0] is a dependant for task [1]
    if not data:
        raise ValueError
    return data[5:6], data[36:37]


def get_step_time(step_name, setup=60):
    step_time = ord(step_name) - ord('A') + 1
    return step_time + setup


def process_instructions(instructions):
    all_tasks = set()
    task_depends_on = dict()  # task_depends_on[task] = set(prerequisites)
    task_dependants = dict()

    for op in instructions:
        first, second = parse_instruction(op)
        all_tasks.add(first)
        all_tasks.add(second)
        first_task_dependants = task_dependants.get(first, set())
        first_task_dependants.add(second)
        task_dependants[first] = first_task_dependants
        second_task_depends_on = task_depends_on.get(second, set())
        second_task_depends_on.add(first)
        task_depends_on[second] = second_task_depends_on

    return deepcopy(all_tasks), deepcopy(task_depends_on), deepcopy(task_dependants)


def get_instructions_order(instructions):
    all_tasks, task_depends_on, task_dependants = process_instructions(instructions)

    task_order = []
    for _ in range(1000000):
        tasks_with_no_prerequisites = list(sorted(t for t in all_tasks if t not in task_depends_on))
        if not tasks_with_no_prerequisites:
            break
        step = tasks_with_no_prerequisites[0]
        all_tasks.remove(step)
        if step in task_depends_on:
            del task_depends_on[step]
        # remove task from dependencies as its completed
        empty_dependants = []
        for k, v in task_depends_on.items():
            if step in v:
                v.remove(step)
                task_depends_on[k] = v
            if not v:
                empty_dependants.append(k)
        for k in empty_dependants:
            # Task have an empty set of dependencies -> remove from dict
            del task_depends_on[k]
        task_order.append(step)

    return "".join(task_order)


def get_construction_time(instructions, num_workers, setup_time):
    pending_tasks, task_depends_on, task_dependants = process_instructions(instructions)

    class Worker:
        def __init__(self):
            # Worker with task = None is idle
            self.task = None
            # ended_time is when task is already finised
            self.ended_time = 0

        def is_idle(self, second):
            return self.task is None and self.ended_time <= second

        def task_just_finished(self, second):
            if self.ended_time == second:
                finished_task = self.task
                self.task = None
                return finished_task
            return None

        def is_working(self, second):
            return self.task is not None and self.ended_time > second

        def assign_task(self, task, second):
            if self.is_working(second):
                raise ValueError
            self.task = task
            self.ended_time = second + get_step_time(task, setup_time)
            pending_tasks.remove(task)
            work_in_progress.add(task)

        def __repr__(self):
            return f"Task {self.task}, ended: {self.ended_time}"

    workers = [Worker() for _ in range(num_workers)]
    work_in_progress = set()

    def complete_task(task):
        work_in_progress.remove(task)
        # Update dependants
        for dependant in task_dependants.get(task, set()):
            prereqs = task_depends_on[dependant]
            prereqs.remove(task)
            if not prereqs:
                # Dependant task do not have any dependencies now, remove
                del task_depends_on[dependant]
        if task in task_dependants:
            del task_dependants[task]  # task do not have dependants as it's completed

    for second in range(1000000):
        # Check work in progess
        for worker in workers:
            task = worker.task_just_finished(second)
            if task is not None:
                complete_task(task)

        # Assign work to idle workers
        tasks_available = deque(sorted(t for t in pending_tasks if t not in task_depends_on))
        for i, worker in enumerate(workers):
            if tasks_available:
                if worker.is_idle(second):
                    step = tasks_available.popleft()
                    worker.assign_task(step, second)

        if not pending_tasks and not work_in_progress:
            # we finish
            return second


def get_data():
    with open('./input', 'rt') as f:
        values = [line.strip() for line in f.readlines()]
    return values


def solve():
    data = get_data()

    steps_order = get_instructions_order(data)
    # Part 1
    print(f"Part1 - The steps order is: {steps_order}")

    # Part 2
    num_workers = 5
    setup_time = 60
    construction_time = get_construction_time(data, num_workers, setup_time)
    print(f"Part2 - The total construction time is: {construction_time}")


if __name__ == "__main__":
    solve()
