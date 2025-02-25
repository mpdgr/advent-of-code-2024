lines = [l.strip().split(" ") for l in open('day2.txt', 'r')]

valid = 0

for l in lines:
    sign = int(l[1]) - int(l[0])
    v = True
    for i in range(1, len(l)):
        diff = int(l[i]) - int(l[i - 1])
        if int(diff) * sign < 0:
            v = False
            break
        if int(diff == 0 or diff < - 3 or diff > 3):
            v = False
            break
    if v:
        valid += 1

print(f"Valid: {valid}")
