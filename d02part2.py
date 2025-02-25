lines = [l.strip().split(" ") for l in open('day2.txt', 'r')]


def valid(l):
    sign = int(l[1]) - int(l[0])
    sc = -1

    for i in range(1, len(l)):
        diff = int(l[i]) - int(l[i - 1])
        if int(diff) * sign < 0:
            sc = i
            break
        if int(diff == 0 or diff < - 3 or diff > 3):
            sc = i
            break
    return sc


valid_count = 0

for l in lines:
    score = valid(l)
    if score == -1:
        valid_count = valid_count + 1
        continue
    for i in range(0, 3):
        lm = l[:score - i] + l[score - i + 1:]
        scorem = valid(lm)
        if scorem == -1:
            valid_count += 1
            break

print(f"Valid: {valid_count}")
