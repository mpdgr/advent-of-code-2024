inputs = [s.strip() for s in open('day25.txt', 'r').readlines()]

keys, locks = [], []


def add_line(line, arr):
    for i, v in enumerate(line):
        if v == '#':
            arr[i] += 1


for i in range(0, len(inputs), 8):
    arr = [0] * 7
    for j in range(7):
        add_line(inputs[i + j], arr)
    if inputs[i] == '.....':
        keys.append(arr)
    else:
        locks.append(arr)

total = 0
for k in keys:
    for l in locks:
        if max([i + j for i, j in zip(k, l)]) <= 7:
            total += 1

print(total)
