class Graph:

    def __init__(self, vs):
        self.V = vs
        self.graph = []

    def addEdge(self, node0, node1, weight):
        self.graph.append([node0, node1, weight])

    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1

    def kruskal_mst(self):
        result = []
        self.graph = sorted(self.graph, key=lambda node: node[2])

        parent, rank = [], []

        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        edges = 0

        for (n0, n1, w) in self.graph:
            n0_parent = self.find(parent, n0)
            n1_parent = self.find(parent, n1)
            if n0_parent != n1_parent:
                result.append([n0, n1, w])
                self.union(parent, rank, n0_parent, n1_parent)
                edges += 1

            if edges == self.V - 1:
                break
        cost = 0
        print("Edges chosen for MST")
        for u, v, weight in result:
            cost += weight
            print(f"({u}) -- ({v}) weight {weight}")
        print("MST total weight", cost)

    
    def prim_mst(self):
        pass

if __name__ == '__main__':
    g = Graph(4)
    g.addEdge(0, 1, 10)
    g.addEdge(0, 2, 6)
    g.addEdge(0, 3, 5)
    g.addEdge(1, 3, 15)
    g.addEdge(2, 3, 4)

    g.kruskal_mst()
