from flask import Flask, render_template, request, jsonify
from pq_operations import MaxHeap 

app = Flask(__name__)

pq = MaxHeap()


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/reset', methods=['POST'])
def reset_heap():
    try:
        pq.reset_heap()   # clear the heap
        return jsonify({"tree": None, "empty": True})
    except Exception as e:
        return jsonify({"error": str(e), "tree": None, "empty": True}), 500

@app.route("/insert", methods=["POST"])
def insert_node():
    key_str = request.json.get("key")
    if not key_str or not key_str.isdigit():
        return jsonify(None)  # invalid input
    key = int(key_str)
    success = pq.insert(key)
    if not success:
        return jsonify(None)   # limit reached
    return jsonify(pq.to_dict())


@app.route("/delete", methods=["POST"])
def delete_root_route():
    deleted_val = pq.delete_root()

    if deleted_val is None:
        # Heap was empty
        return jsonify({"error": "Heap is empty"})

    if pq.node_count == 0:
        # After deletion, heap is now empty
        return jsonify({"empty": True})

    # Return updated heap structure for frontend rendering
    return jsonify(pq.to_dict())

@app.route('/tree', methods=['GET'])
def get_tree():
    try:
        if pq.root is None:
            return jsonify({"tree": None, "empty": True})
        return jsonify({"tree": pq.to_dict(), "empty": False})
    except Exception as e:
        return jsonify({"error": str(e), "tree": None, "empty": True}), 500

@app.route("/heapifyUp", methods=["POST"])
def heapify_up_route():
    try:
        data = request.get_json()
        key = int(data["key"])
        node = pq.find_node(key)   # implement this helper

        if not node:
            return jsonify({"error": f"Node {key} not found"}), 400

        steps = pq.heapify_up(node)
        return jsonify({"steps": steps})

    except Exception as e:
        print("HeapifyUp server error:", e)
        return jsonify({"error": "Internal server error"}), 500

@app.route("/heapifyDown", methods=["POST"])
def heapify_down_route():
    try:
        # Always start from the root for heapify-down
        if not pq.root:
            return jsonify({"error": "Heap is empty"}), 400

        steps = pq.heapify_down()

        return jsonify({"steps": steps})

    except Exception as e:
        print("HeapifyDown server error:", e)
        return jsonify({"error": "Internal server error"}), 500


@app.route("/traverse/<order>", methods=["GET"])
def traverse(order):
    if order == "preorder":
        result = pq.preorder_traversal()   # e.g. [10, 5, 3, 7, 15]
    elif order == "inorder":
        result = pq.inorder_traversal()    # e.g. [3, 5, 7, 10, 15]
    elif order == "postorder":
        result = pq.postorder_traversal()  # e.g. [3, 7, 5, 15, 10]
    else:
        return jsonify({"error": "Unknown order"}), 400

    return jsonify(result)   # sends JSON array, not string


if __name__ == "__main__":
    app.run(debug=True)
