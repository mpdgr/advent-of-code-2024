input = [s.strip() for s in open('day24.txt', 'r').readlines()]

# read values
values = dict()

ptr = 0
line = input[ptr]
while (line != ''):
    var = line[:3]
    val = line.split(' ')[1]
    values[var] = int(val)
    ptr += 1
    line = input[ptr]
ptr += 1

# read expressions
expressions = list()
while ptr < len(input):
    line = input[ptr]
    s = line.split(' ')
    var1 = s[0]
    func = s[1]
    var2 = s[2]
    outg = s[4]
    expressions.append((var1, func, var2, outg))
    ptr += 1


class LogicGate:
    id: str = None
    outp = None             # connected gates -> out
    inp1 = None             # connected gate -> in
    inp2 = None             # connected gate -> in
    in_val_1: int = None    # incoming value
    in_val_2: int = None    # incoming value
    out_val: int = None     # out value
    function = None
    activation_count = 0
    recursion_limit = 10

    def __init__(self, id):
        self.id = id
        self.outp = list()

    def trigger(self, source, signal: int):
        if source == self.inp1:
            self.__trigger_1(signal)
        elif source == self.inp2:
            self.__trigger_2(signal)
        else:
            raise ValueError(f'Invalid input!: {source.id}')

    def trigger_in(self, signal: int):  # only use for x and y inputs!
        for o in self.outp:
            o.trigger(self, signal)
        self.__clear()

    def __trigger_1(self, signal: int):
        if signal is None:
            raise ValueError(f'None signal')
        self.in_val_1 = signal
        if self.in_val_2 is not None:
            self.__activate()

    def __trigger_2(self, signal: int):
        if signal is None:
            raise ValueError(f'None signal')
        self.in_val_2 = signal
        if self.in_val_1 is not None:
            self.__activate()

    def __activate(self):
        result = self.function(self.in_val_1, self.in_val_2)
        self.out_val = result
        for o in self.outp:
            o.trigger(self, result)
        self.activation_count = self.activation_count + 1
        if self.activation_count > self.recursion_limit:
            raise RecursionError
        self.__clear()

    def __clear(self):
        self.in_val_1 = None
        self.in_val_2 = None

    def set_connection(self, inputs: tuple):
        self.inp1 = inputs[0]
        self.inp2 = inputs[1]
        gates[inputs[0].id].add_observable_gate(self)
        gates[inputs[1].id].add_observable_gate(self)

    def set_function(self, desc):
        if desc == 'AND':
            self.function = self.__and_gate
        elif desc == 'OR':
            self.function = self.__or_gate
        elif desc == 'XOR':
            self.function = self.__xor_gate
        else:
            raise ValueError(f'Invalid argument: {desc}')

    def add_observable_gate(self, observable):
        self.outp.append(observable)

    def __and_gate(self, a, b):
        return a & b

    def __or_gate(self, a, b):
        return a | b

    def __xor_gate(self, a, b):
        return a ^ b


# initialize all logic gates
gates = dict()
for e in expressions:
    gates[e[3]] = LogicGate(e[3])

# initialize all input points
inputs = []
for i in range(0, 45):
    nr = '0' + str(i) if i < 10 else str(i)
    x_gate = 'x' + nr
    gates[x_gate] = LogicGate(x_gate)
    inputs.append(gates[x_gate])

    nr = '0' + str(i) if i < 10 else str(i)
    y_gate = 'y' + nr
    gates[y_gate] = LogicGate(y_gate)
    inputs.append(gates[y_gate])

inputs = sorted(inputs, key=lambda o: o.id)

# initialize all output points
outputs = []
for g in gates.keys():
    if g[0] == 'z':
        outputs.append(gates[g])

outputs = sorted(outputs, key=lambda o: o.id, reverse=True)

# initialize all connections
for e in expressions:
    gate = gates[e[3]]
    gate.set_connection((gates[e[0]], gates[e[2]]))
    gate.set_function(e[1])


def get_output():
    out = list()
    for o in outputs:
        out.append(o.out_val)
    return out


def reset_recursion():
    for g in gates.values():
        g.activation_count = 0


def reset_gates():
    for g in gates.values():
        g.in_val_1 = None
        g.in_val_2 = None


def reset_output():
    for o in outputs:
        o.out_val = None


# run all input values into the system (part 1 input)
def run(x_list, y_list):
    for i in range(0, 45):
        inputs[i].trigger_in(x_list[i])
        inputs[i + 45].trigger_in(y_list[i])
    reset_recursion()
    reset_gates()
    return get_output()


def test_at_index(index):
    success = True
    # 0 + 0 = 0 -> 0
    x = [0] * 45
    y = [0] * 45
    z = [0] * 46
    score = run(x, y)
    if score != z:
        success = False

    # 0 + 1 = 1 -> 0
    x = [0] * 45
    y = [0] * 45
    y[index] = 1
    z = [0] * 46
    z[len(z) - 1 - index] = 1
    score = run(x, y)
    if score != z:
        success = False

    # 1 + 0 = 1 -> 0
    x = [0] * 45
    x[index] = 1
    y = [0] * 45
    z = [0] * 46
    z[len(z) - 1 - index] = 1
    score = run(x, y)
    if score != z:
        success = False

    # 1 + 1 = 0 -> 1
    x = [0] * 45
    x[index] = 1
    y = [0] * 45
    y[index] = 1
    z = [0] * 46
    z[len(z) - 1 - index - 1] = 1
    score = run(x, y)
    if score != z:
        success = False

    return success


