lines = [l.split('   ') for l in open('day1.txt', 'r')]

v1 = sorted([int(s[0]) for s in lines])
v2 = sorted([int(s[1]) for s in lines])

diff_sum = 0
for i in range(0, len(v1)):
    diff_sum += abs(v1[i] - v2[i])

print(diff_sum)
