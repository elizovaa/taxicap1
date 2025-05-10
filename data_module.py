
def get_adj_matrix(number):
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
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    return matrix

def write_solution(n, total_weight, count_leaves, list_edges):
    with open(rf"Agafonova_{n}_2.txt", "w", encoding='utf-8') as file:
        file.write(f"c Вес дерева = {total_weight}, число листьев = {count_leaves},\n")
        file.write(f"p edge {n} {len(list_edges)}\n")
        for edge in list_edges:
            file.write(f"e {edge[0] + 1} {edge[1] + 1}\n")