def swap_inputs(id_1, id_2):
    g_1 = gates[id_1]
    g_2 = gates[id_2]

    # g1 inputs
    g_1_in1 = g_1.inp1
    g_1_in2 = g_1.inp2
    # g2 inputs
    g_2_in1 = g_2.inp1
    g_2_in2 = g_2.inp2

    # swap functions
    func1 = g_1.function
    func2 = g_2.function

    g_1.function = func2
    g_2.function = func1

    # clear observables
    if g_1.inp1 and g_1 in g_1.inp1.outp:
        g_1.inp1.outp.remove(g_1)
    if g_1.inp2 and g_1 in g_1.inp2.outp:
        g_1.inp2.outp.remove(g_1)
    if g_2.inp1 and g_2 in g_2.inp1.outp:
        g_2.inp1.outp.remove(g_2)
    if g_2.inp2 and g_2 in g_2.inp2.outp:
        g_2.inp2.outp.remove(g_2)

    # swap inputs
    g_1.inp1 = g_2_in1
    g_1.inp2 = g_2_in2

    g_2.inp1 = g_1_in1
    g_2.inp2 = g_1_in2

    # add outputs
    if g_1.inp1:
        g_1.inp1.outp.append(g_1)
    if g_1.inp2:
        g_1.inp2.outp.append(g_1)
    if g_2.inp1:
        g_2.inp1.outp.append(g_2)
    if g_2.inp2:
        g_2.inp2.outp.append(g_2)


def run_all():
    errors = set()
    for i in range(0, 45):
        try:
            success = test_at_index(i)
        except RecursionError:
            success = False
        if not success:
            errors.add(i)
        if len(errors) >= 7:
            break
    return errors


def swap_test(id_1, id_2):
    # swap before test
    swap_inputs(id_1, id_2)

    errors = run_all()

    # swap back after test
    swap_inputs(id_1, id_2)

    return errors


def swap_test_c(id_1, id_2, id_3, id_4, id_5, id_6, id_7, id_8):
    # swap before test
    swap_inputs(id_1, id_2)
    swap_inputs(id_3, id_4)
    swap_inputs(id_5, id_6)
    swap_inputs(id_7, id_8)

    errors = run_all()

    # swap back after test
    swap_inputs(id_1, id_2)
    swap_inputs(id_3, id_4)
    swap_inputs(id_5, id_6)
    swap_inputs(id_7, id_8)

    return errors


def swap_and_test(benchmark, ids):
    candidates = []
    for i in range(0, len(ids)):
        print(f'Swap testing gate: {i + 1} of {len(ids)}')
        for j in range(i + 1, len(ids)):
            errors_after_swap = swap_test(ids[i], ids[j])
            if len(errors_after_swap) < benchmark:
                candidates.append((ids[i], ids[j], len(errors_after_swap)))
    return candidates


# first run to determine nr of errors
err = run_all()

# find gates corresponding to errors
err_gates = list()
for e in err:
    err_gates.append(outputs[len(outputs) - e - 1])


# recursively get gates neighbours to find candidates for swap
def get_peers(gate: LogicGate, depth=0, max_depth=0):
    d = depth + 1
    peers = set()
    peers.add(gate)
    if gate.inp1:
        peers.add(gate.inp1)
    if gate.inp2:
        peers.add(gate.inp2)
    for g in gate.outp:
        peers.add(g)
    if d < max_depth:
        p_temp = set()
        for p in peers:
            further_peers = get_peers(p, d, max_depth)
            p_temp.update(further_peers)
        peers.update(p_temp)
    return peers


# find swap candidates
cand = set()
for e in err_gates:
    cand.update(get_peers(e, 0, 3))  # increase depth if result not found

err_gates_ids = {e.id for e in err_gates}
cand_ids = {e.id for e in cand - {None}}
cand_ids = {s for s in cand_ids if not s.startswith('x') and not s.startswith('y') and s in gates.keys()}

print(f'Invalid gates: {err_gates_ids}')
print(f'Invalid gates count: {len(err_gates)}')
print(f'Swap candidates count: {len(cand_ids)}')

# swap testing
candidates = swap_and_test(len(err), list(cand_ids))

min_err = 1000
tested = list()
zeros = list()

# test all possible combinations of 4 swaps of candidates
for s1 in candidates:
    for s2 in candidates:
        for s3 in candidates:
            for s4 in candidates:
                all = {s1, s2, s3, s4}
                all_ind = {s1[0], s2[0], s3[0], s4[0], s1[1], s2[1], s3[1], s4[1]}
                if len(all) == 4 and len(all_ind) == 8 and list(sorted(all_ind)) not in tested:
                    tested.append(list(sorted(all_ind)))
                    errors = swap_test_c(s1[0], s1[1], s2[0], s2[1], s3[0], s3[1], s4[0], s4[1])
                    if len(errors) == 0:
                        zeros.append(all)

print(f'Zero errors: {len(zeros)}')

for z in zeros:
    z_set = set()
    for e in z:
        z_set.update({e[0], e[1]})
    print(sorted(z_set))
