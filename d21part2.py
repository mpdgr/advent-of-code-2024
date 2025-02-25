inputs = [s.strip() for s in open('day21.txt', 'r').readlines()]


class NumericIn:
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    #     | 0 | A |
    #     +---+---+

    def __init__(self, operator):
        self.operator = operator

    right, left, up, down = '>', '<', '^', 'v'
    locs = {
        'A': (3, 2),
        '0': (3, 1),
        '1': (2, 0),
        '2': (2, 1),
        '3': (2, 2),
        '4': (1, 0),
        '5': (1, 1),
        '6': (1, 2),
        '7': (0, 0),
        '8': (0, 1),
        '9': (0, 2),
    }
    left_col = {'7', '4', '1'}
    bottom_row = {'0', 'A'}

    # current arm position
    state = 'A'
    # operator of this pad
    operator = None

    def request_sequence(self, seq):
        end_sequences = 0
        for c in seq:
            operator_sequence = self.request_push(c)
            end_sequences = end_sequences + operator_sequence
        return end_sequences

    def request_push(self, btn):
        valid_sequences = self.__find_sequences(btn)
        operator_sequence = self.operator.request_sequence(valid_sequences)
        self.state = btn
        return operator_sequence

    def __find_sequences(self, target):
        source = self.state
        loc_source = NumericIn.locs[source]
        loc_target = NumericIn.locs[target]

        dist_h = loc_target[1] - loc_source[1]
        dist_v = loc_target[0] - loc_source[0]
        # path 1
        p1 = ''
        if dist_h > 0:
            p1 += NumericIn.right * dist_h
        if dist_h < 0:
            p1 += NumericIn.left * (dist_h * -1)
        if dist_v > 0:
            p1 += NumericIn.down * dist_v
        if dist_v < 0:
            p1 += NumericIn.up * (dist_v * -1)
        p2 = ''
        if dist_v > 0:
            p2 += NumericIn.down * dist_v
        if dist_v < 0:
            p2 += NumericIn.up * (dist_v * -1)
        if dist_h > 0:
            p2 += NumericIn.right * dist_h
        if dist_h < 0:
            p2 += NumericIn.left * (dist_h * -1)

        sequences = []
        if source in NumericIn.left_col and target in NumericIn.bottom_row:
            sequences.append(p1)
        elif source in NumericIn.bottom_row and target in NumericIn.left_col:
            sequences.append(p2)
        elif p1 != p2:
            sequences.append(p1)
            sequences.append(p2)
        else:
            sequences.append(p1)

        return sequences


class DirectionalIn:
    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+

    def __init__(self, operator):
        self.operator = operator

    right, left, up, down = '>', '<', '^', 'v'
    locs = {
        '>': (1, 2),
        '<': (1, 0),
        '^': (0, 1),
        'v': (1, 1),
        'A': (0, 2),
    }
    left_col = {'<'}

    # current arm position
    state = 'A'
    # operator of this pad
    operator = None

    def request_sequence(self, possible_paths):
        # parent requested to proceed with one of the two valid paths
        # examine both and choose shorter
        shortest_seq = -1
        for p in possible_paths:
            path = p + 'A'
            # now compute possible paths to get this parent request
            end_sequence = 0
            for c in path:
                operator_sequence = self.request_push(c)
                end_sequence = end_sequence + operator_sequence
            if shortest_seq == -1 or end_sequence < shortest_seq:
                shortest_seq = end_sequence
        return shortest_seq

    def request_push(self, btn):
        valid_sequences = self._find_sequences(btn)
        if self.operator is not None:
            operator_sequence = self.operator.request_sequence(valid_sequences)
            self.state = btn
            return operator_sequence
        else:
            return 1

    def _find_sequences(self, target):
        source = self.state
        loc_source = DirectionalIn.locs[source]
        loc_target = DirectionalIn.locs[target]

        dist_h = loc_target[1] - loc_source[1]
        dist_v = loc_target[0] - loc_source[0]
        p1 = ''
        if dist_h > 0:
            p1 += DirectionalIn.right * dist_h
        if dist_h < 0:
            p1 += DirectionalIn.left * (dist_h * -1)
        if dist_v > 0:
            p1 += DirectionalIn.down * dist_v
        if dist_v < 0:
            p1 += DirectionalIn.up * (dist_v * -1)
        p2 = ''
        if dist_v > 0:
            p2 += DirectionalIn.down * dist_v
        if dist_v < 0:
            p2 += DirectionalIn.up * (dist_v * -1)
        if dist_h > 0:
            p2 += DirectionalIn.right * dist_h
        if dist_h < 0:
            p2 += DirectionalIn.left * (dist_h * -1)

        sequences = []
        if source in DirectionalIn.left_col:
            sequences.append(p1)
        elif target in DirectionalIn.left_col:
            sequences.append(p2)
        elif p1 != p2:
            sequences.append(p1)
            sequences.append(p2)
        else:
            sequences.append(p1)

        return sequences


