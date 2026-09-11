from flask import Flask, render_template, request, jsonify
from treeOperations import BST

app = Flask(__name__)
bt = BST() 

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/insert", methods=["POST"])
def insert_node():
    key_str = request.json.get("key")
    if not key_str or not key_str.isdigit():
        return jsonify(None)  # invalid input
    key = int(key_str)
    success = bt.insert(key)
    if not success:
        return jsonify(None)   # limit reached
    bt.update_height_and_balance()
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
        bt.update_height_and_balance()
        return jsonify({"empty": True})  # tree is now empty
    bt.update_height_and_balance()
    return jsonify(bt.to_dict())

@app.route('/tree', methods=['GET'])
def get_tree():
    try:
        if bt.root is None:
            return jsonify({"tree": None, "empty": True})
        return jsonify({"tree": bt.to_dict(), "empty": False})
    except Exception as e:
        return jsonify({"error": str(e), "tree": None, "empty": True}), 500

@app.route('/rotate', methods=['POST'])
def rotate_node():
    key = int(request.json['key'])
    pivot = bt.search(key)
    if not pivot:
        return jsonify({"error": f"Node {key} not found", "tree": bt.to_dict()})

    if pivot.balance > 1:
        if pivot.left and pivot.left.balance >= 0:
            new_subtree = bt.rotate_right(pivot)  # LL
        else:
            pivot.left = bt.rotate_left(pivot.left)  # LR
            new_subtree = bt.rotate_right(pivot)
    elif pivot.balance < -1:
        if pivot.right and pivot.right.balance <= 0:
            new_subtree = bt.rotate_left(pivot)  # RR
        else:
            pivot.right = bt.rotate_right(pivot.right)  # RL
            new_subtree = bt.rotate_left(pivot)
    else:
        return jsonify({"message": "Node is balanced, no rotation"})

    # IMPORTANT: update bt.root
    bt.root = bt.replace_node(bt.root, key, new_subtree)
    bt.update_height_and_balance()
    return jsonify({"tree": bt.to_dict()})

@app.route('/reset', methods=['POST'])
def reset_tree():
    bt.root = None   # clear the tree
    return jsonify({"tree": None, "empty": True})

@app.route("/traverse/<order>")
def traverse(order):
   # if bt.is_empty():
   #     return jsonify([])

    if order == "inorder":
        result = bt.inorder_traversal()
    elif order == "preorder":
        result = bt.preorder_traversal()
    elif order == "postorder":
        result = bt.postorder_traversal()
    else:
        return jsonify({"error": "Unknown traversal order"}), 400

    return jsonify(result)  # must be a list


if __name__ == '__main__':
    app.run(debug=True)
