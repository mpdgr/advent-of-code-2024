all_lines = [l for l in open('day19.txt', 'r').readlines()]

available = [p.strip().removesuffix(',') for p in all_lines[0].strip().split()]
required = [p.strip() for p in all_lines[2:]]

av = set(available)
patterns_possible = set()
memo_valid = set()
memo_invalid = set()

counter = 0


def sequence_valid(pattern: str):
    global counter
    if len(pattern) == 0:
        counter = counter + 1
        return True
    if pattern in memo_valid:
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
        memo_valid.add(p)
        patterns_possible.add(p)
        total = total + 1

longest_pattern = 0
for p in av:
    if len(p) > longest_pattern:
        longest_pattern = len(p)


def sequence_comb(pattern: str, pattern_using):
    sequence_cache = {}
    processed = ''
    sequence_cache[processed] = 0
    for c in pattern:
        all_count = 0
        if len(processed) == 0:
            processed = c
            if c in pattern_using:
                sequence_cache[processed] = 1
            else:
                sequence_cache[processed] = 0
            continue
        if c in pattern_using:
            all_count = sequence_cache[processed]
        in_process = processed + c
        # we'll look for patterns in up to last n=longest_pattern chars of processed char
        length_to_look_back = longest_pattern if len(processed) >= longest_pattern else len(in_process)
        for i in range(2, length_to_look_back + 1):
            # check if element is in a set off all elements present in the pattern
            check_element = in_process[-i:]
            remain = in_process[0:-i]
            # remain part must be in solved already, otherwise this combination is not possible
            if check_element in pattern_using and remain in sequence_cache.keys():
                remain_comb = sequence_cache[remain]
                if remain_comb == 0 and len(remain) != 0:
                    continue
                if remain_comb == 0:
                    all_count = all_count + 1
                    continue
                all_count = all_count + remain_comb
        processed = in_process
        sequence_cache[in_process] = all_count
    return sequence_cache[processed]


def combinations_count(pattern: str):
    # set of used patterns
    pattern_using = set()
    for p in av:
        if p in pattern:
            pattern_using.add(p)
    return sequence_comb(pattern, pattern_using)


all_counter = 0
for p in patterns_possible:
    all_counter += combinations_count(p)

print(f'all combinations count: {all_counter}')
