import tkinter as tk
from tkinter import ttk
from binary_tree_class import Node
from binary_tree_class import BinaryTree 
import time
import math
from tkinter import scrolledtext
from tkinter import messagebox as mb 
from array import array
import os
import fitz
from PIL import Image, ImageTk



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Radom Binary Tree Animation")
        self.geometry("800x850")
        
        self.widgets = BTApps(self)

        self.mainloop() 


class BTApps:
    def __init__(self, parent):

        self.parent = parent 
        self.parent.title("Random Binary Tree Visualizer")

        # Define constants
        self.node_radius = 20
        self.level_gap = 70
        self.h_gap = 40

        self.create_widgets() 

        # Keep canvas display frame open 
        self.canvas_display_frame.pack(padx=10, pady=(50,75), fill=tk.BOTH,
                expand=True)

        self.tree = BinaryTree() # Create an instance of binary tree 

        # Default display for explanation of animation
        self.execute_home()

    # Create widgets for the program to be functional enough
    # for playing with tree operations and traversals
    def create_widgets(self):

        self.bg_color = '#383839'
        self.head_frame = tk.Frame(self.parent, bg=self.bg_color, 
                highlightbackground='white', highlightthickness=1)

        # Header frame will embed title and short title
        self.head_frame = tk.Frame(self.parent, bg=self.bg_color, 
                highlightbackground='white', highlightthickness=1)
        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.configure(height=50)


        # Defines header title bar
        self.title_lb = tk.Label(self.head_frame, text='Data structure:', 
                bg=self.bg_color, fg='white', font=('Bold', 20))
        self.title_lb.pack(side=tk.LEFT)

        self.subtitle_lb = tk.Label(self.head_frame, text='Binary Tree Animation', 
                bg=self.bg_color, fg='white', font=('Regular', 15))
        self.subtitle_lb.place(relx=0.35, rely=0.2)


        # Menu specification in a separate BottomMenu class 
        self.bottom_menu = BottomMenu(self.parent, self)

        # Define canvas frame and canvas
        self.canvas_display_frame = tk.Frame(self.parent)
        self.canvas = tk.Canvas(self.canvas_display_frame, bg="white")


        # Create a frame to hold canvas and scrollbars 
        canvas_scroll_frame = tk.Frame(self.canvas_display_frame)
        canvas_scroll_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas inside the scroll frame
        self.canvas = tk.Canvas(canvas_scroll_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create text label for display messages on Canvas 
        self.canvas_label = tk.Label(self.canvas, text="", font=('Bold', 15), 
                bg="white", fg="blue") 

        # Vertical scrollbar next to canvas
        self.v_scrollbar = ttk.Scrollbar(canvas_scroll_frame, 
                                         orient=tk.VERTICAL, 
                                         command=self.canvas.yview)

        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Horizontal scrollbar below the canvas
        self.h_scrollbar = ttk.Scrollbar(self.canvas_display_frame, 
                                         orient=tk.HORIZONTAL, 
                                         command=self.canvas.xview)

        self.h_scrollbar.pack(fill=tk.X)

        # Connect scrollbars to canvas
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, 
                              xscrollcommand=self.h_scrollbar.set)


        # Text Widget (correct placement inside viewing window)
        self.text_widget = scrolledtext.ScrolledText(self.parent, 
                                                     wrap=tk.WORD,
                                                     width=75, height=10)


        self.close_btn = tk.Button(self.parent, text="Close", bg="#383839", 
                                   fg="white", activebackground="#383839", 
                                   activeforeground="white", font=('Bold', 15), 
                                   command=lambda: self.close_current_view)

         # Home button takes user to description of animation
        self.home_btn = tk.Button(self.parent, text="Home", bg="#383839", 
                                  fg="white", activebackground="#383839", 
                                  activeforeground="white", font=('Bold', 15), 
                                  command=lambda: self.open_pdf("Home"))

    # Sets up menu bottons and entry feilds for animation
    def setup_animation_ui(self, var):

        # Erase the earlier instance of the buttons
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()
        if self.home_btn.winfo_ismapped():
            self.home_btn.place_forget()

        # Canvas frame remains visible, don’t forget it
        # Only reset the input frame
        self.bottom_menu.input_frame.pack_forget()
        self.bottom_menu.input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Configure inputs according to push operation 
        if var == "Create": 
            self.bottom_menu.show_single_input("Create")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.generate_tree()
            )

        # Configure traversal buttons
        elif var == "Preorder":
            self.bottom_menu.show_no_input("Preorder")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_preorder()
            )

        elif var == "Postorder":
            self.bottom_menu.show_no_input("Postorder")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_postorder() 
            )

        elif var == "Inorder":
            self.bottom_menu.show_no_input("Inorder")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_inorder()
            )

        self.parent.update_idletasks()

    # Label lets creation of expressive message describing the result 
    def add_label(self, text): 

        self.canvas_label.config(text=text)

        self.canvas_label.place(relx=0.5, # Adjusted placement at center
                                rely=0.9, 
                                anchor=tk.CENTER) 

    def animate_creation(self, values, delay=800):

        # Initially create an empty binary tree
        self.tree.makenull()

        # Insert the nodes one by one
        def insert_next(i=0):
            if i >= len(values):
                return
            val = values[i]
            self.tree.insert_random(val)

            # redraw tree after each insertion
            self.clear_canvas()
            self.assign_positions(self.tree.root, 400, 50, 200)
            self.draw_tree(self.tree.root) # Draw tree after each insertion

            # schedule next insertion using Tkinter's event loop
            self.canvas.after(delay, lambda: insert_next(i+1))

        insert_next() # Initiate recursive call to insert nodes


    # Clear contents before displaying new fields, text, buttons, etc.
    def clear_main_content_area(self):
        '''Hides main content widgets, input fields, and specific 
           labels/buttons.'''

        if self.text_widget.winfo_ismapped():
            self.text_widget.pack_forget()
        
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()

    # Hides input frame and its buttons
    def hide_input_frame(self):

        if self.entry.winfo_ismapped():
            self.entry.grid_forget()

        if self.txt_label.winfo_ismapped():
            self.txt_label.grid_forget()

    # Shows input frame 
    def show_input_frame(self):

        self.input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)


