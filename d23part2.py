lines = [l.strip() for l in open('day23.txt', 'r').readlines()]

connections = set()
for l in lines:
    c1, c2 = l.split('-')
    connections.add((c1, c2))

# create adjacency matrix
adj_matrix = dict()
for c in connections:
    adj_matrix.setdefault(c[0], set()).add(c[1])
    adj_matrix.setdefault(c[1], set()).add(c[0])

# stores longest sequence found so far
l_seq = set()
# temp storage for vertices visited during single search
visited_this_run = set()


# recursively finds all complete graphs that given vertex belongs to and checks if it is the longest found so far
# params:
# - v: the vertex being examined
# - complete_found: list of vertices representing the current complete graph that includes 'v'
# for the initial call v = any vertex, and complete_found is a list containing v
def find_largest_complete_graph(v, complete_found):
    # mark current node as visited
    visited_this_run.add(v)
    # check if currently found graph is the largest so far
    if len(complete_found) > len(l_seq):
        l_seq.clear()
        l_seq.update(complete_found[:])
    # get all neighbors
    neighbors = adj_matrix[v]
    # among all neighbors find those connected with all vertices of complete graph found so far
    # continue search for neighbors not visited during this run
    for n in neighbors:
        if all_connected(n, complete_found) and n not in visited_this_run:
            extend_complete = complete_found[:]
            extend_complete.append(n)
            find_largest_complete_graph(n, extend_complete)


# check if given vertex is directly connected with all vertices from the list
def all_connected(vertex, graph):
    for i in graph:
        if vertex not in adj_matrix[i]:
            return False
    return True


# run search for each vertex, clear cache after
for n in adj_matrix:
    find_largest_complete_graph(n, [n])
    visited_this_run = set()
print(f"graph size: {len(l_seq)}, sequence: {','.join(sorted(l_seq))}")
