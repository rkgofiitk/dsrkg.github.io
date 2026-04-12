import random
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    data = request.get_json()
    num_nodes = data.get('num_nodes', 5)

    # Create node labels A, B, C...
    labels = [chr(65 + i) for i in range(num_nodes)]
    graph = {label: [] for label in labels}

    # Step 1: ensure connectivity with a spanning tree
    for i in range(1, num_nodes):
        j = random.randint(0, i-1)
        graph[labels[i]].append(labels[j])
        graph[labels[j]].append(labels[i])

    # Step 2: add extra random edges, but restrict degree ≤ 3
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if (labels[j] not in graph[labels[i]]
                and random.random() < 0.3
                and len(graph[labels[i]]) < 3
                and len(graph[labels[j]]) < 3):
                graph[labels[i]].append(labels[j])
                graph[labels[j]].append(labels[i])

    return jsonify(graph)

@app.route('/run_dfs', methods=['POST'])
def run_dfs():
    data = request.get_json()
    graph = data['graph']
    start = data['start']

    visited = set()
    snapshots = []

    def dfs_visit(node, step):
        visited.add(node)
        snapshots.append({
            "step": step,
            "current_node": node,
            "visited": list(visited),
            "edges_highlighted": []
        })
        for neighbor in graph[node]:
            if neighbor not in visited:
                snapshots[-1]["edges_highlighted"].append({
                    "source": node,
                    "target": neighbor
                })
                dfs_visit(neighbor, step+1)

    #  Call the helper inside run_dfs
    dfs_visit(start, 0)

    return jsonify(snapshots)
@app.route("/reset", methods=["POST"])
def reset():
    global current_graph, snapshots, visit_order, visit_counter, traversed_edges
    current_graph = None
    snapshots = []
    visit_order = {}
    visit_counter = 1
    traversed_edges = set()
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    app.run(debug=True)
