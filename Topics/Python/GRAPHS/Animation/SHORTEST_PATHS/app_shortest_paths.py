import random
import heapq
from flask import Flask, request, jsonify, render_template
from shortest_path import generate_weighted_graph, dijkstra, reconstruct_path 

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_graph', methods=['POST'])
def generate_random_graph():
    data = request.get_json()
    num_nodes = data.get('num_nodes', 5)
    graph = generate_weighted_graph(num_nodes)
    graph = {u: [[v, w] for (v, w) in neighbors] for u, neighbors in graph.items()}

    return jsonify(graph)


@app.route("/run_spath", methods=["POST"])
def run_spath():
    data = request.get_json()
    
    graph = data["graph"]
    start = data["start"]

    result = dijkstra(graph, start)

    # Ensure JSON‑friendly
    result["distances"] = dict(result["distances"])
    result["predecessors"] = dict(result["predecessors"])
    result["paths"] = {k: list(v) for k, v in result["paths"].items()}
    result["steps"] = list(result["steps"])

    return jsonify(result)



@app.route("/reset", methods=["POST"])
def reset():
    global currentGraph, snapshots, pathEdges, currentStep, startNode
    currentGraph = None
    startNode = None
    currentStep = 0
    snapshots = []
    pathEdges = set()
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    app.run(debug=True)
