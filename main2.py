from collections import defaultdict, OrderedDict
import time
from data_module import get_adj_matrix, write_solution

def count_leaves(tree):
    """Подсчитывает количество листьев в текущем остовном дереве"""
    leaves = 0
    for node in tree:
        if len(tree[node]) == 1:
            leaves += 1
    return leaves

def get_list_edges(sorted_tree):
    list_edges = []
    for node, neighbors in sorted_tree.items():
        for neigh in neighbors:
            if not list_edges.__contains__(sorted((node, neigh))):
                list_edges.append(sorted((node, neigh)))
    return sorted(list_edges)

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

def get_branches(tree):
    branches = defaultdict(list)
    for node, neighbors in tree.items():
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

def prima(n, matrix, INF = 9999999):
    selected = [0] * n
    no_edge = 0
    selected[0] = True
    tree = defaultdict(set)
    list_edges = []
    total_weight = 0
    while (no_edge < n - 1):
        print(no_edge, n - 1)
        minimum = INF
        x = 0
        y = 0
        for i in range(n):
            if selected[i]:
                for j in range(n):
                    if ((not selected[j]) and matrix[i][j]):
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

    sorted_tree = OrderedDict(sorted(tree.items()))
    print("Алгоритм Прима (вес, кол-во листьев):", total_weight, count_leaves(tree))
    # for node, neighbors in sorted_tree.items():
    #     print(f"Вершина {node}: {neighbors}")
    return tree

n = 64
max_leaves = n // 16
INF = 9999999
matrix = get_adj_matrix(n)

start_time = time.time()
sorted_tree = prima(n, matrix)
number_leaves = count_leaves(sorted_tree)
old_number_leaves = number_leaves
while number_leaves > max_leaves:
    branches = get_branches(sorted_tree)
    # for node, neighbors in branches.items():
    #     print(f"Вершина {node}: {neighbors}")
    res_branches = defaultdict(list)
    for leaf, vs in branches.items():
        min_weight = INF
        leaf_conn = 0
        our_leaf_conn = 0
        if leaf == vs[0]:  # висячая вершина
            for leaf2, vs2 in branches.items():
                if leaf == leaf2:
                    continue
                if min_weight > matrix[leaf][leaf2]:
                    min_weight = matrix[leaf][leaf2]
                    leaf_conn = leaf2
            res_branches[leaf] = [None, leaf_conn, min_weight - vs[2]]
            print(None, leaf, leaf_conn, vs[2], min_weight - vs[2])
        else:  # ветка
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
            res_branches[leaf] = [our_leaf_conn, leaf_conn, min_weight - vs[2]]
            print(our_leaf_conn, leaf, leaf_conn, vs[2], min_weight - vs[2])
    res_leaf = None
    res_min_diff_weight = INF
    for leaf, vs in res_branches.items():
        if res_min_diff_weight > vs[2]:
            res_min_diff_weight = vs[2]
            res_leaf = leaf
    print(f"Ветка с {res_leaf} может присоединиться с минимальной разницей {res_min_diff_weight}")
    child = branches[res_leaf][0]
    root = branches[res_leaf][1]
    leaf_conn = res_branches[res_leaf][1]
    if res_leaf == branches[res_leaf][0]:
        # print(child, root, leaf_conn)
        sorted_tree[child].remove(root)
        sorted_tree[root].remove(child)
        sorted_tree[child].add(leaf_conn)
        sorted_tree[leaf_conn].add(child)
    else:
        our_leaf_conn = res_branches[res_leaf][0]
        # print(our_leaf_conn, leaf_conn, child, root)
        if our_leaf_conn == res_leaf:
            sorted_tree[child].remove(root)
            sorted_tree[root].remove(child)
        else:
            sorted_tree[our_leaf_conn].remove(root)
            sorted_tree[root].remove(our_leaf_conn)
        sorted_tree[our_leaf_conn].add(leaf_conn)
        sorted_tree[leaf_conn].add(our_leaf_conn)
    number_leaves -= 1

end_time = time.time()
print(f"Время выполнения функции: {end_time - start_time} секунд")
# for node, neighbors in sorted_tree.items():
#     print(f"Вершина {node}: {neighbors}")
total_weight = get_weight(0, sorted_tree[0], sorted_tree)
count_leaves = count_leaves(sorted_tree)
print("Новый вес:", total_weight)
print("Старое кол-во листьев:", old_number_leaves)
print("Новое кол-во листьев:", count_leaves)

list_edges = get_list_edges(sorted_tree)
write_solution(n, total_weight, count_leaves, list_edges)
