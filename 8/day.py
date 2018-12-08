

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


def get_node_value(node, index=0):
    num_children = node[0 + index]
    num_metadata = node[1 + index]

    _, end_node_index = get_node_metadata(node, index)
    metadata = node[end_node_index - num_metadata: end_node_index]
    end_index = 2 + index

    if num_children == 0:
        end_index += num_metadata
        return sum(metadata), end_index

    child_values = dict()
    for child in range(1, num_children + 1):
        v, end_index = get_node_value(node, end_index)
        child_values[child] = v

    value = sum(child_values[c] for c in metadata if c in child_values)
    end_index += num_metadata
    return value, end_index


def solve():
    data = parse_input(get_data())

    # Part 1
    license_code = get_metadata_sum(data)
    print(f"Part1 - The license code is: {license_code}")

    # Part 2
    node_value, _ = get_node_value(data)
    print(f"Part2 - The second check (node value) is: {node_value}")


if __name__ == "__main__":
    solve()
