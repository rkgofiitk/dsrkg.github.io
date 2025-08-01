class TreeNode:
    def __init__(self, value, x=0, y=0):
        self.value = value
        self.left = None
        self.right = None
        self.x = x
        self.y = y


class BSTVisualizer:
    def __init__(self, canvas):
        self.canvas = canvas
        canvas.delete("all")
        self.root = None
        self.node_radius = 20
        self.level_gap = 70
        self.h_gap = 30
        self.animation_speed = 10  # pixels per frame

    def insert(self, value):
        self.root = self._insert(self.root, value, 400, 50, 200)
        self.redraw()

    def delete(self, value):
        self.root = self._delete(self.root, value)
        self.redraw()

    def find(self, value):
        return self._find(self.root, value)

    def _insert(self, node, value, x, y, dx):
        if node is None:
            return TreeNode(value, x, y)
        if value < node.value:
            node.left = self._insert(node.left, value, x - dx, y + self.level_gap, dx // 2)
        elif value > node.value:
            node.right = self._insert(node.right, value, x + dx, y + self.level_gap, dx // 2)
        return node

    def _delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            min_larger_node = self._get_min(node.right)
            node.value = min_larger_node.value
            node.right = self._delete(node.right, min_larger_node.value)
        return node


    def _find(self, node, value):
        if node is None:
            print("Traced not found path")
            return False 
        if value == node.value:
            print("Traced found path")
            return True
        if value < node.value:
            return self._find(node.left, value)
        else:
            return self._find(node.right, value)
          


    def _get_min(self, node):
        while node.left:
            node = node.left
        return node

    def redraw(self):
        self.canvas.delete("all")
        if self.root:
            self._draw_tree(self.root)

    def _draw_tree(self, node):
        if node.left:
            self._draw_line(node.x, node.y, node.left.x, node.left.y)
            self._draw_tree(node.left)
        if node.right:
            self._draw_line(node.x, node.y, node.right.x, node.right.y)
            self._draw_tree(node.right)
        self._draw_node(node)

    def _draw_node(self, node):
        x, y = node.x, node.y
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill="skyblue")
        self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 12, "bold"))

    def _draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, width=2)

    def pre_list(self):
        return self._pre_list(self.root)

    def _pre_list(self, node):
        if node is None:
            return []
        return [node.value] + self._pre_list(node.left) + self._pre_list(node.right)

    def post_list(self):
        return self._post_list(self.root)

    def _post_list(self, node):
        if node is None:
            return []
        return self._post_list(node.left) + self._post_list(node.right) + [node.value]

    def in_list(self):
        return self._in_list(self.root)

    def _in_list(self, node):
        if node is None:
            return []
        return self._in_list(node.left) + [node.value] + self._in_list(node.right) 
