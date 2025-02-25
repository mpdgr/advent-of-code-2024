from collections import deque

lines = [s.strip() for s in open('day9.txt', 'r').readlines()]
record = lines[0]
expanded = []

queue = deque()

for c in record:
    queue.append(int(c))

to_move = deque()
total_length = 0
file_id_length = dict()

current_id = 0

while queue:
    file_length = queue.popleft()
    for i in range(0, file_length):
        expanded.append(current_id)
        to_move.append(current_id)
        file_id_length[current_id] = file_length
    total_length += file_length
    current_id += 1

    if queue:
        empty_spaces = queue.popleft()
        for j in range(0, empty_spaces):
            expanded.append(-1)


ex_index = {}
for i, val in enumerate(expanded):
    if val not in ex_index.keys():
        ex_index[val] = i


def find_free_spots(expanded):
    empty_start = True
    processing_free_spot = False
    free_spots = []
    free_spots_pointer = 0
    for i in range(0, len(expanded)):
        if expanded[i] == -1 and empty_start:
            free_spots.append((i, 1))
            empty_start = False
            processing_free_spot = True
        elif expanded[i] == -1:
            spot_c = free_spots[len(free_spots) - 1]
            val = spot_c[1] + 1
            free_spots[len(free_spots) - 1] = (spot_c[0], val)
        elif expanded[i] != -1 and processing_free_spot:
            processing_free_spot = False
            empty_start = True
            free_spots_pointer += 1
    return free_spots


def fill_spot(free_spot, id, length):
    for i in range(free_spot[0], free_spot[0] + length):
        expanded[i] = id


def clear_source(val):
    for i, v in enumerate(expanded):
        if v == val:
            expanded[i] = -1


def get_key_index(val):
    return ex_index[val]


ids = sorted(list(file_id_length.keys()), reverse=True)
result_l = []
while ids:
    key = ids[0]
    free_spots = find_free_spots(expanded)
    for i, free_spot in enumerate(free_spots):
        if free_spot[1] >= file_id_length[key] and key != 0 and (get_key_index(key) > free_spot[0]):
            clear_source(key)
            fill_spot(free_spot, key, file_id_length[key])
            break
    del (ids[0])
    result_l = expanded

total = 0
for i in range(0, len(result_l)):
    if result_l[i] != -1:
        total += i * int(result_l[i])

print(f'Total: {total}')
