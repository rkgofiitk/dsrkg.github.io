MAX_NODES = 15  # or whatever limit you want

class Node:
    _id_counter = 0  # class-level counter shared by all nodes

    def __init__(self, data):
        self.key = data
        self.left = None
        self.right = None

        # balance and height 
        self.balance = 0
        self.height = 0

        # assign a unique, stable id
        self.id = Node._id_counter
        Node._id_counter += 1

       


class BST:
    def __init__(self):
        self.root = None

    def isEmpty(self):
        return self.root == None

    def insert(self, key):
        if self.node_count() >= MAX_NODES:
            return False   # signal failure
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_helper(self.root, key)
        return True

    

    def _insert_helper(self, node, key):
        if key == node.key:
            return  # Ignore duplicates (or handle differently)

        if key > node.key:
            if node.right is not None:
                self._insert_helper(node.right, key)
            else:
                node.right = Node(key)
        else:  # key < node.data
            if node.left is not None:
                self._insert_helper(node.left, key)
            else:
                node.left = Node(key)


    # Search key in BST

    def search(self, key):
        return self._search_helper(self.root, key)

    def _search_helper(self, node, key):
        if node is None or node.key == key:
            return node

        # Recursively search in the left and right subtrees
        left_result = self._search_helper(node.left, key)
        if left_result: # In left subtree
            return left_result

        right_result = self._search_helper(node.right, key)
        if right_result: # In right subtree
            return right_result

        return None  # Searched key is absent 

    def delete(self, key):
        self.root = self._delete_helper(self.root, key)

    def _delete_helper(self, node, key):
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete_helper(node.left, key)
        elif key > node.key:
            node.right = self._delete_helper(node.right, key)
        else:  # key == node.data
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                min_node = self._find_min(node.right)
                node.key = min_node.key
                node.right = self._delete_helper(node.right, min_node.key)
        return node

    def _find_min(self, node):
        current = node
        while current.left:
            current = current.left
        return current 

    def _find_max(self, node):
        current = node
        while current.right:
            current = current.right

        return current 

    def get_minimum(self):
        if self.root == None:
            return None 
        return self._find_min(self.root).key

    def get_maximum(self):
        if self.root == None:
            return None
        return self._find_max(self.root).key

    def inorder_traversal(self):
        l = self._inorder_helper(self.root)
        return l

    def _inorder_helper(self, node):
        if node is None:
            return []

        result = []
        result.extend(self._inorder_helper(node.left))
        result.append(node.key)
        result.extend(self._inorder_helper(node.right))
        return result

    def preorder_traversal(self):
        l = self._preorder_helper(self.root)
        return l

    def _preorder_helper(self, node):
        if node is None:
            return []

        result = []
        result.append(node.key)
        result.extend(self._preorder_helper(node.left))
        result.extend(self._preorder_helper(node.right))
        return result

    def postorder_traversal(self):
        l = self._postorder_helper(self.root)
        return l
    def _postorder_helper(self, node):
        if node is None:
            return []

        result = []
        result.extend(self._postorder_helper(node.left))
        result.extend(self._postorder_helper(node.right))
        result.append(node.key)
        return result

    def makenull(self):
        self.root = None 

    def to_dict(self, node=None):
        # Default to root if no node is passed
        if node is None:
            node = self.root
        if node is None:
            return {"empty": True}   # <-- instead of None

        # Build dictionary recursively
        children = []
        if node.left:
            children.append(self.to_dict(node.left))
        if node.right:
            children.append(self.to_dict(node.right))

        return {
            "id": node.id,
            "name": str(node.key),
            "balance": node.balance,
            "children": children
        }

    def node_count(self):
        return self._count_helper(self.root) 

    def _count_helper(self, node):
        if node is None:
            return 0 

        return 1 + self._count_helper(node.left) + self._count_helper(node.right)


    def rotate_left(self, pivot):
        new_root = pivot.right
        tmp = new_root.left

        new_root.left = pivot
        pivot.right = tmp

        self._update_ht_and_bl(pivot)
        self._update_ht_and_bl(new_root)

        return new_root

    def rotate_right(self, pivot):
        new_root = pivot.left
        tmp = new_root.right

        new_root.right = pivot
        pivot.left = tmp

        self._update_ht_and_bl(pivot)
        self._update_ht_and_bl(new_root)

        return new_root


    def replace_node(self, node, key, new_subtree):
        if not node:
            return None
        if node.key == key:
            return new_subtree
        elif key < node.key:
            node.left = self.replace_node(node.left, key, new_subtree)
        else:
            node.right = self.replace_node(node.right, key, new_subtree)
        return node


    def update_height_and_balance(self):
        self._update_ht_and_bl(self.root)

    def _update_ht_and_bl(self, node):
        if not node:
            return -1   # ensures leaf height = 0
        left_height = self._update_ht_and_bl(node.left)
        right_height = self._update_ht_and_bl(node.right)
        node.height = 1 + max(left_height, right_height)
        node.balance = left_height - right_height
        return node.height


    def print_balances(self, node=None):
        if node is None:
            node = self.root
        if not node:
            return
        print(f"Node {node.key}: height={node.height}, balance={node.balance}")
        if node.left:
            self.print_balances(node.left)
        if node.right:
            self.print_balances(node.right)

##   Experiment with operations
#bt = BST() 

#bt.insert(65)
#bt.insert(55)
#bt.insert(45)
#bt.insert(85)
#bt.insert(75)
#bt.insert(95)
#bt.insert(25)
#bt.delete(25)
#bt.update_height_and_balance()
#bt.print_balances()
#ret = bt.search(65)
#print(type(ret.key))
#print("found key:", ret.key)
#print(bt.to_dict())


