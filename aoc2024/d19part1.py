all_lines = [l for l in open('day19.txt', 'r').readlines()]

available = [p.strip().removesuffix(',') for p in all_lines[0].strip().split()]
required = [p.strip() for p in all_lines[2:]]

av = set(available)
memo_valid = set()
memo_invalid = set()


def sequence_valid(pattern: str):
    if len(pattern) == 0 or pattern in memo_valid:
        return True
    if pattern in memo_invalid:
        return False
    any_sub_valid = False
    for i in range(1, len(pattern) + 1):
        start_seq = pattern[:i]
        if start_seq in av:
            sub = sequence_valid(pattern[i:])
            if sub:
                any_sub_valid = True
                memo_valid.add(pattern[i:])
            else:
                memo_invalid.add(pattern[i:])
    return any_sub_valid


total = 0
for p in required:
    v = sequence_valid(p)
    if v:
        total += 1

print(f'total: {total}')
