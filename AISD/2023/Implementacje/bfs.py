import queue

graph = {
    0: [1, 2, 4],
    1: [3, 5],
    2: [],
    3: [0, 5],
    4: [],
    5: [0, 1]
}

visited = set()
q = queue.Queue()
output = []


def bfs(graph, node):
    if node in visited:
        return

    visited.add(node)
    q.put(node)

    while not q.empty():
        neigh = q.get()
        output.append(neigh)
        for n in graph[neigh]:
            if n in visited:
                continue
            visited.add(n)
            q.put(n)
            bfs(graph, n)

bfs(graph, 0)
assert(output == [0, 1, 2, 4, 3, 5])
