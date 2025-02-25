m = [s.strip() for s in open('day4.txt', 'r').readlines()]
t = 0
for r in range(1, len(m) - 1):
    for c in range(1, len(list(m[r])) - 1):
        if m[r][c] == 'A' and {m[r - 1][c - 1], m[r + 1][c + 1]} == {m[r - 1][c + 1], m[r + 1][c - 1]} == {'M', 'S'}:
            t += 1
print(f"Total: {t}")
