import heapq

# load maze
maze = [s for s in open('day20.txt', 'r').readlines()]

# constants
inf = 1_000_000
width = len(maze[0])
height = len(maze)
open = {'.', 'S', 'E'}

# start/end track
start = (0, 0)
end = (0, 0)


def find_vertices():
    global start
    global end
    for r, line in enumerate(maze):
        for c, char in enumerate(line):
            if char in open:
                vertices.append((r, c))
            if char == 'S':
                start = ((r, c))
            if char == 'E':
                end = ((r, c))


def find_holes():
    for r, line in enumerate(maze):
        for c, char in enumerate(line):
            if c < width - 2 and char in open and maze[r][c + 1] == '#' and maze[r][c + 2] in open:
                holes.append((r, c + 1))
            if r < height - 2 and char in open and maze[r + 1][c] == '#' and maze[r + 2][c] in open:
                holes.append((r + 1, c))


# find vertices
vertices = []
find_vertices()

# find possible holes
holes = []
find_holes()


def create_adj_matrix(vertices):
    adj_matrix = {}
    for v in vertices:
        adj_matrix[(v[0], v[1])] = []

    for r, c in vertices:
        if (r + 1, c) in vertices:
            adj_matrix[r, c].append((r + 1, c))
        if (r - 1, c) in vertices:
            adj_matrix[r, c].append((r - 1, c))
        if (r, c + 1) in vertices:
            adj_matrix[r, c].append((r, c + 1))
        if (r, c - 1) in vertices:
            adj_matrix[r, c].append((r, c - 1))

    return adj_matrix


# single run
def shortest_path(holes):
    # init vertices
    v = vertices[:]
    # add holes
    for h in holes:
        v.append((h[0], h[1]))
    # create adjacency matrix
    adj_matrix = create_adj_matrix(v)

    # init states
    vertice_state = {}
    for v in adj_matrix.keys():
        vertice_state[v] = (inf, None)
    vertice_state[start] = (0, None)

    # init queue
    resolve_queue = []
    for v, s in adj_matrix.items():
        heapq.heappush(resolve_queue, (vertice_state[v][0], v))

    # dist counter
    total_dist = -1
    resolved = set()

    while resolve_queue:
        visited = heapq.heappop(resolve_queue)
        dist = visited[0]
        loc = visited[1]
        resolved.add(loc)
        if loc == end:
            total_dist = dist
            break
        for n in adj_matrix[loc]:
            if vertice_state[n][0] > dist + 1 and n not in resolved:
                vertice_state[n] = (dist + 1, loc)
                heapq.heappush(resolve_queue, (dist + 1, n))

    return total_dist, vertice_state


das_total = shortest_path([])
print(f'total: {das_total[0]}')

states = das_total[1]

track = set()
track_d = dict()
next_loc = end
# get path
while next_loc is not None:
    s = states[next_loc]
    pointer = s[1]
    track.add(pointer)
    track_d[next_loc] = s[0]
    next_loc = pointer

track.add(start)
track.add(end)

track_d[start] = 0
track_d[end] = das_total[0]

# remove invalid holes
valid_holes_vertical = set()
valid_holes_horizontal = set()

for h in holes:
    if (h[0] - 1, h[1]) in track and (h[0] + 1, h[1]) in track:
        valid_holes_vertical.add(h)

    if (h[0], h[1] - 1) in track and (h[0], h[1] + 1) in track:
        valid_holes_horizontal.add(h)

valid_holes_union = valid_holes_vertical | valid_holes_horizontal

print(f'track length: {len(track)}')
print(f'valid holes vertical: {len(valid_holes_vertical)}')
print(f'valid holes horizontal: {len(valid_holes_horizontal)}')
print(f'valid holes union: {len(valid_holes_union)}')
print(f'valid holes sum: {len(valid_holes_horizontal) + len(valid_holes_vertical)}')

saves = []

for i, h in enumerate(valid_holes_horizontal):
    pos_1 = track_d[(h[0], h[1] - 1)]
    pos_2 = track_d[(h[0], h[1] + 1)]
    if pos_1 < pos_2:
        diff = pos_2 - pos_1
    else:
        diff = pos_1 - pos_2
    saves.append(diff - 2)

for i, h in enumerate(valid_holes_vertical):
    pos_1 = track_d[(h[0] - 1, h[1])]
    pos_2 = track_d[(h[0] + 1, h[1])]
    if pos_1 < pos_2:
        diff = pos_2 - pos_1
    else:
        diff = pos_1 - pos_2
    saves.append(diff - 2)

save_dict = {}
for s in saves:
    if s not in save_dict.keys():
        save_dict[s] = 1
    else:
        save_dict[s] = save_dict[s] + 1


le_total = 0
for k in save_dict.keys():
    if k >= 100:
        le_total = le_total + save_dict[k]

print(f'total: {le_total}')
