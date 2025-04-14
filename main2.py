from collections import defaultdict, OrderedDict


def count_leaves(tree):
    """Подсчитывает количество листьев в текущем остовном дереве"""
    leaves = 0
    for node in tree:
        if len(tree[node]) == 1:
            leaves += 1
    return leaves

def get_weight(root_node, childs, sorted_tree):
    if len(childs) == 0:
        return 0
    weight = 0
    for child in childs:
        weight += matrix[root_node][child]
        new_childs = set(sorted_tree[child])
        new_childs.remove(root_node)
        weight += get_weight(child, new_childs, sorted_tree)
    return weight

number = 64
file = open(f"Taxicab_{number}.txt", "r")
lines = file.readlines()
file.close()
n = int(lines[0].replace('n = ', ''))
print("Кол-во вершин:", n)
matrix = []
for i in range(n):
    matrix.append([0] * n)
points = []
for i in range(1, len(lines)):
    elements = lines[i].split('\t')
    x, y = int(elements[0]), int(elements[1])
    points.append([x, y])
for i in range(n):
    x, y = points[i]
    for j in range(i + 1, n):
        a, b = points[j]
        dest = abs(x - a) + abs(y - b)
        matrix[i][j] = dest
        matrix[j][i] = dest

INF = 9999999
# create a array to track selected vertex
# selected will become true otherwise false
selected = [0] * n
# set number of edge to 0
no_edge = 0
# the number of egde in minimum spanning tree will be
# always less than(V - 1), where V is number of vertices in
# graph
# choose 0th vertex and make it true
selected[0] = True
tree = defaultdict(set)
list_edges = []
total_weight = 0
while (no_edge < n - 1):
    # For every vertex in the set S, find the all adjacent vertices
    # , calculate the distance from the vertex selected at step 1.
    # if the vertex is already in the set S, discard it otherwise
    # choose another vertex nearest to selected vertex  at step 1.
    minimum = INF
    x = 0
    y = 0
    for i in range(n):
        if selected[i]:
            for j in range(n):
                if ((not selected[j]) and matrix[i][j]):
                    # not in selected and there is an edge
                    if minimum > matrix[i][j]:
                        minimum = matrix[i][j]
                        x = i
                        y = j
    tree[x].add(y)
    tree[y].add(x)
    total_weight += matrix[x][y]
    list_edges.append(sorted((x, y)))
    selected[y] = True
    no_edge += 1

# print("Остовное дерево:")
sorted_tree = OrderedDict(sorted(tree.items()))
print("Алгоритм Прима (вес, кол-во листьев):", total_weight, count_leaves(tree))

# for node, neighbors in sorted_tree.items():
#     print(f"Вершина {node}: {neighbors}")
def get_branches(sorted_tree):
    branches = defaultdict(list)
    for node, neighbors in sorted_tree.items():
        child = node
        root = None
        if len(neighbors) == 1:
            child = node
            root = next(iter(neighbors))
            while len(tree[root]) == 2:
                new_set = set(tree[root])
                new_set.remove(child)
                child = root
                i = iter(new_set)
                root = next(i)
            branches[node] = [child, root, matrix[child][root]]
    # for node, neighbors in branches.items():
    #     print(f"Вершина {node}: {neighbors}")
    return branches


max_leaves = n // 16
del_leaf = None
while count_leaves(sorted_tree) > max_leaves:
    print(count_leaves(sorted_tree))

    branches = get_branches(sorted_tree)
    for leaf, vs in branches.items():
        print(leaf, vs)
        if leaf == vs[0]:  # висячая вершина
            min_weight = INF
            leaf_conn = 0
            for leaf2, vs2 in branches.items():
                if leaf == leaf2:
                    continue
                if min_weight > matrix[leaf][leaf2]:
                    min_weight = matrix[leaf][leaf2]
                    leaf_conn = leaf2
            print(leaf, leaf_conn, vs[2], min_weight)
            sorted_tree[vs[0]].remove(vs[1])
            sorted_tree[vs[1]].remove(vs[0])
            sorted_tree[vs[0]].add(leaf_conn)
            sorted_tree[leaf_conn].add(vs[0])
            del_leaf = leaf
            # branches.pop(leaf, None)
        else:  # ветка
            min_weight = INF
            leaf_conn = 0
            our_leaf_conn = 0
            for leaf2, vs2 in branches.items():
                if leaf == leaf2 or vs[0] == leaf2:
                    continue
                if min_weight > matrix[leaf][leaf2]:
                    min_weight = matrix[leaf][leaf2]
                    leaf_conn = leaf2
                    our_leaf_conn = leaf
                if min_weight > matrix[vs[0]][leaf2]:
                    min_weight = matrix[vs[0]][leaf2]
                    leaf_conn = leaf2
                    our_leaf_conn = vs[0]
            print(our_leaf_conn, leaf_conn, vs[2], min_weight)
            if our_leaf_conn == leaf:
                sorted_tree[vs[0]].remove(vs[1])
                sorted_tree[vs[1]].remove(vs[0])
            else:
                sorted_tree[our_leaf_conn].remove(vs[1])
                sorted_tree[vs[1]].remove(our_leaf_conn)
            sorted_tree[our_leaf_conn].add(leaf_conn)
            sorted_tree[leaf_conn].add(our_leaf_conn)
            del_leaf = leaf
            # branches.pop(leaf, None)
        break

# for node, neighbors in sorted_tree.items():
#     print(f"Вершина {node}: {neighbors}")
print("Новый вес:", get_weight(0, sorted_tree[0], sorted_tree))
print("Новое кол-во листьев:", count_leaves(sorted_tree))

