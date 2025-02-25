m = [s.strip() for s in open('day6.txt', 'r').readlines()]  # create matrix
start_pos = ()
visited = set()
current_pos = ()
current_dir = 0

dir_nr = [0, 1, 2, 3]

up_bound = 0
down_bound = len(m) - 1
left_bound = 0
right_bound = len(m[0]) - 1


def next_dir():
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
            visited.add(current_pos)

# walk
while in_bounds:
    next_field = next_pos(current_pos)
    if not in_bounds(next_field):
        in_bounds = False
    elif m[next_field[0]][next_field[1]] not in ('.', '^'):
        current_dir = next_dir()
    else:
        current_pos = next_field
        visited.add(current_pos)

print(f"Total: {len(visited)}")
