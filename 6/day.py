from collections import Counter
from itertools import chain
from functools import partial
# import string


def get_coordinates(data):
    clean_data = (l.strip() for l in data if l.strip())
    coords = []
    for d in clean_data:
        x = int(d.split(",")[0].strip())
        y = int(d.split(",")[1].strip())
        coords.append((x, y))
    return sorted(coords)


def get_bounding_box(coords):
    min_x = min(coords, key=lambda i: i[0])[0]
    max_x = max(coords, key=lambda i: i[0])[0]
    min_y = min(coords, key=lambda i: i[1])[1]
    max_y = max(coords, key=lambda i: i[1])[1]
    return [(min_x, min_y), (max_x, max_y)]


def point_has_infinite_area(coords, point):
    coords = list(coords)
    x = point[0]
    y = point[1]

    points_in_border = (
        next(chain(filter(lambda p: p[0] >= x and p[1] > y, coords)), False),
        next(chain(filter(lambda p: p[0] < x and p[1] >= y, coords)), False),
        next(chain(filter(lambda p: p[0] <= x and p[1] < y, coords)), False),
        next(chain(filter(lambda p: p[0] > x and p[1] <= y, coords)), False),
    )
    return not all(points_in_border)


def distance(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])


def get_points_with_infinite_area(coords):
    filter_infinite_area = partial(point_has_infinite_area, coords)

    return list(filter(filter_infinite_area, coords))


def get_shortest_point(place, points):
    distances = sorted(((distance(place, p), p) for p in points))
    if distances[0][0] == distances[1][0]:
        # Same distance to more than one point
        return None
    return distances[0][1]


def get_distance_matrix(coords, border):
    # infinite_area_points = get_points_with_infinite_area(coords)
    bounding_box = get_bounding_box(coords)
    max_x = bounding_box[1][0] + border + 10
    max_y = bounding_box[1][1] + border + 10

    distance_matrix = dict()
    for i in range(-border, max_x):
        for j in range(-border, max_y):
            place = (i, j)
            distance_matrix[place] = get_shortest_point(place, coords)

    # # Get map
    # point_ids = {p: i for p, i in zip(coords, chain(string.ascii_letters, string.digits))}
    # point_ids[None] = "·"
    # dm = {k: point_ids[v] for k, v in sorted(distance_matrix.items())}
    # for p in coords:
    #     dm[p] = "#"
    # out = []
    # for i in range(-border, max_x):
    #     line = []
    #     for j in range(-border, max_y):
    #         line.append(dm[(i, j)])
    #     out.append("".join(line))
    # print(out)

    return distance_matrix


def get_largest_area_point(coords):

    dm1 = get_distance_matrix(coords, 0)
    dm2 = get_distance_matrix(coords, 100)
    c1 = Counter(dm1.values())
    c2 = Counter(dm2.values())

    non_expansive = [(p, d) for p, d in c1.items() if c2[p] == d]
    max_area = sorted(non_expansive, key=lambda x: x[1], reverse=True)[0]
    return max_area


def get_largest_area(coords):
    point, size = get_largest_area_point(coords)
    return size


def get_data():
    with open('./input', 'rt') as f:
        values = f.readlines()
    return values


def solve():
    data = get_data()

    coords = get_coordinates(data)
    largest_area_size = get_largest_area(coords)

    # Part 1
    print(f"Part1 - The largest non infinite area is: {largest_area_size}")

    # Part 2
    print(f"Part2 - ... is: {None}")


if __name__ == "__main__":
    solve()
