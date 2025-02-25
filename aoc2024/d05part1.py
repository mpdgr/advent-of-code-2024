lines = [s.strip() for s in open('day5.txt', 'r').readlines()]

# create rules and reports
rules = set()
reports = list()
rules_map = dict()
total = 0

for l in lines:
    if '|' in l:
        rules.add((int(l.split('|')[0].strip()), int(l.split('|')[1].strip())))
    elif l.strip() != "":
        r = [int(s.strip()) for s in l.split(',')]
        reports.append(r)

# map of the numbers illegal after a given number
for (b, a) in rules:
    if a not in rules_map:
        rules_map[a] = set()
    rules_map[a].add(b)

# go through the reports - for each number save numbers illegal after
# for each number check if it is in a list of the illegal numbers
for report in reports:
    illegal = set()
    for n in report:
        if n in illegal:
            break
        if n in rules_map:
            illegal.update(rules_map.get(n))
    else:
        total += report[int(len(report) / 2)]

print(f"Total: {total}")
