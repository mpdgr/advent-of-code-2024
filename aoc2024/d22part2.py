inputs = [s.strip() for s in open('day22.txt', 'r').readlines()]


def derive(n):
    n = (n << 6 ^ n) & 0xFFFFFF
    n = (n >> 5 ^ n) & 0xFFFFFF
    return (n << 11 ^ n) & 0xFFFFFF


def derive_times(n, times):
    prices = [n % 10]
    for t in range(0, times):
        n = derive(n)
        prices.append(n % 10)
    return prices


# for each input stores all first occurrences of subsequence and matching price
# key - input nr
# value - dict (subsequence - matching price)
inp_dict = dict()


# if seq didnt occur yet for given line it will be added, otherwise will be ignored
def add_subseq(subseq, price, line_nr):
    if line_nr not in inp_dict:
        line_dict = dict()
        line_dict[subseq] = price
        inp_dict[line_nr] = line_dict
    else:
        if subseq not in inp_dict[line_nr]:
            inp_dict[line_nr][subseq] = price


# check all diff subsequences in sequence
# for first occurrence of the subsequence save subsequence and matching price
def extract_subsequences(line, line_nr):
    for i in range(1, len(line) - 3):
        subseq = []
        for j in range(4):
            subseq.append(line[i + j] - line[i + j - 1])
        price = line[i + 3]
        add_subseq(tuple(subseq), price, line_nr)


# map all subsequence dictionary to total score for each subsequence
# (find all subsequence occurrences and add their prices)
def get_totals_for_subseqs(inp_dict):
    subseq_totals = dict()
    for line_nr, line_dict in inp_dict.items():
        for subseq, price in line_dict.items():
            if subseq in subseq_totals:
                subseq_totals[subseq] = subseq_totals[subseq] + price
            else:
                subseq_totals[subseq] = price
    return subseq_totals


# highest total for subsequence is the max amount to find
def get_highest_val(dict):
    max = 0
    for v in dict.values():
        if v > max:
            max = v
    return max


# create price sequence for each line
seq = []

for i in inputs:
    seq.append(derive_times(int(i), 2000))

# for each sequence parse subsequences and add them to subseq dictionary
for i, v in enumerate(seq):
    extract_subsequences(v, i)
subseq_totals = get_totals_for_subseqs(inp_dict)
das_total = get_highest_val(subseq_totals)

print(f'total: {das_total}')