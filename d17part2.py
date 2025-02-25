reg_A = 0
reg_B = 0
reg_C = 0

prog = [2, 4, 1, 2, 7, 5, 1, 7, 4, 4, 0, 3, 5, 5, 3, 0]
output = []


def compiled():
    global reg_A
    global reg_B
    global output
    reg_B = reg_A % 8 ^ (reg_A >> (reg_A % 8 ^ 2) ^ 5)
    reg_A = reg_A >> 3
    o = reg_B % 8
    output.append(o)
    if reg_A == 0:
        return
    else:
        compiled()


# load candidates matrix
candidates = []
candidates_pointers = []
for i in range(0, 16):
    candidates.append([0, 1, 2, 3, 4, 5, 6, 7])
    candidates_pointers.append(0)


pos = 15
cand_count = 8
current_reg_A = 0

# backtracking
while output != prog:
    # try to pick a candidate
    cand_pointer = candidates_pointers[pos]
    if cand_pointer < cand_count:  # ok we're still in range
        cand = candidates[pos][cand_pointer]
        # lets append our candidate to current_reg_A
        # make space for value
        current_reg_A = current_reg_A << 3
        # add the value
        current_reg_A = current_reg_A | cand
        # now try to run the program and see the output
        output = []
        reg_A = current_reg_A
        compiled()
        print(f"Current reg A: {current_reg_A}")
        # compare the output with expected array
        out_size = len(output)
        all_val_match = True
        for i in range(1, out_size + 1):
            out_val = output[-i]
            exp_val = prog[-i]
            # if any of the values doesn't fit
            if out_val != exp_val:
                all_val_match = False
        if not all_val_match:
            # clear current reg_A of the added value
            current_reg_A = current_reg_A >> 3
            # move the pointer further
            candidates_pointers[pos] = cand_pointer + 1
        # we found a matching number! lets move to the next list of candidates
        # but first update the pointer in case we come back here
        else:
            candidates_pointers[pos] = cand_pointer + 1
            pos = pos - 1
    # we are out of candidates, we have to backtrack
    else:
        # lets remove last value from the end of current_reg_A
        current_reg_A = current_reg_A >> 3
        # lets reset the current pointer
        candidates_pointers[pos] = 0
        # and update the processed line nr
        pos = pos + 1
