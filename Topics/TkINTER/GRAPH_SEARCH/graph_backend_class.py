import random
from collections import deque

class Graph:
    def __init__(self, n, avg):
        self.adj_list = {}
        self.num_nodes = n
        self.prob = self.calculate_probability(n, avg)

    def calculate_probability(self, num_nodes, avg_connections=3):
        if num_nodes <= 1:
            return 0.0
        return min(1.0, avg_connections / (num_nodes - 1))

    def generate_random_graph(self, max_conn=3):
        for i in range(self.num_nodes):
            self.add_vertex(i)

        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if len(self.adj_list[i]) >= max_conn or len(self.adj_list[j]) >= max_conn:
                    continue
                if random.random() < self.prob:
                    self.add_edge(i, j)
        return self

    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, v1, v2, directed=False, weighted=False):
        self.add_vertex(v1)
        self.add_vertex(v2)

        if not weighted:
            w = random.randint(1, 20)
            self.adj_list[v1].append((v2, w))
            if not directed:
                self.adj_list[v2].append((v1, w))
        else:
            self.adj_list[v1].append((v2, None))
            if not directed:
                self.adj_list[v2].append((v1, None))

    def remove_edge(self, v1, v2, directed=False):
        self.adj_list[v1] = [(nbr, w) for nbr, w in self.adj_list.get(v1, []) if nbr != v2]
        if not directed:
            self.adj_list[v2] = [(nbr, w) for nbr, w in self.adj_list.get(v2, []) if nbr != v1]

    def remove_vertex(self, vertex):
        for v in self.adj_list:
            self.adj_list[v] = [(nbr, w) for nbr, w in self.adj_list[v] if nbr != vertex]
        if vertex in self.adj_list:
            del self.adj_list[vertex]

    def initialize_lists(self):
        self.marker = ["u"] * self.num_nodes
        self.list_order = []

    def start_dfs(self):
        self.initialize_lists()
        for vertex in range(self.num_nodes):
            if self.marker[vertex] == "u":
                self.dfs_recursive(vertex)

    def dfs_recursive(self, start_vertex):
        self.marker[start_vertex] = "v"
        self.list_order.append(chr(65 + int(start_vertex)))
        for nbr, _ in self.adj_list[start_vertex]:
            if self.marker[nbr] != "v":
                self.dfs_recursive(nbr)

    def start_bfs(self):
        self.initialize_lists()
        for vertex in range(self.num_nodes):
            if self.marker[vertex] == "u":
                queue = deque([vertex])
                self.marker[vertex] = "v"
                self.list_order.append(chr(65 + int(vertex)))
                self.bfs_recursive(queue)

    def bfs_recursive(self, queue=None):
        if not queue:
            return
        current_vertex = queue.popleft()
        for nbr, _ in self.adj_list[current_vertex]:
            if self.marker[nbr] != "v":
                self.list_order.append(chr(65 + int(nbr)))
                self.marker[nbr] = "v"
                queue.append(nbr)
        self.bfs_recursive(queue)

    def display(self):
        for vertex, neighbors in self.adj_list.items():
            char_v = chr(65 + int(vertex))
            # Include both neighbor and weight in the display
            char_nbrs = [f"{chr(65 + int(nbr))}({w})" for nbr, w in neighbors]
            print(f"{char_v} -> {char_nbrs}")


# Example Usage
#g = Graph(10, 3)
#g.generate_random_graph(5)
#g.display()

#g.start_dfs()
#print("DFS list (All Components):", g.list_order)

#g.start_bfs()
#print("BFS list (All Components):", g.list_order)

