matrix = [s.strip() for s in open('day8.txt', 'r').readlines()]

up_bound = 0
right_bound = len(matrix[0]) - 1
down_bound = len(matrix) - 1
left_bound = 0
left_up = -1
right_down = 1

emitters = dict()
peers = set()
echos = set()

def find_echos(emitter, coemitter):
    v_dist = coemitter[0] - emitter[0]
    h_dist = coemitter[1] - emitter[1]
    search_ray(emitter, v_dist, h_dist, right_down)
    search_ray(coemitter, v_dist, h_dist, left_up)


def search_ray(loc, v_dist, h_dist, dir):
    row = loc[0] - v_dist * dir
    col = loc[1] - h_dist * dir
    v = True
    while v:
        if valid_pos(row, col):
            echos.add((row, col))
            row = row - v_dist * dir
            col = col - h_dist * dir
        else:
            v = False


def valid_pos(row, col):
    return up_bound <= row <= down_bound and left_bound <= col <= right_bound


# find all broadcasters
for r, line in enumerate(matrix):
    for c, char in enumerate(list(line)):
        if char != '.':
            if char not in emitters:
                emitters[char] = []
            emitters[char].append((r, c))

# find all pairs emitter - coemitter, add to echos
for frequency in emitters.values():
    for i in range(len(frequency)):
        for j in range(i + 1, len(frequency)):
            peers.add((frequency[i], frequency[j]))
            echos.update([frequency[i], frequency[j]])

# find echos for each pair
for p in peers:
    find_echos(p[0], p[1])
print(f'Total: {len(echos)}')
