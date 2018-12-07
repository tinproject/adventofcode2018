from copy import deepcopy


def parse_instruction(data):
    # returns -> task [0] is a dependant for task [1]
    if not data:
        raise ValueError
    return data[5:6], data[36:37]


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
    print(f"Part2 - ... is: {None}")


if __name__ == "__main__":
    solve()
