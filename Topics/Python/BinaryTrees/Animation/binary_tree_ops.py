import random
from collections import deque
MAX_NODES = 15  # or whatever limit you want

import json

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

    # Generates a random value from integer range 1-100
    def generate_list(self):
        return random.sample(range(1, 100), MAX_NODES)
  
    # Creates a binary tree with random value by levelwise 
    # insertion method
    def create_tree(self):
        l = self.generate_list()
        for num in l:
            self.insert_random(num)

    # Levelwise insertion of nodes in a binary tree
    def insert_levelwise(self, val):

        new_node = Node(val)

        if not self.root:
            self.root = new_node
            return self.root
        
        queue = deque([self.root])

        while queue:
            current = queue.popleft()
            
            if not current.left:
                current.left = new_node
                return self.root
            else:
                queue.append(current.left)
            
            if not current.right:
                current.right = new_node
                return self.root
            else:
                queue.append(current.right)

    def insert_random(self, val):
        new_node = Node(val)

        if not self.root:
            self.root = new_node
            return self.root

        queue = deque([self.root])

        while queue:
            current = queue.popleft()

            # Randomly decide whether to insert left
            if not current.left and random.choice([True, False]):
                current.left = new_node
                return self.root
            else:
                if current.left:
                    queue.append(current.left)

            # Randomly decide whether to insert right
            if not current.right and random.choice([True, False]):
                current.right = new_node
                return self.root
            else:
                if current.right:
                    queue.append(current.right)

        # If we never inserted (because of skips), force insert at
        # first available spot
        queue = deque([self.root])
        while queue:
            current = queue.popleft()
            if not current.left:
                current.left = new_node
                return self.root
            elif not current.right:
                current.right = new_node
                return self.root
            else:
                queue.append(current.left)
                queue.append(current.right)

    def isEmpty(self):
        return self.root == None

    def insert(self, node, key):
        if self.node_count() >= MAX_NODES:
            return False   # signal failure
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_helper(self.root, node, key)
        return True

    def _insert_helper(self, node, child, key):
        if node is None:  # Reached leaf node
            return 
        elif node.left == None:
            if node.left == None:
                node= Node(key) # Insert as right child 
            else:
                node.left = Node(key)  # Insert as left child
        else: # Not a leaf 
            if key > node.data:
                if node.right is not None: # Traverse right branch
                    self._insert_helper(node.right, key)
                else: # End of right branch 
                    node.right = Node(key)
            else:
                if node.left is not None:  # Traverse left branch
                    self._insert_helper(node.left, key)
                else: # End of left branch
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

#bt = BinaryTree()
#bt.create_tree()
#tree_dict = bt.to_dict()  # serialize to dict

#print(bt.preorder_traversal())
