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

    def __init__(self, id):
        self.id = id
        self.outp = list()

    def trigger(self, source, signal: int):
        if source == self.inp1:
            self.__trigger_1(signal)
        elif source == self.inp2:
            self.__trigger_2(signal)
        else:
            raise ValueError(f'Invalid input!: {source}')

    def trigger_in(self, signal: int):  # only use for x and y inputs!
        for o in self.outp:
            o.trigger(self, signal)

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

    def __clear(self):
        self.inp1 = None
        self.inp2 = None

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


# run all input values into the system
def run():
    for i in inputs:
        v = values[i.id]
        i.trigger_in(v)


def print_out():
    for o in outputs:
        print(o.out_val, end='')


run()
print_out()
