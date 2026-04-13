MAX_NODES = 15  # or whatever limit you want

class Node:
    _id_counter = 0  # class-level counter shared by all nodes

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        # assign a unique, stable id
        self.id = Node._id_counter
        Node._id_counter += 1


class BinaryTree:
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
        if key == node.data:
            return  # Ignore duplicates (or handle differently)

        if key > node.data:
            if node.right is not None:
                self._insert_helper(node.right, key)
            else:
                node.right = Node(key)
        else:  # key < node.data
            if node.left is not None:
                self._insert_helper(node.left, key)
            else:
                node.left = Node(key)
        
    def multiple_inserts(self, s): 
        # Remove whitespaces in input
        new_str = s.replace(" ","")

        # Return if input string is emoty
        if not new_str:
            return

        # Extract input elements delimited by commas 
        new_str = [e for e in new_str.split(',')]   

        cnt = 0   # For counting insertions 

        # Find number of insertions
        n = len(new_str)

        # Insert elements one at a time
        for item in new_str:
            if cnt == n: # Return if maximum is reached 
                return
            else:
                self.insert(int(item)) # Leading/trailing spaces
                cnt += 1 # Increment after insertion        


    def search(self, key):
        return self._search_helper(self.root, key)

    def _search_helper(self, node, key):
        if node is None or node.data == key:
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

        if key < node.data:
            node.left = self._delete_helper(node.left, key)
        elif key > node.data:
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
                node.data = min_node.data
                node.right = self._delete_helper(node.right, min_node.data)
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
        return self._find_min(self.root).data

    def get_maximum(self):
        if self.root == None:
            return None
        return self._find_max(self.root).data

    def inorder_traversal(self):
        l = self._inorder_helper(self.root)
        return l

    def _inorder_helper(self, node):
        if node is None:
            return []

        result = []
        result.extend(self._inorder_helper(node.left))
        result.append(node.data)
        result.extend(self._inorder_helper(node.right))
        return result

    def preorder_traversal(self):
        l = self._preorder_helper(self.root)
        return l


    def _preorder_helper(self, node):
        if node is None:
            return []

        result = []
        result.append(node.data)
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
        result.append(node.data)
        return result

    def makenull(self):
        self.root = None 

    def to_dict(self, node=None):
        # Default to root if no node is passed
        if node is None:
            node = self.root
        if node is None:
            return None

        # Build dictionary recursively
        children = []
        if node.left:
            children.append(self.to_dict(node.left))
        if node.right:
            children.append(self.to_dict(node.right))

        return {
            "id" : node.id,
            "name": str(node.data),
            "children": children
        }

    def node_count(self):
        return self._count_helper(self.root) 

    def _count_helper(self, node):
        if node is None:
            return 0 

        return 1 + self._count_helper(node.left) + self._count_helper(node.right)

##   Experiment with operations


