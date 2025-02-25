lines = [s for s in open('day7.txt', 'r').readlines()]
in_v = []

valids_list = list()
valids_set = set()

valid_total = 0

for l in lines:
    s = l.split(':')
    in_v.append((int(s[0]), [int(n) for n in s[1].strip().split()]))


def score(sc, depth, max_depth, arr, target):
    if sc == target and depth == max_depth:
        return True
    elif depth == max_depth:
        return False
    elif sc > target:
        return False
    return score(sc + arr[depth + 1], depth + 1, max_depth, arr, target) \
        or score(sc * arr[depth + 1], depth + 1, max_depth, arr, target)


def comp_for_inv(t):
    target = t[0]
    arr = t[1]
    max_depth = len(t[1]) - 1
    return score(arr[0], 0, max_depth, arr, target)


for v in in_v:
    if comp_for_inv(v):
        valid_total += v[0]
        valids_set.add(v[0])
        valids_list.append(v[0])

print(f'Total: {valid_total}')
