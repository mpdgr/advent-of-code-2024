import math

lines = [l for l in open('day14.txt', 'r').readlines()]

robots = {}
size_h = 101
size_v = 103

for i, line in enumerate(lines):
    coords = line.split('=')[1].strip().split(',')
    dirs = line.split('=')[2].strip().split(',')
    robots[i] = (int(coords[0]), int(coords[1][:-2]), int(dirs[0]), int(dirs[1]))


# robot (start_x, start_y, dir_h, dir_v)
# position after given number of steps
def comp_pos(start_x, start_y, dir_h, dir_v, steps) -> (int, int):
    end_x = (start_x + steps * dir_h) % size_h
    end_y = (start_y + steps * dir_v) % size_v
    return end_x, end_y


# map all positions after given nr of steps
def all_pos(robots, steps) -> (int, int):
    mapping = list()
    for k in robots.keys():
        r = robots[k]
        mapping.append(comp_pos(r[0], r[1], r[2], r[3], steps))
    return mapping

# assume robots/points on Christmas tree picture will be clustered somehow,
# so on average positioned closer to each other, compared to random setups
# - so compute dispersion rate for every picture, min will likely indicate the tree
# (for each point comp mean distance from center defined by average of all points positions)


# compute mean (x, y) position for all points in space
def center_xy(mapping):
    x_sum = 0
    y_sum = 0
    for x, y in mapping:
        x_sum += x
        y_sum += y
    return x_sum / len(mapping), y_sum / len(mapping)


def mean_dist_from_center(mapping, center):
    # distance from center for each point
    dist = list()
    c_x, c_y = center[0], center[1]
    for p in mapping:
        p_x, p_y = p[0], p[1]
        dist_x = p_x - c_x if p_x > c_x else c_x - p_x
        dist_y = p_y - c_y if p_y > c_y else c_y - p_y
        dist.append(math.sqrt(math.pow(dist_x, 2) + math.pow(dist_y, 2)))
    # mean distance from center for all points
    return sum(dist) / len(dist)


# compute mean distance from center for all points after given nr of steps
def dist_mean(robots, steps):
    mapping = all_pos(robots, steps)
    center = center_xy(mapping)
    return mean_dist_from_center(mapping, center)


def print_choinka(mapping):
    for y in range(0, 103):
        for x in range(0, 101):
            val = 'X' if (x, y) in mapping else '.'
            print(val, end="")
        print('')


means = []
for i in range(0, 10_000):  # assume 10k is enough to find the tree
    means.append((i, dist_mean(robots, i)))

min_dispersion_steps = min(means, key=lambda x: x[1])[0]
print(f'Steps to tree: {min_dispersion_steps}')

print_choinka(all_pos(robots, min_dispersion_steps))
