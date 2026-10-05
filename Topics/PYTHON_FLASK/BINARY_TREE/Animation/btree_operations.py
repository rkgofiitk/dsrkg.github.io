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
#print(tree_dict)

#print(bt.preorder_traversal())
