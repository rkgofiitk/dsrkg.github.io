from flask import Flask, request, jsonify, render_template
from hash_class import Hash, Node, List 

import random
import time


app = Flask(__name__)

from flask import Flask, request, jsonify
from hash_class import Hash  # import your Hash class

app = Flask(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/create", methods=["POST"])
def create_table():
    global H
    size = int(request.json.get("size", 10))
    capacity = int(request.json.get("capacity", 20))
    H = Hash(size=size, capacity=capacity)
    return jsonify(H.to_dict())

@app.route("/insert", methods=["POST"])
def insert():
    key = request.json.get("key")
    val = request.json.get("val")
    H.insert(key, val)
    return jsonify({"message": f"Inserted ({key}, {val})"})

@app.route("/find", methods=["GET"])
@app.route("/find", methods=["GET"])
def find_route():
    key = int(request.args.get("key"))
    val = request.args.get("val")
    locs, index = H.find(key, val)
    if locs:
        return jsonify({
            "found": True,
            "values": [node.val for node in locs],
            "bucket": index
        })
    else:
        return jsonify({"found": False, "bucket": index})


@app.route("/delete", methods=["DELETE"])
def delete():
    key = request.json.get("key")
    val = request.json.get("val")
    deleted = H.delete(int(key), val)
    return jsonify({"deleted": deleted})


@app.route("/display", methods=["GET"])
def display():
    # Return the full table structure for visualization
    buckets = []
    for i, bucket in enumerate(H.table):
        chain = []
        tmp = bucket.head
        while tmp:
            chain.append({"key": tmp.key, "val": tmp.val})
            tmp = tmp.next
        buckets.append({"bucket": i, "chain": chain})
    return jsonify({"hash_table": buckets})


@app.route("/reset", methods=["POST"])
def reset():
    return jsonify({"msg": "Hash table is reset"})

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
    
if __name__ == "__main__":
    app.run(debug=True)


