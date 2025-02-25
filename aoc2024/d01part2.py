lines = [l.split('   ') for l in open('day1.txt', 'r')]

v1 = [int(s[0]) for s in lines]
v2 = [int(s[1]) for s in lines]

sim_score = 0
for i in v1:
    sim_score += i * len([n for n in v2 if n == i])

print(sim_score)
