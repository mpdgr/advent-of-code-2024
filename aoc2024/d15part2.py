# load data
d = [s.strip() for s in open('day15.txt', 'r').readlines()]

# dirs
# (row, col)
up, right, down, left = (-1, 0), (0, 1), (1, 0), (0, -1)

up_search, down_search = -1, 1
inv = (-1, -1)

# inputs
m = []
m_w = []
dirs = []

# helper vars
robot_pos = inv
visited = set()

# load matrix and directions
for l in d:
    if not l:
        pass
    elif l[0] == '#':
        m.append(list(l.strip()))
    else:
        for c in l.strip():
            dirs.append(c)

# widen matrix
for r, row in enumerate(m):
    n_row = []
    for c, column in enumerate(row):
        if m[r][c] == '#':
            n_row.extend(['#', '#'])
        elif m[r][c] == '.':
            n_row.extend(['.', '.'])
        elif m[r][c] == 'O':
            n_row.extend(['[', ']'])
        elif m[r][c] == '@':
            n_row.extend(['@', '.'])
    m_w.append(n_row)
m = m_w

# find robot
for r, row in enumerate(m):
    for c, column in enumerate(row):
        if m[r][c] == '@':
            robot_pos = r, c


def get_dir(d):
    if d == '^':
        return up
    elif d == '>':
        return right
    elif d == 'v':
        return down
    elif d == '<':
        return left


def target(pos, dir):
    d = get_dir(dir)
    return pos[0] + d[0], pos[1] + d[1]


def update_robot_pos(pos):
    global robot_pos
    robot_pos = pos


def can_move(pos, dir):
    t = target(pos, dir)
    return m[t[0]][t[1]] == '.'


def move_robot(pos, dir):
    t = target(pos, dir)
    m[t[0]][t[1]], m[pos[0]][pos[1]] = m[pos[0]][pos[1]], m[t[0]][t[1]]
    update_robot_pos(t)


def free_loc(pos, dir):
    t = target(pos, dir)
    while m[t[0]][t[1]] != '.' and m[t[0]][t[1]] != '#':
        t = target((t[0], t[1]), dir)
    if m[t[0]][t[1]] == '.':
        return t
    else:
        return inv


def all_to_move(pos, search_dir):
    atm = set()
    visited.add(pos)
    if m[pos[0]][pos[1]] == '#':
        atm.add(inv)
    elif m[pos[0]][pos[1]] == '[':
        atm.add(pos)
        if ((pos[0], pos[1] + 1) not in visited):
            atm.update(all_to_move((pos[0], pos[1] + 1), search_dir))
        atm.update(all_to_move((pos[0] + search_dir, pos[1]), search_dir))
    elif m[pos[0]][pos[1]] == ']':
        atm.add(pos)
        if ((pos[0], pos[1] - 1) not in visited):
            atm.update(all_to_move((pos[0], pos[1] - 1), search_dir))
        atm.update(all_to_move((pos[0] + search_dir, pos[1]), search_dir))
    return atm


def movable_group(atm):
    return inv not in atm


def move_group(atm, search_dir):  # only for up and down pushes
    atm_l = list(atm)
    rev = search_dir > 0
    atm_l_s = sorted(atm_l, key=lambda x: x[0], reverse=rev)
    for pos in atm_l_s:
        m[pos[0] + search_dir][pos[1]] = m[pos[0]][pos[1]]
        m[pos[0]][pos[1]] = '.'
    m[robot_pos[0]][robot_pos[1]] = '.'
    update_robot_pos((robot_pos[0] + search_dir, robot_pos[1]))
    m[robot_pos[0]][robot_pos[1]] = '@'


def fill_line(line_start, line_end):
    line_i = line_start[0]
    reverse = False
    for c in range(line_start[1], line_end[1] + 1):
        m[line_i][c] = '[' if not reverse else ']'
        reverse = not reverse


def h_push(pos, dir, push_t):  # only for left and right pushes
    t_r = target(pos, dir)

    if get_dir(dir) == left:
        t = pos[0], pos[1] - 1  # robot moves here
        line_end = pos[0], pos[1] - 2  # line ends here
        line_start = push_t
        fill_line(line_start, line_end)
        update_robot_pos(t)

    if get_dir(dir) == right:
        t = pos[0], pos[1] + 1  # robot moves here
        line_start = pos[0], pos[1] + 2
        line_end = push_t  # line ends here
        fill_line(line_start, line_end)
        update_robot_pos(t)

    m[pos[0]][pos[1]] = '.'
    m[t_r[0]][t_r[1]] = '@'


# measure matrix coords
def get_gps():
    val = 0
    for r, row in enumerate(m):
        for c, column in enumerate(row):
            if m[r][c] == '[':
                val = 100 * r + c + val
    return val

# run the program
for dir in dirs:
    if can_move(robot_pos, dir):
        move_robot(robot_pos, dir)
    elif get_dir(dir) == left or get_dir(dir) == right:
        free = free_loc(robot_pos, dir)
        if free != inv:
            h_push(robot_pos, dir, free)
    else:
        search_dir = up_search if get_dir(dir) == up else down_search
        all_t_m = all_to_move((robot_pos[0] + search_dir, robot_pos[1]), search_dir)
        if movable_group(all_t_m):
            move_group(all_t_m, search_dir)
        visited = set()


print(get_gps())
