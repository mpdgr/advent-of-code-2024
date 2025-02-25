# load data
d = [s.strip() for s in open('day15.txt', 'r').readlines()]

# dirs
# (row, col)
up = (-1, 0)
right = (0, 1)
down = (1, 0)
left = (0, -1)

inv = (-1, -1)

m = []
dirs = []
robot_pos = inv

# load matrix and directions
for l in d:
    if not l:
        pass
    elif l[0] == '#':
        m.append(list(l.strip()))
    else:
        for c in l.strip():
            dirs.append(c)

# find robot
for r, row in enumerate(m):
    for c, column in enumerate(row):
        if m[r][c] == '@':
            robot_pos = r, c


def get_direction(d):
    if d == '^':
        return up
    elif d == '>':
        return right
    elif d == 'v':
        return down
    elif d == '<':
        return left


def target(pos, dir):
    return pos[0] + dir[0], pos[1] + dir[1]


def update_robot_pos(pos):
    global robot_pos
    robot_pos = pos


def can_move(pos, dir):
    t = target(pos, get_direction(dir))
    return m[t[0]][t[1]] == '.'


def move(pos, dir):
    t = target(pos, get_direction(dir))
    m[t[0]][t[1]], m[pos[0]][pos[1]] = m[pos[0]][pos[1]], m[t[0]][t[1]]
    update_robot_pos(t)


def free_loc(pos, dir):
    t = target(pos, get_direction(dir))
    while m[t[0]][t[1]] != '.' and m[t[0]][t[1]] != '#':
        t = target((t[0], t[1]), get_direction(dir))
    if m[t[0]][t[1]] == '.':
        return t
    else:
        return inv


def push(pos, dir, push_t):
    t = target(pos, get_direction(dir))
    m[push_t[0]][push_t[1]] = 'O'
    m[pos[0]][pos[1]] = '.'
    m[t[0]][t[1]] = '@'
    update_robot_pos(t)


# measure matrix coords
def get_gps():
    val = 0
    for r, row in enumerate(m):
        for c, column in enumerate(row):
            if m[r][c] == 'O':
                val = 100 * r + c + val
    return val


# move
# can_move(dir)?
# if can swap
# if cant:
# can_push()
# if can push
# find first empty -> fill first empty
# change pos
for direction in dirs:
    if can_move(robot_pos, direction):
        move(robot_pos, direction)
        continue
    free = free_loc(robot_pos, direction)
    if free != inv:
        push(robot_pos, direction, free)
        continue

print(get_gps())