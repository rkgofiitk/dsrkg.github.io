from flask import Flask, request, jsonify, render_template
from treeOperations import BinaryTree   # your class file


app = Flask(__name__)
bt = BinaryTree()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/reset', methods=['POST'])
def reset_tree():
    bt.root = None   # clear the tree
    return jsonify({"tree": None, "empty": True})

@app.route("/insert", methods=["POST"])
def insert_node():
    key_str = request.json.get("key")
    if not key_str or not key_str.isdigit():
        return jsonify(None)  # invalid input
    key = int(key_str)
    success = bt.insert(key)
    if not success:
        return jsonify(None)   # limit reached
    return jsonify(bt.to_dict())

@app.route("/delete", methods=["POST"])
def delete_node():
    key_str = request.json.get("key")
    if not key_str or not key_str.isdigit():
        return jsonify(None)  # invalid input
    key = int(key_str)
    before = bt.node_count()
    bt.delete(key)
    after = bt.node_count()
    if before == after:
        return jsonify(None)  # node not found
    if bt.root is None:
        return jsonify({"empty": True})  # tree is now empty
    return jsonify(bt.to_dict())


@app.route("/traverse/<order>", methods=["GET"])
def traverse(order):
    if order == "preorder":
        result = bt.preorder_traversal()   # e.g. [10, 5, 3, 7, 15]
    elif order == "inorder":
        result = bt.inorder_traversal()    # e.g. [3, 5, 7, 10, 15]
    elif order == "postorder":
        result = bt.postorder_traversal()  # e.g. [3, 7, 5, 15, 10]
    else:
        return jsonify({"error": "Unknown order"}), 400

    return jsonify(result)   # sends JSON array, not string

@app.route("/tree")
def get_tree():
    if bt.root is None:
        return jsonify({"empty": True})
    return jsonify(bt.to_dict())


if __name__ == "__main__":
    app.run(debug=True)
