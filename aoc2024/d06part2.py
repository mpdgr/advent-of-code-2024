m = [s.strip() for s in open('day6.txt', 'r').readlines()]
all_blocks = set()
total_blocks = 0
stp = ()
dir_nr = [0, 1, 2, 3]
up_bound = 0
down_bound = len(m) - 1
left_bound = 0
right_bound = len(m[0]) - 1
counter = 0


def next_dir(current_dir):
    return dir_nr[(current_dir + 1) % 4]


def in_bounds(pos):
    return not (pos[0] < up_bound or pos[0] > down_bound or pos[1] < left_bound or pos[1] > right_bound)


def next_pos(current_pos):
    if current_dir == 0:
        return current_pos[0] - 1, current_pos[1]
    if current_dir == 1:
        return current_pos[0], current_pos[1] + 1
    if current_dir == 2:
        return current_pos[0] + 1, current_pos[1]
    if current_dir == 3:
        return current_pos[0], current_pos[1] - 1


# find starting position
for r in range(1, len(m) - 1):
    for c in range(1, len(list(m[r])) - 1):
        if m[r][c] == '^':
            current_pos = (r, c)
            stp = current_pos


# copy matrix
for rt in range(0, len(m)):
    counter = counter + 1
    for ct in range(0, len(list(m[rt]))):
        # copy matrix
        v = [r[:] for r in m]
        if v[rt][ct] in ('^', '#'):
            continue
        # insert block
        v[rt] = m[rt][:ct] + '#' + m[rt][ct + 1:]
        visited = set()
        current_pos = stp
        current_dir = 0
        in_bnds = True

        # walk
        while in_bnds:
            next_field = next_pos(current_pos)
            if not in_bounds(next_field):
                in_bnds = False
            elif v[next_field[0]][next_field[1]] != '.' and v[next_field[0]][next_field[1]] != '^':
                current_dir = next_dir(current_dir)
            else:
                current_pos = next_field
                if (current_pos, current_dir) in visited:
                    all_blocks.add((rt, ct))
                    break
                visited.add((current_pos, current_dir))

print(f'Cycling blocks: {len(all_blocks)}')