#--------------- User Input --------------------------

    def accept_user_input(self):
        # Get and validate user's input
        user_input = self.bottom_menu.data_entry1.get()

        if not user_input.isnumeric():
            self.add_label("Invalid input: Enter a number") 

            # Input is invalid
            return -1

        # Get integer value
        return int(user_input)


    def generate_tree(self):
        self.clear_canvas()
        self.add_label("")

        try:
            n = self.accept_user_input() 
            if n == -1:
                return

        except ValueError:
            n = 10

        self.bottom_menu.data_entry1.delete(0, tk.END) 

        values = self.tree.generate_list(n)   # <-- now backend accepts n
        self.animate_creation(values)


    def clear_canvas(self):
        self.canvas.delete("all")

    def highlight_ring(self, node, color="orange"):
        ring = self.canvas.create_oval(
            node.x - self.node_radius - 5, node.y - self.node_radius - 5,
            node.x + self.node_radius + 5, node.y + self.node_radius + 5,
            outline="orange", width=2
        )
        # Remove ring after short delay
        self.canvas.after(800, lambda: self.canvas.delete(ring))

    # Generic animation for tree traversal 
    def animate_traversal(self, order_list, color="blue", label="Traversal"):
        if not order_list:
            self.add_label(f"{label}: Tree is empty")
            return

        # Outline ring for focusing on currently visited node 
        ring = self.canvas.create_oval(0, 0, 0, 0, outline=color, width=2)

        # Create a list of strings for traversal list
        traversal_values = [str(node.data) for node in order_list]

        # Visit the next node in the traversal list 
        def visit_next(i=0):
            if i >= len(order_list):
                self.canvas.delete(ring)

                # Place the node in a text string 
                self.add_label(f"{label}: {' → '.join(traversal_values)}")
                return

            node = order_list[i]
            self.add_label(f"Visiting: {node.data}")   # value = data live log update

            # Target coords for ring
            x1 = node.x - self.node_radius - 5
            y1 = node.y - self.node_radius - 5
            x2 = node.x + self.node_radius + 5
            y2 = node.y + self.node_radius + 5

            # The callback function for ring to glide on tree branch
            def after_glide():
                # Use highlighted ring for visited node in traversal order 
                self.canvas.after(50, lambda: self.highlight_ring(node, color)) 
                self.canvas.after(800, lambda: visit_next(i+1))


            # Smooth glide to node, then run after_glide
            self._glide_ring(ring, x1, y1, x2, y2, callback=after_glide)

        visit_next()


    # Glide function 
    def _glide_ring(self, ring, target_x1, target_y1, 
                    target_x2, target_y2, callback, steps=20):
        
        #Smoothly glide ring to target coords in given steps.
        current = self.canvas.coords(ring)
        if not current or current == [0, 0, 0, 0]:
            current = [target_x1, target_y1, target_x2, target_y2]

        dx1 = (target_x1 - current[0]) / steps
        dy1 = (target_y1 - current[1]) / steps
        dx2 = (target_x2 - current[2]) / steps
        dy2 = (target_y2 - current[3]) / steps

        def step(n=0, x1=current[0], y1=current[1], 
                 x2=current[2], y2=current[3]):
            if n >= steps:
                self.canvas.coords(ring, target_x1, target_y1, 
                                   target_x2, target_y2)
                callback()   # run explicit callback
                return
            self.canvas.coords(ring, x1 + dx1, y1 + dy1, x2 + dx2, y2 + dy2)
            self.canvas.after(30, lambda: step(n+1, x1+dx1, y1+dy1,
                                               x2+dx2, y2+dy2))

        step()

    # --- Specific tree traversals are wrappers over animate_traveral  ---

    def animate_preorder(self):
        self.animate_traversal(self.tree.preorder_traversal(), color="purple", 
                               label="Preorder")

    def animate_inorder(self):
        self.animate_traversal(self.tree.inorder_traversal(), color="green",
                               label="Inorder")

    def animate_postorder(self):
        self.animate_traversal(self.tree.postorder_traversal(), color="blue", 
                               label="Postorder")

 
    # Calculates the position of a node
    def assign_positions(self, node, x, y, dx):
        if node is None:
            return
        node.x, node.y = x, y
        if node.left:
            self.assign_positions(node.left, x - dx, y + self.level_gap, dx // 2)
        if node.right:
            self.assign_positions(node.right, x + dx, y + self.level_gap, dx // 2)
    def draw_tree(self, node):
        if node is None:
            return
        if node.left:
            self.canvas.create_line(node.x, node.y, node.left.x, node.left.y, width=2)
            self.draw_tree(node.left)
        if node.right:
            self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, width=2)
            self.draw_tree(node.right)
        self.draw_node(node)

    def draw_node(self, node):
        x, y = node.x, node.y
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill="skyblue")
        self.canvas.create_text(x, y, text=str(node.data), font=("Arial", 12, "bold"))


    # Opens PDF viewer  
    def open_pdf(self, fx):
        self.clear_main_content_area() # Hide other content first

        # Make the canvas frame visible for PDF display
        self.canvas_display_frame.pack(padx=10, pady=(10,75), 
                                       fill=tk.BOTH, 
                                       expand=True) # pady bottom for close_btn

        self.canvas.delete("all") # Clear previous canvas content

        file_name = ""
        if fx == "Home": file_name = "explanation.pdf"
        elif fx == "Linked list": file_name = "linked_list_description.pdf"
        else:
            self.canvas.create_text(self.canvas.winfo_width()/2, 
                    self.canvas.winfo_height()/2,
                    text=f"PDF definition for '{fx}' not found.", 
                    anchor=tk.CENTER)
            return

        if not os.path.exists(file_name):
            self.canvas.create_text(self.canvas.winfo_width()/2, 
                    self.canvas.winfo_height()/2,
                    text=f"File not found: {file_name}", anchor=tk.CENTER)
            return

        try:
            doc = fitz.open(file_name)
            page_images_pil = []
            total_height = 0
            max_width = 0
            page_padding = 5 # Pixels between pages

            if len(doc) == 0:
                self.canvas.create_text(self.canvas.winfo_width()/2, 
                        self.canvas.winfo_height()/2,
                        text="PDF is empty.", anchor=tk.CENTER)
                doc.close()
                return

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)

                # Adjust zoom_factor = 1.0 for 72 DPI (1 PDF point = 1 pixel)
                # zoom_factor = 1.33 for ~96 DPI (often better for screen)
                zoom_factor = 1.33

                mat = fitz.Matrix(zoom_factor, zoom_factor)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                
                img_pil = Image.frombytes("RGB", [pix.width, pix.height], 
                        pix.samples)
                page_images_pil.append(img_pil)
                
                total_height += img_pil.height
                if page_num < len(doc) - 1: # Padding for all but the last page
                    total_height += page_padding
                if img_pil.width > max_width:
                    max_width = img_pil.width
            doc.close()

            if not page_images_pil: 
                return

            # Store PIL image as an instance variable to keep it in memory
            self.pdf_composite_image_pil = Image.new("RGB", 
                    (max_width, total_height), "white")
            current_y = 0
            for img_pil in page_images_pil:
                self.pdf_composite_image_pil.paste(img_pil, (0, current_y))
                current_y += img_pil.height + page_padding
            
            # Store PhotoImage as an instance variable
            self.pdf_image_tk = ImageTk.PhotoImage(self.pdf_composite_image_pil)
            
            self.canvas.create_image(0, 0, anchor=tk.NW, 
                    image=self.pdf_image_tk)
            self.canvas.config(scrollregion=(0, 0, max_width, total_height))

        except Exception as e:
            self.canvas.delete("all")
            self.canvas.create_text(self.canvas.winfo_width()/2, 
                    self.canvas.winfo_height()/2,
                    text=f"Error opening PDF '{file_name}':\n{e}", 
                    anchor=tk.CENTER, justify=tk.CENTER)
        
        self.close_btn.place(relx=0.5, rely=0.95, anchor=tk.S) 
        # Place close button at the bottom


    # In execute_home, if it opens a PDF
    def execute_home(self):
        self.clear_main_content_area()

        self.open_pdf("Home") # It will use the scrollable PDF viewer
        self.close_btn.configure(command=self.close_current_view)

    def close_current_view(self):
        # Clears the current view (PDF, Text, Animation Input/Setup) and 
        # associated resources.
        
        # Clear canvas
        self.clear_main_content_area() 

        # Clear PDF specific resources if they exist
        if hasattr(self, 'pdf_image_tk'):
            del self.pdf_image_tk
        if hasattr(self, 'pdf_composite_image_pil'):
            del self.pdf_composite_image_pil
        
        # Reset canvas scrollregion if it was set for PDF
        self.canvas.config(scrollregion=(0,0, self.canvas.winfo_width(), 
            self.canvas.winfo_height()))

        # Hide main action button and close button
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()


