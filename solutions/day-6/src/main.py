import numpy as np


def get_points():
    return [(78, 335), (74, 309), (277, 44), (178, 286), (239, 252), (118, 354), (170, 152), (75, 317), (156, 318), (172, 45), (138, 162), (261, 195), (306, 102), (282, 67), (53, 141), (191, 237), (352, 180), (95, 247), (353, 357), (201, 327), (316, 336), (57, 43), (119, 288), (299, 328), (125, 327), (187, 186), (121, 151), (121, 201), (43, 67), (76, 166), (238, 148), (326, 221), (219, 207), (237, 160), (345, 244), (321, 346), (48, 114), (304, 80), (265, 216), (191, 92), (54, 75), (118, 260), (336, 249), (81, 103), (290, 215), (300, 246), (293, 59), (150, 274), (296, 311), (264, 286)]
    # return [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]

def index_of_smallest(distances):
    _min = max(distances)
    index = -1
    for i in range(len(distances)):
        if distances[i] < _min:
            _min = distances[i]
            index = i
    return index


def make_grid(points, metric):
    x_length, y_length = grid_size(points)
    grid = np.zeros((x_length, y_length))
    for i in range(x_length):
        for j in range(y_length):
            index = metric(i, j, points)
            grid[i][j] = index
    return grid


def index_of_nearest_point(i, j, points):
    distances = get_distances(i, j, points)
    if sum(distances == min(distances)) > 1:
        index = -1
    else:
        index = index_of_smallest(distances)
    return index


def get_distances(i, j, points):
    distances = np.array([abs(i - x) + abs(j - y) for x, y in points])
    return distances


def grid_size(points):
    max_x, max_y = 0, 0
    for (x, y) in points:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    return max_x + 1, max_y + 1


def get_points_to_consider(grid, points):
    to_be_considered = set(range(len(points)))
    is_infinite = set()
    is_infinite |= set(grid[0, :])
    is_infinite |= set(grid[:, 0])
    is_infinite |= set(grid[grid.shape[0] - 1, :])
    is_infinite |= set(grid[:, grid.shape[1] - 1])
    return to_be_considered - is_infinite


def grid_to_string(grid, points):
    representation = ''
    mapping = {
        -1: '.',
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'f',
    }
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            letter = mapping[grid[i][j]]
            if (i, j) in points:
                letter = letter.upper()
            representation += letter
        representation += '\n'
    return representation


def point_within_total_distance(total_distance=10000):
    def metric(i, j, points):
        distances = get_distances(i, j, points)
        return 1 if sum(distances) <= total_distance else -1
    return metric


def part_2():
    points = get_points()
    grid = make_grid(points, point_within_total_distance())
    print(sum(sum(grid == 1)))


def part_1():
    points = get_points()
    grid = make_grid(points, index_of_nearest_point)
    points_to_consider = get_points_to_consider(grid, points)
    greatest_area = 0
    for point in points_to_consider:
        area = sum(sum(grid == point))
        if area > greatest_area:
            greatest_area = area
    print(greatest_area)


def run():
    part_1()
    part_2()


if __name__ == '__main__':
    run()
