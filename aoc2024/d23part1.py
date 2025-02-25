lines = [l.strip() for l in open('day23.txt', 'r').readlines()]

connections = set()

for l in lines:
    c1 = l.split('-')[0]
    c2 = l.split('-')[1]
    connections.add((c1, c2))

adj_matrix = {}

for c in connections:
    if c[0] not in adj_matrix:
        adj_matrix[c[0]] = [c[1]]
    else:
        adj_matrix[c[0]].append(c[1])
    if c[1] not in adj_matrix:
        adj_matrix[c[1]] = [c[0]]
    else:
        adj_matrix[c[1]].append(c[0])

# connected
connected = list()
for computer in adj_matrix:
    all_neighbors = adj_matrix[computer]
    for i in range(0, len(all_neighbors)):
        for j in range(i + 1, len(all_neighbors)):
            if all_neighbors[i] in adj_matrix[all_neighbors[j]]:
                connection = {computer, all_neighbors[i], all_neighbors[j]}
                if connection not in connected:
                    connected.append(connection)

chief = list()
for connection in connected:
    for c in connection:
        if c[0] == 't' and connection not in chief:
            chief.append(connection)

print(len(chief))
