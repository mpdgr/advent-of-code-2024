# load lines
line = [int(s) for s in open('day11.txt', 'r').readlines()[0].strip().split(' ')]

run_size = 25
buffer_size = 500

# cache for full result after run
cache = {}
# cache for result size after run
cache_len = {}


def blink_times(value, times):
    line = [value]
    for i in range(0, times):
        line = blink(line)
    return line


def blink(line):
    res_line = []
    for item in line:
        if item == 0:
            res_line.append(1)
        elif len(str(item)) % 2 == 0:
            size_new = int(len(str(item)) / 2)
            it_1 = str(item)[:size_new]
            it_2 = str(item)[size_new:]
            res_line.append(int(it_1))
            res_line.append(int(it_2))
        else:
            res_line.append(item * 2024)
    return res_line


def blink_item(item, times):
    if item in cache.keys():
        return cache[item]
    res_line = blink_times(item, times)
    cache[item] = res_line
    cache_len[item] = len(res_line)
    return res_line


def blink_item_for_length(item, times):
    if item in cache_len.keys():
        return cache_len[item]
    res_line = blink_times(item, times)
    cache[item] = res_line
    cache_len[item] = len(res_line)
    return len(res_line)

# ---> first run:
result = []
for item in line:
    blinked = blink_item(item, run_size)
    result.extend(blinked)

print(f"Total 1st run: {len(result)}")
print(f"Cache length: {len(cache.keys())}")

# ---> prepare second run:
# unique results from first run
unique = set(result)
# fill cache with first run unique scores
counter = 1
for u in unique:
    blink_item(u, run_size)
    counter += 1
print(f"Total unique in second run: {len(unique)}")
print(f"Total cache size after first run: {len(cache.keys())}")


# --->  run third run in batches:
def third_run(l):
    total = 0
    for i in l:
        result = blink_item_for_length(i, run_size)
        total += result
    return total


# --->  run second run:
# ***this takes a while!***
result_2_buffer = []
run_1_size = len(result)
score = 0
for i, item in enumerate(result):
    # process by batch
    if i % buffer_size == 0:
        # do a third run for lines in buffer
        third_run_l = third_run(result_2_buffer)
        score = score + third_run_l
        result_2_buffer = []
        print(f"Adding to total, processed = {i}")
        print(f"- score so far = {score}")
    blinked = blink_item(item, run_size)
    result_2_buffer.extend(blinked)
# do the third run for last not filled batch
third_run_l = third_run(result_2_buffer)
score += third_run_l

print(f"Total 3nd run: {score}")