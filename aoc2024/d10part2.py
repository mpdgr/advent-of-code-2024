m = [s.strip() for s in open('day10.txt', 'r').readlines()]

# bounds
up_bound = 0
down_bound = len(m) - 1
left_bound = 0
right_bound = len(m[0]) - 1

# find heads
heads = set()
for r in range(0, len(m)):
    for c in range(0, len(list(m[r]))):
        if m[r][c] == '0':
            pos = (r, c)
            heads.add(pos)

# paths from head do target
head_targets = {}
for head in heads:
    head_targets[head] = list()


def height(r, c):
    return int(m[r][c])


# walk from given position
def walk(r, c, start_pos):
    # height
    h = height(r, c)
    # if we reached the target
    if h == 9:
        head_targets[start_pos].append((r, c))
        return
    # go up
    if r > up_bound and height(r - 1, c) == h + 1:
        walk(r - 1, c, start_pos)
    # go down
    if r < down_bound and height(r + 1, c) == h + 1:
        walk(r + 1, c, start_pos)
    # go left
    if c > left_bound and height(r, c - 1) == h + 1:
        walk(r, c - 1, start_pos)
    # go right
    if c < right_bound and height(r, c + 1) == h + 1:
        walk(r, c + 1, start_pos)


def comp_total():
    total_trails = 0
    for head in head_targets.keys():
        total_trails += len(head_targets[head])
    return total_trails


# do a walk and comp totals
for head in heads:
    walk(head[0], head[1], head)

print(f'Total: {comp_total()}')
