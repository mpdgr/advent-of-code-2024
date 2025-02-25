file = open('day3.txt', 'r')

pairs = []
total = 0
muls = 0
withcomma = 0

for l in file:
    for s in l.split("mul"):
        if s.startswith("("):
            muls += 1
            pairs.append(s.removeprefix("(").split(")")[0])

for p in pairs:
    if "," in p:
        withcomma += 1
        pair = p.split(",")
        if len(pair) != 2:
            continue
        try:
            v1 = int(pair[0])
            v2 = int(pair[1])
        except ValueError:
            continue
        total += v1 * v2

print(f"Total: {total}")
