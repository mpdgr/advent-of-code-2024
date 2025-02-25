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

    operator = None

    def request_sequence(self, seq):
        end_sequences = []
        for c in seq:
            operator_sequence = self.request_push(c)
            end_sequences = end_sequences + operator_sequence
        return end_sequences

    def request_push(self, btn):
        valid_sequences = self.__find_sequences(self.state, btn)
        operator_sequence = self.operator.request_sequence(valid_sequences)
        self.state = btn
        return operator_sequence

    def __find_sequences(self, source, target):
        source = self.state
        loc_source = NumericIn.locs[source]
        loc_target = NumericIn.locs[target]

        dist_h = loc_target[1] - loc_source[1]
        dist_v = loc_target[0] - loc_source[0]
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

    operator = None

    def request_sequence(self, possible_paths):
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
        # choose shortest seq
        shortest = sequences[0]
        for s in sequences:
            if len(s) < len(shortest):
                shortest = s
        return shortest

    def request_push(self, btn):
        valid_sequences = self.__find_sequences(self.state, btn)
        if self.operator is not None:
            operator_sequence = self.operator.request_sequence(valid_sequences)
            self.state = btn
            return operator_sequence
        else:
            return [btn]

    def __find_sequences(self, source, target):
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


def run(inp):
    first_pad = DirectionalIn(None)
    second_pad = DirectionalIn(first_pad)
    third_pad = DirectionalIn(second_pad)
    numeric_pad = NumericIn(third_pad)

    result_sequence = numeric_pad.request_sequence(inp)

    numeric_part_n = int(inp[:3])
    res = numeric_part_n * len(result_sequence)
    return res


total = 0
for inp in inputs:
    total += run(inp)

print(total)
