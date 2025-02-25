with open('day3.txt', 'r') as file:
    lines = file.readlines()

total = 0

dos = []
pairs = []

# remove invalid instructions
donts = ''.join(lines).split("don't()")
dos.append(donts[0])
for dont in donts[1:]:
    if "do()" in dont:
        for i in dont.split("do()")[1:]:
            dos.append(i)

# parse valid instructions
for s in ''.join(dos).split("mul"):
    if s.startswith("("):
        pairs.append(s.removeprefix("(").split(")")[0])

for p in pairs:
    if "," in p:
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
