

def parse_input(data):
    return [int(v.strip()) for v in data[0].split()]


def get_data():
    with open('./input', 'rt') as f:
        values = [line.strip() for line in f.readlines()]
    return values


def get_node_metadata(node, index=0):
    num_children = node[0 + index]
    num_metadata = node[1 + index]

    metadata = []
    end_index = 2 + index
    while num_children > 0:
        m, end_index = get_node_metadata(node, end_index)
        metadata += m
        num_children -= 1

    metadata += node[end_index:end_index+num_metadata]
    end_index += num_metadata

    return metadata, end_index


def get_metadata_sum(node):
    metadata, _ = get_node_metadata(node)
    return sum(metadata)


def get_node_value(node):
    pass


def solve():
    data = parse_input(get_data())

    # Part 1
    license_code = get_metadata_sum(data)
    print(f"Part1 - The license code is: {license_code}")

    # Part 2
    print(f"Part2 - ... is: {None}")


if __name__ == "__main__":
    solve()
