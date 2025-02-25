inputs = [s.strip() for s in open('day22.txt', 'r').readlines()]


def derive(n):
    n = (n << 6 ^ n) & 0xFFFFFF
    n = (n >> 5 ^ n) & 0xFFFFFF
    return (n << 11 ^ n) & 0xFFFFFF


def derive_times(n, times):
    for t in range(0, times):
        n = derive(n)
    return n


total = 0
for i in inputs:
    total += derive_times(int(i), 2000)

print(f'total: {total}')
