import heapq

# load matrix
m = [s.strip() for s in open('day16.txt', 'r').readlines()]

vertices = set()    # (loc)
adj_matrix = {}     # (loc) -> ((loc), dist)
start = ()
end = ()

turn_cost = 1000
step_cost = 1

up, right, down, left = (-1, 0), (0, 1), (1, 0), (0, -1)

v_locs = ('.', 'S', 'E')

# get all coordinates
for r, row in enumerate(m):
    for c, column in enumerate(row):
        if m[r][c] in v_locs:
            vertices.add((r, c))
            adj_matrix[(r, c)] = []
        if m[r][c] == 'S':
            start = r, c
        if m[r][c] == 'E':
            end = r, c

# create adjacency matrix
for v in vertices:
    # up
    if m[v[0] - 1][v[1]] in v_locs:
        adj_matrix[(v[0], v[1])].append(((v[0] - 1, v[1]), 1))
    # right
    if m[v[0]][v[1] + 1] in v_locs:
        adj_matrix[(v[0], v[1])].append(((v[0], v[1] + 1), 1))
    # down
    if m[v[0] + 1][v[1]] in v_locs:
        adj_matrix[(v[0], v[1])].append(((v[0] + 1, v[1]), 1))
    # left
    if m[v[0]][v[1] - 1] in v_locs:
        adj_matrix[(v[0], v[1])].append(((v[0], v[1] - 1), 1))


# parse all corners and lines:
#
#       * *
#       *
#
#     * * *
#

# get candidates for a change
all_corners = set()     #(neighbor_1_loc, neighbor_2_loc, center_loc)
all_lines = set()       #(neighbor_1_loc, neighbor_2_loc, center_loc)


# solve corner: for both participants create vertex value 1002, from middle value remove vertices,
# from neighbor remove middle value
def solve_corner(n1, n2, owner):
    adj_matrix[n1].append(((n2[0], n2[1]), turn_cost + 2 * step_cost))
    adj_matrix[n2].append(((n1[0], n1[1]), turn_cost + 2 * step_cost))
    if ((owner[0], owner[1]), step_cost) in adj_matrix[n1]:
        adj_matrix[n1].remove(((owner[0], owner[1]), step_cost))
    if ((owner[0], owner[1]), step_cost) in adj_matrix[n2]:
        adj_matrix[n2].remove(((owner[0], owner[1]), step_cost))
    if ((n1[0], n1[1]), step_cost) in adj_matrix[owner]:
        adj_matrix[owner].remove(((n1[0], n1[1]), step_cost))
    if ((n2[0], n2[1]), step_cost) in adj_matrix[owner]:
        adj_matrix[owner].remove(((n2[0], n2[1]), step_cost))


# solve line: for both participants create vertex value 2, from middle value remove vertices,
# from neighbor remove middle value
def solve_line(n1, n2, owner):
    adj_matrix[n1].append(((n2[0], n2[1]), 2 * step_cost))
    adj_matrix[n2].append(((n1[0], n1[1]), 2 * step_cost))
    if ((owner[0], owner[1]), step_cost) in adj_matrix[n1]:
        adj_matrix[n1].remove(((owner[0], owner[1]), step_cost))
    if ((owner[0], owner[1]), step_cost) in adj_matrix[n2]:
        adj_matrix[n2].remove(((owner[0], owner[1]), step_cost))
    if ((n1[0], n1[1]), step_cost) in adj_matrix[owner]:
        adj_matrix[owner].remove(((n1[0], n1[1]), step_cost))
    if ((n2[0], n2[1]), step_cost) in adj_matrix[owner]:
        adj_matrix[owner].remove(((n2[0], n2[1]), step_cost))


def get_loc(neighbor):
    return neighbor[0], neighbor[1]


for center in adj_matrix.keys():
    # corners candidates
    all_neighbors = adj_matrix[center]
    has_corner = False
    for i, n in enumerate(all_neighbors):
        for j in range(i + 1, len(all_neighbors)):
            neighbor_1_loc = all_neighbors[i][0]
            neighbor_2_loc = all_neighbors[j][0]
            if neighbor_1_loc[0] != neighbor_2_loc[0] and neighbor_1_loc[1] != neighbor_2_loc[1] :
                # are corner!
                all_corners.add((neighbor_1_loc, neighbor_2_loc, center))
                has_corner = True
    if has_corner:
        for i, n in enumerate(all_neighbors):
            for j in range(i + 1, len(all_neighbors)):
                neighbor_1_loc = all_neighbors[i][0]
                neighbor_2_loc = all_neighbors[j][0]
                if neighbor_1_loc[0] == neighbor_2_loc[0] or neighbor_1_loc[1] == neighbor_2_loc[1]:
                    # are aligned!
                    all_lines.add((neighbor_1_loc, neighbor_2_loc, center))

for corner in all_corners:
    solve_corner(corner[0], corner[1], corner[2])

for line in all_lines:
    solve_line(line[0], line[1], line[2])


# solve start and end
def solve_start():
    adj_matrix[start] = []
    adj_matrix[start].append(((start[0], start[1] + 1), step_cost))
    adj_matrix[start].append(((start[0] - 1, start[1]), turn_cost + step_cost))
    n_state[start] = (False, 0, None)


def solve_end():
    adj_matrix[end] = []
    adj_matrix[end].append(((end[0] + 1, end[1]), step_cost))
    adj_matrix[end].append(((end[0], end[1] - 1), step_cost))

    adj_matrix[(end[0], end[1] - 1)].append((end, step_cost))
    adj_matrix[(end[0] + 1, end[1])].append((end, step_cost))


# dict of current nodes state:
# loc -> resolved, dist, path_ptr
n_state = {}

# init states
for loc in adj_matrix.keys():
    n_state[loc] = (False, -1, None)

solve_start()
solve_end()

# walk:
# start walk -> examine all adj
# while loc = end
# for each adj, save cost and pointer to incoming
# choose lowest cost
# move
# locations stored in a priority queue

visited_count = 0

# location node:
# heapq locs to visit
# pointer to incoming path
max_heapq = 0


def djks(start, target):    # dijkstra search
    global max_heapq
    visited_count = 0
    current_loc = start
    resolve_queue = []
    while current_loc != target:
        visited_count = visited_count + 1
        cost_to_here = n_state[current_loc][1]
        # get neighbors
        for neighbor in adj_matrix[current_loc]:
            neighbor_loc = neighbor[0]
            neighbor_state = n_state[neighbor_loc]
            if neighbor_state[0] == True:   # it is already resolved -> do nothing
                continue
            neighbor_lowest_cost = neighbor_state[1]
            cost_to_go = neighbor[1]
            if neighbor_lowest_cost == -1 or cost_to_here + cost_to_go < neighbor_lowest_cost:
                # update neighbor state
                neighbor_lowest_cost = cost_to_here + cost_to_go
                n_state[neighbor_loc] = (False, neighbor_lowest_cost, current_loc)
                # add neighbor to resolve queue
                heapq.heappush(resolve_queue, (neighbor_lowest_cost, neighbor_loc))
                if len(resolve_queue) > max_heapq:
                    max_heapq = len(resolve_queue)
        # current location is resolved -> update state
        state_before_update = n_state[current_loc]
        state_after_update = (True, state_before_update[1], state_before_update[2])
        n_state[current_loc] = state_after_update
        # move to next visit
        new_loc = heapq.heappop(resolve_queue)[1]
        current_loc = new_loc
    return n_state[current_loc][1]

das_total = djks(start, end)
print(f'Total: {das_total}')
