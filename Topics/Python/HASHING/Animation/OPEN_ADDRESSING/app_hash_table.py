from flask import Flask, request, jsonify, render_template
from hash_class import HashTable

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/create", methods=["POST"])
def create_table():
    global H
    size = int(request.json.get("size", 10))
    H = HashTable(size=size)
    return jsonify(H.to_dict())

@app.route("/find", methods=["GET"])
def find_route():
    key = request.args.get("key")
    val = request.args.get("val")
    idx, probes = H.find(key, val)

    if idx is not None:
        return jsonify({
            "success": True,
            "index": idx,
            "probes": probes,
            "table": H.to_dict()
        })
    else:
        return jsonify({
            "success": False,
            "probes": probes,
            "table": H.to_dict()
        })

@app.route("/insert", methods=["POST"])
def insert():
    global H
    key = request.json.get("key")
    val = request.json.get("val")
    probe = request.json.get("probe", "linear")

    if probe == "linear":
        success, probes = H.linear_resolution(key, val)
    elif probe == "quadratic":
        success, probes = H.quadratic_resolution(key, val)
    else:
        success, probes = False, []

    return jsonify({
        "success": success,
        "table": H.to_dict(),
        "inserted": {"key": key, "val": val, "probe": probe},
        "probes": probes   # ✅ include probe sequence
    })



@app.route("/delete", methods=["DELETE"])
def delete_route():
    global H
    key = request.json.get("key")
    val = request.json.get("val")
    probe = request.json.get("probe", "linear")

    if probe == "linear":
        success, probes, deleted_idx = H.delete(key, val, 0)
    elif probe == "quadratic":
        success, probes, deleted_idx = H.delete(key, val, 1)
    else:
        success, probes, deleted_idx = False, [], None

    return jsonify({
        "success": success,
        "table": H.to_dict(),
        "deleted": {"key": key, "val": val, "index": deleted_idx},
        "probes": probes
    })


@app.route("/collision_stats", methods=["GET"])
def collision_stats():
    
    total, average = H.average_chain_length()
    stats = {
        "total_elements": total,
        "collision_count": H.collision_count(),
        "max_chain_length": H.max_chain_length(),
        "average_chain_length": average
    }
    return jsonify(stats)


@app.route("/reset", methods=["POST"])
def reset():
    global H
    H = HashTable(size=10)
    return jsonify({"msg": "Hash table is reset"})
    
if __name__ == "__main__":
    app.run(debug=True)


