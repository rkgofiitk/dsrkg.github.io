import queue

MAX_NODES = 16

class Node:
    _id_counter = 0
    def __init__(self, data):
        self.key = data
        self.left = None
        self.right = None
        self.parent = None
        self.id = Node._id_counter
        Node._id_counter += 1

class MaxHeap:
    def __init__(self, capacity=MAX_NODES):
        self.root = None
        self.Q = queue.Queue()
        self.count = 0
        self.capacity = capacity

    def node_count(self):
        return self.count

    def reset_heap(self):
        self.__init__(MAX_NODES)
        self.print_heap()

    def insert(self, key):
        if self.node_count() == self.capacity:
            print("Limit reached, insertion of ", key, "not permitted")
            return False

        newNode = Node(key)
        if self.root is None:
            self.root = newNode
            self.Q.put(self.root)
            self.count += 1
            return True

        parent = self.Q.queue[0]  # peek
        if parent.left is None:
            parent.left = newNode
            newNode.parent = parent
        elif parent.right is None:
            parent.right = newNode
            newNode.parent = parent
            self.Q.get()  # parent now has two children, dequeue it

        self.Q.put(newNode)
        self.count += 1

        # Bubble-up
       # self._heapify_up(newNode)
        return True

    def delete_root(self):
        if self.root is None:
            return {"error": "Heap is empty"}

        # Case: only one node
        if self.count == 1:
            val = self.root.key
            self.root = None
            self.Q = queue.Queue()
            self.count = 0
            return {"deleted": val, "steps": []}

        steps = []
        val = self.root.key

        # Step 1: find deepest rightmost node via BFS
        bfsQ = queue.Queue()
        bfsQ.put(self.root)
        last_node = None
        while not bfsQ.empty():
            node = bfsQ.get()
            last_node = node
            if node.left:
                bfsQ.put(node.left)
            if node.right:
                bfsQ.put(node.right)

        # Step 2: swap root and last node keys
        steps.append({"action": "swap", "nodes": [str(self.root.key), str(last_node.key)]})
        self.root.key, last_node.key = last_node.key, self.root.key

        # Step 3: remove last node
        steps.append({"action": "remove", "node": str(last_node.key)})
        if last_node.parent:
            if last_node.parent.left == last_node:
                last_node.parent.left = None
            elif last_node.parent.right == last_node:
                last_node.parent.right = None
        last_node.parent = None

        self.count -= 1

        # Step 4: rebuild queue with BFS to preserve completeness
        newQ = queue.Queue()
        def bfs(node):
            if not node:
                return
            newQ.put(node)
            if node.left:
                bfs(node.left)
            if node.right:
                bfs(node.right)
        bfs(self.root)
        self.Q = newQ

        # Step 5: run heapify-down and collect steps
        steps.extend(self.heapify_down())

        return {"deleted": val, "steps": steps}

    def heapify_down(self):
        steps = []
        node = self.root
        while node and (node.left or node.right):
            largest = node
            if node.left:
                steps.append({"action": "compare", "nodes": [str(node.key), str(node.left.key)]})
                if node.left.key > largest.key:
                    largest = node.left
            if node.right:
                steps.append({"action": "compare", "nodes": [str(node.key), str(node.right.key)]})
                if node.right.key > largest.key:
                    largest = node.right

            if largest == node:
            # No swap needed, stop
                break

            steps.append({"action": "swap", "nodes": [str(node.key), str(largest.key)]})
            node.key, largest.key = largest.key, node.key
            node = largest

        if node:
            steps.append({"action": "highlight", "node": str(node.key)})
        return steps


    def find_node(self, key):
        for n in list(self.Q.queue):
            if str(n.key) == str(key):
                return n
        return None


    
    def heapify_up(self, node):
        steps = []
        while node.parent and node.key > node.parent.key:  # max-heap
            steps.append({"action": "compare", "nodes": [str(node.key), str(node.parent.key)]})
            steps.append({"action": "swap", "nodes": [str(node.key), str(node.parent.key)]})

            # Swap keys
            node.key, node.parent.key = node.parent.key, node.key

            node = node.parent

        steps.append({"action": "highlight", "node": str(node.key)})
        return steps


    def preorder_traversal(self):
        result = []
        def _preorder(node):
            if node is None:
                return
            result.append(node.key)
            _preorder(node.left)
            _preorder(node.right)

        _preorder(self.root)
        return result

    def postorder_traversal(self):
        result = []
        def _postorder(node):
            if node is None:
                return
            _postorder(node.left)
            _postorder(node.right)
            result.append(node.key) 

        _postorder(self.root)
        return result 

    def inorder_traversal(self):
        result = []
        def _inorder(node):
            if node is None:
                return
            _inorder(node.left)
            result.append(node.key) 
            _inorder(node.right)

        _inorder(self.root)
        return result 
        

    def print_heap(self):
        result = []
        def _print(node):
            if node is None: 
                return
            result.append(node.key) 
            _print(node.left)
            _print(node.right)
        _print(self.root)
        print("Current Heap is: ", result)

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
            "key": str(node.key),
            "children": children
        }

pq = MaxHeap()
#print(pq.node_count())
##
#pq.insert(1)
#pq.insert(2)
#steps =  pq.heapify_up(pq.find_node(2))
#print("HeapifyUp steps:", steps)
#print(pq.node_count())
#pq.insert(3)
#steps = pq.heapify_up(pq.find_node(3))
#print("HeapifyUp steps:", steps)
#pq.insert(10)
#pq.heapify_up(pq.find_node(10))

#print("HeapifyUp steps:", steps)


#pq.insert(5)
#pq.heapify_up(pq.find_node(5))
#pq.insert(6)
#pq.heapify_up(pq.find_node(6))
#pq.insert(7)
#pq.heapify_up(pq.find_node(7))
#print(pq.node_count())
#pq.insert(8)
#pq.heapify_up(pq.find_node(8))
#pq.insert(4)
#pq.heapify_up(pq.find_node(4))
#pq.insert(9)
#pq.heapify_up(pq.find_node(9))
#pq.print_heap()
#print(pq.node_count())
#pq.reset_heap()

#pq.insert(9)
#pq.heapify_up(pq.find_node(9))
#pq.insert(4)
#pq.heapify_up(pq.find_node(4))
#pq.insert(8)
#pq.heapify_up(pq.find_node(8))
#pq.print_heap()
#print("deleted: ", deleted)

#print("Preorder traversal: ", pq.preorder_traversal())
#print("Inorder traversal: ", pq.inorder_traversal())
#print("Postorder traversal: ", pq.postorder_traversal())
 
#print(pq.to_dict())


#print("The root after insertion: ", pq.root.key)


#deleted = pq.delete_root()
#pq.heapify_down()
#print("Deleted root:", deleted)
#pq.print_heap()
#pq.print_heap()
#print("Number of elements = ", pq.count)