class DirectionalInCacheable(DirectionalIn):

    def __init__(self, operator, relay=False):
        super().__init__(operator)
        self.relay = relay

    relay = False
    cache = dict()

    def request_sequence(self, possible_paths):
        # check cache
        k = tuple(possible_paths)
        if self.relay and k in self.cache:
            return self.cache[k]

        # parent requested to proceed with one of the two valid paths
        # examine both and choose the shorter
        sequences = []
        for p in possible_paths:
            path = p + 'A'
            # now compute possible paths to get this parent request
            end_sequence = []
            for c in path:
                operator_sequence = self.request_push(c)
                end_sequence = end_sequence + operator_sequence
            sequences.append(end_sequence)
        shortest = sequences[0]
        for s in sequences:
            if len(s) < len(shortest):
                shortest = s

        # update cache
        if self.relay and k not in self.cache:
            v = len(shortest)
            self.cache[k] = v

        # relay passes only length of the sequence
        if self.relay:
            return len(shortest)
        # non-relay passes whole sequence
        else:
            return shortest

    def request_push(self, btn):
        valid_sequences = self._find_sequences(btn)
        if self.operator is not None:
            operator_sequence = self.operator.request_sequence(valid_sequences)
            self.state = btn
            return operator_sequence
        else:
            return [btn]


def run(inp):
    d01 = DirectionalInCacheable(None)
    d02 = DirectionalInCacheable(d01)
    d03 = DirectionalInCacheable(d02)
    d04 = DirectionalInCacheable(d03)
    d05 = DirectionalInCacheable(d04)
    d06 = DirectionalInCacheable(d05)
    d07 = DirectionalInCacheable(d06)
    d08 = DirectionalInCacheable(d07)
    d09 = DirectionalInCacheable(d08)
    d10 = DirectionalInCacheable(d09)
    d11 = DirectionalInCacheable(d10)
    d12 = DirectionalInCacheable(d11)
    d13 = DirectionalInCacheable(d12, True)
    d14 = DirectionalIn(d13)
    d15 = DirectionalIn(d14)
    d16 = DirectionalIn(d15)
    d17 = DirectionalIn(d16)
    d18 = DirectionalIn(d17)
    d19 = DirectionalIn(d18)
    d20 = DirectionalIn(d19)
    d21 = DirectionalIn(d20)
    d22 = DirectionalIn(d21)
    d23 = DirectionalIn(d22)
    d24 = DirectionalIn(d23)
    d25 = DirectionalIn(d24)
    d26 = DirectionalIn(d25)
    d_n = NumericIn(d26)

    result_sequence = d_n.request_sequence(inp)

    numeric_part = inp[:3]
    numeric_part_n = int(numeric_part)
    print(f'numeric part: {numeric_part}, seq length: {result_sequence}')

    res = numeric_part_n * result_sequence
    return res


total = 0
for inp in inputs:
    total += run(inp)

print(f'total: {total}')
