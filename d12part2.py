# load matrix
m = [s.strip() for s in open('day12.txt', 'r').readlines()]

# bounds
up_bound = 0
down_bound = len(m) - 1
left_bound = 0
right_bound = len(m[0]) - 1

# map of regions
# key - tuple (letter, (r_start))
# value list of tuples (r, c)
regions = {}

# map of borders
# key - tuple (r, c) value = nr of borders
borders = {}

all_visited = set()


def visited(r, c):
    return (r, c) in all_visited


def neighbor(r, c):
    return m[r][c]


def visit(r, c, peer_set) -> set:
    if visited(r, c):
        return peer_set
    else:
        all_visited.add((r, c))

    im_parent = False
    # if peer list is empty Im the region parent
    if not peer_set:
        peer_set = set()
        im_parent = True

    # add my pos to peer list
    peer_set.add((r, c))
    val = m[r][c]
    all_visited.add((r, c))

    # find border walls
    fence = 0
    if r == up_bound or neighbor(r - 1, c) != val:
        # has up fence
        if not (r == up_bound and c != left_bound and m[r][c - 1] == val
                or r != up_bound and c != left_bound and m[r][c - 1] == val and m[r - 1][c - 1] != val):
            fence = fence + 1
    if r == down_bound or neighbor(r + 1, c) != val:
        # has down fence
        if not (r == down_bound and c != left_bound and m[r][c - 1] == val
                or r != down_bound and c != left_bound and m[r][c - 1] == val and m[r + 1][c - 1] != val):
            fence = fence + 1
    if c == left_bound or neighbor(r, c - 1) != val:
        # has left fence
        if not (c == left_bound and r != up_bound and m[r - 1][c] == val
                or c != left_bound and r != up_bound and m[r - 1][c] == val and m[r - 1][c - 1] != val):
            fence = fence + 1
    if c == right_bound or neighbor(r, c + 1) != val:
        # has right fence
        if not (c == right_bound and r != up_bound and m[r - 1][c] == val
                or c != right_bound and r != up_bound and m[r - 1][c] == val and m[r - 1][c + 1] != val):
            fence = fence + 1
    borders[(r, c)] = fence

    # visit unvisited neighbors
    if r != up_bound and not visited(r - 1, c) and neighbor(r - 1, c) == val:
        peer_set.update(visit(r - 1, c, peer_set))
    if r != down_bound and not visited(r + 1, c) and neighbor(r + 1, c) == val:
        peer_set.update(visit(r + 1, c, peer_set))
    if c != left_bound and not visited(r, c - 1) and neighbor(r, c - 1) == val:
        peer_set.update(visit(r, c - 1, peer_set))
    if c != right_bound and not visited(r, c + 1) and neighbor(r, c + 1) == val:
        peer_set.update(visit(r, c + 1, peer_set))

    # visiting finished - if im parent I must register a region
    if im_parent:
        regions[(val, (r, c))] = peer_set

    return peer_set


# traverse all cells
for r, line in enumerate(m):
    for c, char in enumerate(list(line)):
        visit(r, c, set())

# list of all regions (letter, score)
reg_l = []

# regions - tuple (letter, (r_start)) value list of tuples (r, c)
for region in regions.keys():
    # plant type
    val = region[0]
    # all neighbors including parent
    all_locs = set(regions[region])
    # neighbors count
    loc_count = len(all_locs)
    loc_fence_counter = 0
    for loc in all_locs:
        loc_fence_counter = loc_fence_counter + borders[loc]  # add borders count from each loc
    region_score_t = loc_count * loc_fence_counter
    reg_l.append((val, region_score_t))

das_total = 0
for r in reg_l:
    das_total = das_total + r[1]

print(f'Total: {das_total}')
