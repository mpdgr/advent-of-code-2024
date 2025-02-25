from collections import deque

lines = [s.strip() for s in open('day9.txt', 'r').readlines()]
record = lines[0]
result = []
queue = deque()

for c in record:
    queue.append(int(c))

to_move = deque()
total_length = 0
current_id = 0

while queue:
    file_length = queue.popleft()

    for i in range(0, file_length):
        result.append(current_id)
        to_move.append(current_id)
    total_length += file_length
    current_id += 1

    if queue:
        empty_spaces = queue.popleft()
        for j in range(0, empty_spaces):
            result.append(-1)

for i in range(0, total_length):
    if result[i] == -1:
        result[i] = str(to_move.pop())

first_free = int(record[0])
result_l = list(result)

total = 0
for i in range(0, total_length):
    total += i * int(result_l[i])
    if result_l[i] == '.':
        result_l[i] = str(to_move.pop())

print(f'total score: {total}')

