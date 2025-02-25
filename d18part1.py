import heapq

invalids = [(int(s.split(',')[0]), int(s.split(',')[1].strip())) for s in open('day18.txt', 'r').readlines()][:1024]
low = 0
high = 70
inf = 1_000_000

inv = set(invalids)
resolved = set()
adj_matrix = {}
resolve_queue = []

# (dist from start, from pointer)
vertice_state = {}

start = (0, 0)
end = (high, high)


def find_neighbors(x, y):
    if x < high and (x + 1, y) not in inv:
        adj_matrix[x, y].append((x + 1, y))
    if x > low and (x - 1, y) not in inv:
        adj_matrix[x, y].append((x - 1, y))
    if y < high and (x, y + 1) not in inv:
        adj_matrix[x, y].append((x, y + 1))
    if y > low and (x, y - 1) not in inv:
        adj_matrix[x, y].append((x, y - 1))


for y in range(low, high + 1):
    for x in range(low, high + 1):
        if (x, y) not in inv:
            adj_matrix[(x, y)] = []
            find_neighbors(x, y)


for v in adj_matrix.keys():
    vertice_state[v] = (inf, None)


vertice_state[start] = (0, None)

for v, s in adj_matrix.items():
    heapq.heappush(resolve_queue, (vertice_state[v][0], v))

total_dist = -1

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

print(f'total: {total_dist}')

