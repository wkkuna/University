graph = {
    0: [1, 2, 4],
    1: [3, 5],
    2: [],
    3: [0, 5],
    4: [],
    5: [0, 1]
}

visited = set()
output = []


def dfs(graph, node):
    if node not in visited:
        visited.add(node)
        output.append(node)

        for n in graph[node]:
            dfs(graph, n)


dfs(graph, 0)
assert(output == [0, 1, 3, 5, 2, 4])
