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


    def pulsate(self, item_id, x_center, y_center, pulses=6, callback=None):
        """Make a canvas item pulsate (grow/shrink) around its center."""
        def _pulse(count=0):
            if count < pulses:
                scale = 1.1 if count % 2 == 0 else 0.9
                self.canvas.scale(item_id, x_center, y_center, scale, scale)
                self.canvas.after(100, lambda: _pulse(count + 1))
            else:
                if callback:
                    callback()
        _pulse()


    def _get_depth(self, node):
        """Helper to compute depth of tree."""
        if node is None:
            return 0
        return 1 + max(self._get_depth(node.left), self._get_depth(node.right))

    def insert(self, value):
        # Center root horizontally
        canvas_width = self.canvas.winfo_width()
        root_x = canvas_width // 2
        root_y = 50

        # Compute max depth of current tree
        max_depth = self._get_depth(self.root)

        # Dynamic horizontal spacing: shrink as depth grows
        initial_dx = max(canvas_width // (2 ** (max_depth + 1)), self.node_radius * 2)

        # Perform insertion
        self.root = self._insert(self.root, value, root_x, root_y, initial_dx)

        # Redraw updated tree
        self.redraw()

    def delete(self, value):
        if self.find(value):
            self.root = self._delete(self.root, value)
            return True
        return False



    # Check if delete is successful?
    '''def delete(self, value):
        if self.find(value):
            self.root = self._delete(self.root, value)
            self.redraw()
            return True
        else:
            return False'''

    def find(self, value):
        return self._find(self.root, value)


    def _insert(self, node, value, x, y, dx):
        """Recursive insertion with clamped coordinates."""
        if node is None:
            # Clamp x so node stays inside canvas
            x = max(self.node_radius, min(self.canvas.winfo_width() - self.node_radius, x))
            return TreeNode(value, x, y)

        if value < node.value:
            node.left = self._insert(node.left, value, x - dx, y + self.level_gap, dx // 2)
        elif value > node.value:
            node.right = self._insert(node.right, value, x + dx, y + self.level_gap, dx // 2)
        return node

    def assign_positions(self, node, x, y, dx):
        """Assign positions recursively, centered around parent."""
        if node is None:
            return

        node.x, node.y = x, y

        # Left child: shift left from parent
        if node.left:
            self.assign_positions(node.left, x - dx, y + self.level_gap, dx // 2)

        # Right child: shift right from parent
        if node.right:
            self.assign_positions(node.right, x + dx, y + self.level_gap, dx // 2)




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
          
    def find_node(self, value):
        """Return the node object with given value, or None if not found."""
        return self._find_node(self.root, value)

    def _find_node(self, node, value):
        if node is None:
            return None
        if value == node.value:
            return node
        elif value < node.value:
            return self._find_node(node.left, value)
        else:
            return self._find_node(node.right, value)


    def _get_min(self, node):
        while node.left:
            node = node.left
        return node

    def redraw(self):
        self.canvas.delete("all")
        if self.root:
            canvas_width = self.canvas.winfo_width()
            root_x = canvas_width // 2
            root_y = 50
            initial_dx = canvas_width // 4   # generous spacing for first level
            self.assign_positions(self.root, root_x, root_y, initial_dx)
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
        tag = f"node_{node.value}" # Create unique tag

        oval_id = self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill="skyblue", tags = (tag,))

        self.canvas.create_text(x, y, text=str(node.value),
                        font=("Arial", 12, "bold"),
                        tags=(tag,))
        


    def get_item_by_tag(self, tag):
        items = self.canvas.find_withtag(tag)
        if items:
            return items[0]  # Return the first matching item
        return None  # If no item found

    def repaint_oval(self, tag, new_color):
        items = self.canvas.find_withtag(tag)
        for item in items:
            self.canvas.itemconfig(item, fill=new_color)

    def _draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, width=2)

    def pre_list(self):
        return self._pre_list(self.root)

    def _pre_list(self, node):
        if node is None:
            return []
        return [node] + self._pre_list(node.left) + self._pre_list(node.right)

    def post_list(self):
        return self._post_list(self.root)

    def _post_list(self, node):
        if node is None:
            return []
        return self._post_list(node.left) + self._post_list(node.right) + [node]

    def in_list(self):
        return self._in_list(self.root)

    def _in_list(self, node):
        if node is None:
            return []
        return self._in_list(node.left) + [node] + self._in_list(node.right)
 

    def pulsate(self, item_id, x_center, y_center, pulses=6, callback=None):
        """Make a canvas item pulsate (grow/shrink) around its center."""
        def _pulse(count=0):
            if count < pulses:
                scale = 1.1 if count % 2 == 0 else 0.9
                self.canvas.scale(item_id, x_center, y_center, scale, scale)
                self.canvas.after(100, lambda: _pulse(count + 1))
            else:
                if callback:
                    callback()
        _pulse()
    
    def _find_min(self, node):
        while node.left:
            node = node.left
        return node
    

