from flask import Flask, render_template, jsonify
from binary_tree_ops import BinaryTree

app = Flask(__name__)

bt = BinaryTree()
bt.create_tree()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tree")
def get_tree():
    global bt
    bt = BinaryTree()
    bt.create_tree()
    return jsonify(bt.to_dict())


@app.route("/traverse/<order>", methods=["GET"])
def traverse(order):
    global bt
    if order == "preorder":
        result = bt.preorder_traversal()   # e.g. [10, 5, 3, 7, 15]
    elif order == "inorder":
        result = bt.inorder_traversal()    # e.g. [3, 5, 7, 10, 15]
    elif order == "postorder":
        result = bt.postorder_traversal()  # e.g. [3, 7, 5, 15, 10]
    else:
        return jsonify({"error": "Unknown order"}), 400

    return jsonify(result)   # sends JSON array, not string


if __name__ == "__main__":
    app.run(debug=True)
