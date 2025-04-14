number = 64
file = open(f"Taxicab_{number}.txt", "r")
lines = file.readlines()
file.close()
n = int(lines[0].replace('n = ', ''))
print(n)
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
print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))

import heapq
from collections import defaultdict, OrderedDict


def count_leaves(tree):
    """Подсчитывает количество листьев в текущем остовном дереве"""
    leaves = 0
    for node in tree:
        if len(tree[node]) == 1:
            leaves += 1
    return leaves


def prim_modified(graph, max_leaves):
    """
    Модифицированный алгоритм Прима

    graph - матрица смежности графа
    max_leaves - максимальное допустимое количество листьев
    """
    n = len(graph)
    sum = 0
    count_edges = 0
    visited = set()
    edges = []  # очередь приоритетов для ребер
    tree = defaultdict(set)  # текущее остовное дерево
    list_edges = []

    # Начинаем с первой вершины
    start_node = 0
    visited.add(start_node)

    # Добавляем все ребра от начальной вершины
    for neighbor in range(n):
        if graph[start_node][neighbor] > 0:
            heapq.heappush(edges, (graph[start_node][neighbor], start_node, neighbor))

    while len(visited) < n:
        # Получаем ребро с минимальным весом
        while edges:
            weight, u, v = heapq.heappop(edges)
            print(f"{u}-{v}: {weight}")
            if v not in visited:
                # Проверяем количество листьев после добавления ребра
                tree[u].add(v)
                tree[v].add(u)
                # new_leaves = count_leaves(tree)
                # if new_leaves <= max_leaves:
                visited.add(v)
                sum += weight
                list_edges.append(sorted((u, v)))
                count_edges += 1
                #     break
                # else:
                #     # Откатываем добавление ребра
                #     tree[u].remove(v)
                #     tree[v].remove(u)

        # Добавляем новые ребра от текущей вершины
        for neighbor in range(n):
            if graph[v][neighbor] > 0 and neighbor not in visited:
                heapq.heappush(edges, (graph[v][neighbor], v, neighbor))

    return tree, sum, count_edges, list_edges


max_leaves = n // 16
result_tree, weight, count_edges, list_edges = prim_modified(matrix, max_leaves)

print("Остовное дерево:")
l = 0
sorted_tree = OrderedDict(sorted(result_tree.items()))
for node, neighbors in sorted_tree.items():
    print(f"Вершина {node}: {neighbors}")
    l += 1

list_edges = sorted(list_edges)
print(len(list_edges))
print(l, weight, count_edges, count_leaves(result_tree))

# with open(rf"Agafonova_{number}_1.txt", "w", encoding='utf-8') as file:
#     file.write(f"c Вес дерева = {weight}, число листьев = {count_leaves(result_tree)},\n")
#     file.write(f"p edge {n} {len(list_edges)}\n")
#     for edge in list_edges:
#         file.write(f"e {edge[0] + 1} {edge[1] + 1}\n")

