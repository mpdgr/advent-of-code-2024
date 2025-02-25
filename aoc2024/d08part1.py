matrix = [s.strip() for s in open('day8.txt', 'r').readlines()]      # create matrix

# find broadcasters
broadcasters = dict()
for r, line in enumerate(matrix):
    for c, char in enumerate(list(line)):
        if char != '.':
            if char not in broadcasters:
                broadcasters[char] = []
            broadcasters[char].append((r, c))

all_pairs = set()
all_c_peers = set()


def find_counter_peers(smaller, larger):
    # smaller peer coords
    # (r1c1)(r2c2)
    r_3 = smaller[0] - (larger[0] - smaller[0])
    c_3 = smaller[1] - (larger[1] - smaller[1])
    # larger peer coords
    r_4 = larger[0] + (larger[0] - smaller[0])
    c_4 = larger[1] + (larger[1] - smaller[1])
    return r_3, c_3, r_4, c_4


def validate_counter_peers(quadruple):
    left_bound = 0
    up_bound = 0
    right_bound = len(matrix[0]) - 1
    down_bound = len(matrix) - 1
    s_valid = up_bound <= quadruple[0] <= down_bound and left_bound <= quadruple[1] <= right_bound
    l_valid = up_bound <= quadruple[2] <= down_bound and left_bound <= quadruple[3] <= right_bound
    if s_valid:
        all_c_peers.add((quadruple[0], quadruple[1]))
    if l_valid:
        all_c_peers.add((quadruple[2], quadruple[3]))


# find peers
for frequency in broadcasters.values():
    for i in range(len(frequency)):
        for j in range(i + 1, len(frequency)):
            all_pairs.add((frequency[i], frequency[j]))

# find valid counter peers
for p in all_pairs:
    quad = find_counter_peers(p[0], p[1])
    validate_counter_peers(quad)

print(len(all_c_peers))
