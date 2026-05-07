import heapq
import random 

def generate_weighted_graph(num_nodes=6):
    # Create node labels A, B, C...
    labels = [chr(65 + i) for i in range(num_nodes)]
    graph = {label: [] for label in labels}

    def add_edge(u, v):
        weight = random.randint(1, 10)
        # prevent duplicate edges
        if not any(neigh == v for neigh, _ in graph[u]):
            graph[u].append((v, weight))
            graph[v].append((u, weight))

    # Step 1: spanning tree for connectivity
    for i in range(1, num_nodes):
        j = random.randint(0, i - 1)
        add_edge(labels[i], labels[j])

    # Step 2: add extra edges with degree ≤ 3
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if (all(neigh != labels[j] for neigh, _ in graph[labels[i]])
                and random.random() < 0.3
                and len(graph[labels[i]]) < 3
                and len(graph[labels[j]]) < 3):
                add_edge(labels[i], labels[j])

    # Normalize to JSON‑friendly lists
    normalized = {u: [[v, w] for v, w in neighbors] for u, neighbors in graph.items()}
    return normalized


import heapq
from flask import jsonify

def dijkstra(graph, source):
    # Initialize distances and predecessors
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    predecessors = {node: None for node in graph}
    steps = []

    # Priority queue
    pq = [(0, source)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_dist > distances[current_node]:
            continue

        # Record visit
        steps.append({"type": "visit", "node": current_node})

        # Relax neighbors
        for neighbor, weight in graph.get(current_node, []):
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (new_dist, neighbor))

                # Record update
                steps.append({
                    "type": "update",
                    "from": current_node,
                    "to": neighbor,
                    "newDistance": new_dist
                })

    # Build paths for all nodes
    paths = {}
    for node in graph:
        paths[node] = reconstruct_path(predecessors, node)

    return {
        "distances": distances,
        "predecessors": predecessors,
        "paths": paths,
        "steps": steps
    }

def reconstruct_path(predecessors, target):
    # Handle unreachable nodes
    if target not in predecessors:
        return []

    path = []
    while target is not None:
        path.append(target)
        target = predecessors[target]
    return path[::-1]

#graph = generate_weighted_graph()
#graph = {
#    'A': [('B', 10), ('C', 4), ('F', 2)],
#    'B': [('A', 10), ('D', 5), ('E', 4)],
#    'C': [('A', 4), ('F', 8)],
#    'D': [('B', 5), ('F', 4)],
#    'E': [('B', 4)],
#    'F': [('A', 2), ('C', 8), ('D', 4)]
#}
#print("Graph :", graph, "\n")

#result = dijkstra(graph, "A")
#print("Distances:", result["distances"], "\n")
#print("Predecessors:", result["predecessors"], "\n")
#print("Paths:", result["paths"], "\n")
#print("Steps:", result["steps"][:5])  # first few steps