class BottomMenu:

    def __init__(self, parent, widgets):
        self.parent = parent
        self.widgets = widgets
        self.create_menu()

    def create_menu(self):
        # --- Footer container ---
        self.bg_color = "#383839"
        self.footer_frame = tk.Frame(self.parent)
        self.footer_frame.pack(side="top", fill="x")


        # --- Input frame (fixed height row above bottom menu) ---
        self.input_frame = tk.Frame(self.footer_frame, height=40)
        self.input_frame.pack(side="top", fill=tk.X)
        self.input_frame.pack_propagate(False)   # keep 40px height even if empt        
        # --- Bottom menu frame (second row) ---
        self.bottom_menu_frame = tk.Frame(self.footer_frame, height=40)
        self.bottom_menu_frame.pack(side="bottom", fill=tk.X)
        self.bottom_menu_frame.pack_propagate(False)

        # Input widgets (created once, packed later in show_* methods)
        
        self.data_entry1 = tk.Entry(self.input_frame, width=20)

        self.txt_label1 = tk.Label(self.input_frame, text="Enter value", 
                font=('Regular', 15))

        self.setup_btn = tk.Button(self.input_frame, text="", 
                font=('Regular', 15), bg=self.bg_color, fg="white", 
                activebackground=self.bg_color, activeforeground="white" )



        # Dropdowns in bottom menu
        self.btree_var = tk.StringVar()
        btree_ops = ttk.OptionMenu(self.bottom_menu_frame, self.btree_var, 
                "Tree Ops")
        btree_ops.pack(side="left", padx=10, pady=5)
        btree_ops["menu"].add_command(label="Create", 
                command=lambda: self.widgets.setup_animation_ui("Create"))

        self.traversal_var = tk.StringVar()
        traversal_ops = ttk.OptionMenu(self.bottom_menu_frame, self.traversal_var, 
                "Traverse")
        traversal_ops.pack(side="left", padx=10, pady=5)
        traversal_ops["menu"].add_command(label="Preorder", 
                command=lambda: self.widgets.setup_animation_ui("Preorder"))
        traversal_ops["menu"].add_command(label="Inorder", 
                command=lambda: self.widgets.setup_animation_ui("Inorder"))
        traversal_ops["menu"].add_command(label="Postorder", 
                command=lambda: self.widgets.setup_animation_ui("Postorder"))


    # --- Public API methods ---
    def clear_inputs(self):
        """Hide input frame and all input widgets."""
        for widget in (self.txt_label1, self.data_entry1,
                       self.setup_btn): widget.pack_forget()


    def show_single_input(self, var, label_text="Enter value 1-15"):
        # Show only one input field + setup button.
        self.clear_inputs()
        self.txt_label1.config(text=label_text)
        self.txt_label1.pack(side="left", padx=5, pady=5)
        self.data_entry1.pack(side="left", padx=5, pady=5)
        

        if var == "Create":
            self.setup_btn.configure(text="Create")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        else:
            self.add_label("Invalid operation")

    def show_no_input(self, var):
        # Show only setup button (no input required).
        self.clear_inputs()
        if var == "Preorder":
            self.setup_btn.configure(text="Preorder")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var == "Inorder":
            self.setup_btn.configure(text="Inorder")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var=="Postorder":
            self.setup_btn.configure(text="Postorder")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        else:
            self.add_label("Invalid operation")


if __name__ == "__main__":

    App() 


