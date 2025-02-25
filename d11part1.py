line = [int(s) for s in open('day11.txt', 'r').readlines()[0].strip().split(' ')]


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


def blink_times(line, times):
    for i in range(0, times):
        line = blink(line)
    return line


res = blink_times(line, 25)
set_res = (set(res))
print(len(res))
