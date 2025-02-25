lns = [s for s in open('day7.txt', 'r').readlines()]
in_v = [(int(l.split(':')[0]), [int(n) for n in l.split(':')[1].strip().split()]) for l in lns]
v_t = 0


def v(r, t):
    return r[0] == t if len(r) == 1 else r[0] < t and v([r[0] + r[1]] + r[2:], t)\
        or v([r[0] * r[1]] + r[2:], t) or v([int(str(r[0]) + str(r[1]))] + r[2:], t)


for i in in_v:
    v_t = v_t + i[0] if v(i[1], i[0]) else v_t
print(f'Total: {v_t}')
