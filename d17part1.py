reg_A = 41644071
reg_B = 0
reg_C = 0

prog = [2, 4, 1, 2, 7, 5, 1, 7, 4, 4, 0, 3, 5, 5, 3, 0]

instr_ptr = 0
output = []


def get_literal(operand):
    return operand


def get_combo(operand):
    if operand == 0:
        return 0
    elif operand == 1:
        return 1
    elif operand == 2:
        return 2
    elif operand == 3:
        return 3
    elif operand == 4:
        return reg_A
    elif operand == 5:
        return reg_B
    elif operand == 6:
        return reg_C
    elif operand == 7:
        return 'x'


def pointer_jump():
    global instr_ptr
    instr_ptr = instr_ptr + 2


def adv(operand):
    global reg_A
    reg_A = reg_A >> get_combo(operand)
    pointer_jump()
    return None


def bxl(operand):
    global reg_B
    reg_B = reg_B ^ get_literal(operand)
    pointer_jump()
    return None


def bst(operand):
    global reg_B
    reg_B = get_combo(operand) % 8
    pointer_jump()
    return None


def jnz(operand):
    global reg_A
    global instr_ptr
    if reg_A == 0:
        pointer_jump()
    else:
        instr_ptr = get_literal(operand)
    return None


def bxc(operand):
    global reg_B
    global reg_C
    reg_B = reg_B ^ reg_C
    pointer_jump()
    return None


def out(operand):
    output = get_combo(operand) % 8
    pointer_jump()
    return output


def bdv(operand):
    global reg_A
    global reg_B
    reg_B = reg_A >> get_combo(operand)
    pointer_jump()
    return None


def cdv(operand):
    global reg_A
    global reg_C
    reg_C = reg_A >> get_combo(operand)
    pointer_jump()
    return None


def get_function(opcode):
    if opcode == 0:
        return adv
    elif opcode == 1:
        return bxl
    elif opcode == 2:
        return bst
    elif opcode == 3:
        return jnz
    elif opcode == 4:
        return bxc
    elif opcode == 5:
        return out
    elif opcode == 6:
        return bdv
    elif opcode == 7:
        return cdv


def read_next():
    global prog
    global instr_ptr
    global output
    if instr_ptr > len(prog) - 1:
        return None
    opcode = prog[instr_ptr]
    operand = prog[instr_ptr + 1]
    function = get_function(opcode)
    out = function(operand)
    if out is not None:
        output.append(out)
    return 0


def read():
    while read_next() is not None:
        read()


read()

print(f'output: {output}')
for o in output:
    print(o, end=',')





