import re

lines = [l for l in open('day13.txt', 'r').readlines()]
n_cost, k_cost = 3, 1
inputs = []


# in: (x1, y1, x2, y2, xt, yt)
# coeff: (n, k)
def coeff(input):
    x1, y1, x2, y2, xt, yt = input[0], input[1], input[2], input[3], input[4], input[5]
    k = (x1 * yt - xt * y1) / (x1 * y2 - x2 * y1)
    n = (xt - k * x2) / x1
    return n, k


for i, line in enumerate(lines):
    if i % 4 == 0:
        inp = ()
        for j in range(0, 3):
            nrs = re.findall(r'\d+', lines[i + j])
            inp += int(nrs[0]), int(nrs[1])
        inputs.append(inp)

das_total = 0
for i in inputs:
    r = coeff(i)
    if r[0] % 1 == 0 and r[1] % 1 == 0:
        das_total += r[0] * n_cost + r[1] * k_cost
print(f'Total: {das_total}')
