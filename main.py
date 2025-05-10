from data_module import get_adj_matrix, write_solution
import heapq
from collections import defaultdict, OrderedDict

number = 64
matrix = get_adj_matrix(number)

def count_leaves(tree):
    """Подсчитывает количество листьев в текущем остовном дереве"""
    leaves = 0
    for node in tree:
        if len(tree[node]) == 1:
            leaves += 1
    return leaves

def prim_modified(graph, max_leaves):
    n = len(graph)
    sum = 0
    count_edges = 0
    visited = set()
    edges = []
    tree = defaultdict(set)
    list_edges = []

    start_node = 0
    visited.add(start_node)

    for neighbor in range(n):
        if graph[start_node][neighbor] > 0:
            heapq.heappush(edges, (graph[start_node][neighbor], start_node, neighbor))

    while len(visited) < n:
        while edges:
            weight, u, v = heapq.heappop(edges)
            if v not in visited:
                tree[u].add(v)
                tree[v].add(u)
                new_leaves = count_leaves(tree)
                if new_leaves <= max_leaves:
                    visited.add(v)
                    sum += weight
                    list_edges.append(sorted((u, v)))
                    count_edges += 1
                    break
                else:
                    tree[u].remove(v)
                    tree[v].remove(u)

        for neighbor in range(n):
            if graph[v][neighbor] > 0 and neighbor not in visited:
                heapq.heappush(edges, (graph[v][neighbor], v, neighbor))

    return tree, sum, count_edges, list_edges


max_leaves = number // 16
result_tree, weight, count_edges, list_edges = prim_modified(matrix, max_leaves)

sorted_tree = OrderedDict(sorted(result_tree.items()))

list_edges = sorted(list_edges)
print(weight, count_edges, count_leaves(result_tree))
write_solution(number, weight, count_leaves(result_tree), list_edges)
