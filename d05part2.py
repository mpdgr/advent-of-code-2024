reports = list()
invalid = list()
rules = set()
rules_map = dict()                                          # value = set of values illegal after a given value/key
total = 0

for l in [s for s in open('day5.txt', 'r').readlines()]:    # parse rules and reports
    if '|' in l:
        rules.add((int(l.split('|')[0]), int(l.split('|')[1])))
    elif l.strip() != "":
        reports.append([int(s) for s in l.split(',')])

for (b, a) in rules:
    if a not in rules_map:
        rules_map[a] = set()
    rules_map[a].add(b)


def valid(r):
    illegal_n = set()                                       # all numbers illegal at given point
    for i, v in enumerate(r):
        if v in illegal_n:
            return i
        if v in rules_map:
            illegal_n.update(rules_map.get(v))              # save all numbers illegal after currently processed
    return -1


for r in reports:                                           # first run only identifies invalid reports
    if valid(r) != -1:
        invalid.append(r)

while invalid:                                              # process until all reports are reordered.
    for r in invalid:                                       # will run forever if rules are contradictory
        i = valid(r)
        if i == -1:
            invalid.remove(r)
            total += r[int(len(r) / 2)]
        else:
            r[i - 1], r[i] = r[i], r[i - 1]                 # if invalid swapped first illegal value with previous

print(f"Total corrected: {total}")
