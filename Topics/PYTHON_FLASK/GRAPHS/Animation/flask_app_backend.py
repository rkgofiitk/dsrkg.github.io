from flask import Flask, jsonify, request, render_template
from graph_core import Graph
import random   # ✅ Needed
from collections import deque # ✅ Needed

app = Flask(__name__) 
graph = None

# Store the last generated graph in memory
last_graph = {"nodes": [], "edges": []}

@app.route("/")
def home():
    # Serve your index.html from templates/
    return render_template("index.html")

@app.route("/generate_graph", methods=["POST"])
def generate_graph():
    global graph, last_graph
    data = request.get_json()
    avg_conn = 3
    num_nodes = int(data["nodes"])
    max_conn = int(data["max_conn"])

    # ✅ Build Graph object using your class
    graph = Graph(num_nodes, avg = avg_conn)
    graph.generate_random_graph(max_conn=max_conn)

    # Convert to JSON for frontend
    nodes = [{"id": i, "label": chr(65 + i)} for i in range(num_nodes)]
    edges = []
    for v, neighbors in graph.adj_list.items():
        for nbr, w in neighbors:
            edges.append({"source": v, "target": nbr, "weight": w})

    last_graph = {"nodes": nodes, "edges": edges}
    return jsonify(last_graph)



@app.route("/graph", methods=["GET"])
def get_graph():
    global last_graph
    return jsonify(last_graph)



@app.route("/dfs", methods=["POST"])
def dfs_route():
    start = request.json.get("start")
    order, tree_edges = graph.start_dfs(start)
    return jsonify({"order": order, "tree_edges": tree_edges})



@app.route("/bfs", methods=["POST"])
def bfs_route():
    start = request.json.get("start")
    order, tree_edges = graph.start_bfs(start)
    return jsonify({"order": order, "tree_edges": tree_edges})


if __name__ == "__main__":
    app.run(debug=True)

