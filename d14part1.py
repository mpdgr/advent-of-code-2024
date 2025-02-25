lines = [l for l in open('day14.txt', 'r').readlines()]

robots = {}
size_h = 101
size_v = 103
steps = 100

# quad (x_s, x_e, y_s, y_e)
quad_1 = (0, int(size_h / 2) - 1, 0, int(size_v / 2) - 1)
quad_2 = (int(size_h / 2) + 1, size_h - 1, 0, int(size_v / 2) - 1)
quad_3 = (0, int(size_h / 2) - 1, int(size_v / 2) + 1, size_v - 1)
quad_4 = (int(size_h / 2) + 1, size_h - 1, int(size_v / 2) + 1, size_v - 1)

for i, line in enumerate(lines):
    coords = line.split('=')[1].strip().split(',')
    dirs = line.split('=')[2].strip().split(',')
    robots[i] = (int(coords[0]), int(coords[1][:-2]), int(dirs[0]), int(dirs[1]))


def in_quad(x, y, quad):
    return quad[0] <= x <= quad[1] and quad[2] <= y <= quad[3]

def get_quad_index(x, y):
    if in_quad(x, y, quad_1):
        return 1
    if in_quad(x, y, quad_2):
        return 2
    if in_quad(x, y, quad_3):
        return 3
    if in_quad(x, y, quad_4):
        return 4
    return 0


# robot (start_x, start_y, dir_h, dir_v)
def comp_pos(start_x, start_y, dir_h, dir_v, steps) -> (int, int):
    end_x = (start_x + steps * dir_h) % size_h
    end_y = (start_y + steps * dir_v) % size_v
    return end_x, end_y


map = [0, 0, 0, 0]
for k in robots.keys():
    r = robots[k]
    pos = comp_pos(r[0], r[1], r[2], r[3], steps)
    q = get_quad_index(pos[0], pos[1])
    if q != 0:
        map[q - 1] = map[q - 1] + 1

t = 1
for v in map:
    t = t * v

print(t)
