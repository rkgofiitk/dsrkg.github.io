import tkinter as tk
from tkinter import ttk
from bst_class import TreeNode 
from bst_class import BSTVisualizer
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
        self.title("Insertion Sort Animation")
        self.geometry("750x750") # Display window

        self.delay = 10 # Default value
        self.widgets = BSTApp(self) # Instance of widget class

        self.mainloop() 


class BSTApp:
    def __init__(self, parent):

        self.parent = parent 
        self.parent.title("Binary Search Tree Visualizer")
        self.toggle_menu_frame = None

        self.create_widgets()

        # Keep canvas display frame open for BSTVisualizer
        self.canvas_display_frame.pack(padx=10, pady=(50,75), fill=tk.BOTH,
                expand=True)

        self.bst = BSTVisualizer(self.canvas) # Create an instance of visualizer

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

        self.subtitle_lb = tk.Label(self.head_frame, text='BST Animation', 
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


    # Sets the menu bottons and entry feilds
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
        if var == "Insert": 
            self.bottom_menu.show_single_input("Insert")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_insert()
            )

        # Configure pop button
        elif var == "Delete":
            self.bottom_menu.show_single_input("Delete")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_delete()
            )

        # Configure search button
        elif var == "Search":
            self.bottom_menu.show_single_input("Search")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_search() 
            )

        # Configure inputs according to traversal order 
        elif var == "Preorder":
            self.bottom_menu.show_no_input("Preorder")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_preorder()
            )

        # Configure interorder button
        elif var == "Inorder":
            self.bottom_menu.show_no_input("Inorder")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_inorder()
            )

        # Configure postorder button
        elif var == "Postorder":
            self.bottom_menu.show_no_input("Postorder")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_postorder() 
            )

        self.parent.update_idletasks()



    def execute_operation(self):
        self.close_current_view()
        self.hide_input_frame()

        self.txt_label.grid(row=0,column=0, padx=5, pady=5)
        self.entry.grid(row=0,column=1, padx=5, pady=5)

        self.show_input_frame()

    def execute_redraw(self):
        self.clear_main_content_area()
        self.hide_input_frame()
        self.add_label("")
        self.bst.redraw()

    def tree_traversal(self,type):
        self.clear_main_content_area()
        self.bst.redraw()
        if type == "Preorder":
            txt = str(self.bst.pre_list())
            self.add_label(txt)
        elif type == "Inorder":
            txt = str(self.bst.in_list())
            self.add_label(txt)
        elif type == "Postorder":
            txt = str(self.bst.post_list())
            self.add_label(txt)
        else:
            txt = "Undefined traversal type"
            self.add_label(txt)
        

    def highlight_node(self, x, y, radius=25, color="yellow", duration=500):
        glow = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            outline=color, width=3
        )
        self.canvas.after(duration, lambda: self.canvas.delete(glow))



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

        if self.insert_btn.winfo_ismapped():
            self.insert_btn.grid_forget()

        if self.delete_btn.winfo_ismapped():
            self.delete_btn.grid_forget()

        if self.search_btn.winfo_ismapped():
            self.search_btn.grid_forget()


    # Shows input frame 
    def show_input_frame(self):

        self.insert_btn.grid(row=0,column=2, padx=5, pady=5)
        self.delete_btn.grid(row=0,column=3, padx=5, pady=5)
        self.search_btn.grid(row=0,column=4, padx=5, pady=5)

        self.input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)


#--------------- Animation Helpers--------------------------

    def accept_user_input(self):
        # Get and validate user's input
        user_input = self.bottom_menu.data_entry1.get()

        if not user_input.isnumeric():
            self.execute_status_message("Invalid input: Enter a number", 
                                        350, 500, color="red")
            # Input is invalid
            return -1

        # Get integer value
        return int(user_input)



    def move_along_branch(self, oval_id, text_id, x1, y1, x2, y2, callback):
        """Animate both oval and text together."""
        steps = 20
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps

        def step(i=0):
            if i < steps:
                self.canvas.move(oval_id, dx, dy)
                self.canvas.move(text_id, dx, dy)
                self.canvas.after(30, lambda: step(i+1))
            else:
                callback()

        step()

    def compare_pause(self, node, oval_id, text_id, callback):
        dest_x, dest_y = node.x, node.y - 30
        coords = self.canvas.coords(oval_id)
        x1, y1 = coords[0], coords[1]
        self.move_along_branch(oval_id, text_id, x1, y1, dest_x, dest_y,
                               lambda: self.canvas.after(500, callback))


    def highlight_ring(self, node, color="orange"):
        ring = self.canvas.create_oval(
            node.x - self.bst.node_radius - 5, node.y - self.bst.node_radius - 5,
            node.x + self.bst.node_radius + 5, node.y + self.bst.node_radius + 5,
            outline="orange", width=2
        )
        # Remove ring after short delay
        self.canvas.after(500, lambda: self.canvas.delete(ring))


    def traverse(self, node, value, oval_id, text_id, dx, settle_callback, 
                 compare_callback=None):
        """
        Generic traversal for BST animations.
        - node: current BST node
        - value: target value
        - oval_id, text_id: temp oval + text IDs
        - dx: horizontal spacing
        - settle_callback: called when traversal ends or finds target
        - compare_callback: optional effect at each comparison (e.g., pulsating ring)
    """
        if node is None:
            coords = self.canvas.coords(oval_id)
            cx = (coords[0] + coords[2]) / 2
            cy = (coords[1] + coords[3]) / 2
            self.bst.pulsate(oval_id, cx, cy, pulses=6,
                             callback=lambda: settle_callback(node, cx, cy))
            return

        def after_pause():
            if compare_callback:
                compare_callback(node)  # e.g., highlight ring
            self.move_along_branch(oval_id, text_id,
                                   *self.canvas.coords(oval_id)[:2],
                                   node.x, node.y,
                                   lambda: (
                                       settle_callback(node, node.x, node.y) if node.value == value else
                                       self.traverse(node.left if value < node.value else node.right,
                                                     value, oval_id, text_id, dx // 2,
                                                     settle_callback, compare_callback)
                                   ))

        self.compare_pause(node, oval_id, text_id, after_pause)




#-------------------------- Animate Insert ---------------------------------

    def animate_insert(self):
        value = self.accept_user_input()
        if value == -1:
            return

        temp_node = self.canvas.create_oval(10, 10, 50, 50, fill="yellow")
        temp_text = self.canvas.create_text(30, 30, text=str(value),
                                            font=("Arial", 12, "bold"))

        def settle_insert(node, x, y):
            self.bst.insert(value)
            self.bst.redraw()
            self.add_label(f"Successfully inserted {value}")

        if self.bst.root:
            self.traverse(self.bst.root, value, temp_node, temp_text,
                          self.canvas.winfo_width() // 4,
                          settle_insert,
                          compare_callback=lambda n: self.highlight_ring(n, "orange"))
        else:
            root_x = self.canvas.winfo_width() // 2
            root_y = 50
            self.move_along_branch(temp_node, temp_text, 10, 10, root_x, root_y,
                                   lambda: settle_insert(None, root_x, root_y))


#-------------------- Animate Delete ---------------------

    def animate_delete(self):
        value = self.accept_user_input()
        if value == -1:
            return

        # Create temporary yellow node + text at top-left
        temp_node = self.canvas.create_oval(10, 10, 50, 50, fill="yellow")
        temp_text = self.canvas.create_text(30, 30, text=str(value),
                                            font=("Arial", 12, "bold"))

        def settle_delete(node, x, y):
            if node is None:
                self.add_label(f"Delete failed: {value} not found")
                # Clean up temp node/text if not found
                self.canvas.delete(temp_node)
                self.canvas.delete(temp_text)
                return

            # Highlight target node with red ring
            ring = self.canvas.create_oval(
                node.x - self.bst.node_radius - 5, node.y - self.bst.node_radius - 5,
                node.x + self.bst.node_radius + 5, node.y + self.bst.node_radius + 5,
                outline="red", width=2
            )

            # Pulse temp node, then perform deletion
            self.bst.pulsate(temp_node, node.x, node.y, pulses=6,
                             callback=lambda: _perform_delete(node, ring))

        def _perform_delete(node, ring):
            # Remove highlight ring + temp node + text
            self.canvas.delete(ring)
            self.canvas.delete(temp_node)
            self.canvas.delete(temp_text)

            # Perform backend deletion and redraw
            self.bst.delete(value)
            self.bst.redraw()
            self.add_label(f"Deleted {value} successfully")

        # Start traversal from root using the shared helper
        if self.bst.root:
            self.traverse(self.bst.root, value, temp_node, temp_text,
                          self.canvas.winfo_width() // 4, settle_delete,
                          compare_callback=lambda n: self.highlight_ring(n, "orange"))


#---------------------------- Animate Search ---------------------------------

    def animate_search(self):


        value = self.accept_user_input()
        if value == -1:
            return

        # Create temporary yellow node + text at top-left
        temp_node = self.canvas.create_oval(10, 10, 50, 50, fill="yellow")
        temp_text = self.canvas.create_text(30, 30, text=str(value),
                                            font=("Arial", 12, "bold"))

        def settle_search(node, x, y):
            if node and node.value == value:
                self.add_label(f"Found {value}")
                # Green ring for success
                self.highlight_ring(node, color="green")
            else:
                self.add_label(f"{value} not found")
                # Clean up temp node/text if not found
            self.canvas.delete(temp_node)
            self.canvas.delete(temp_text)

        if self.bst.root:
            self.traverse(self.bst.root, value, temp_node, temp_text,
                          self.canvas.winfo_width() // 4,
                          settle_search,
                          compare_callback=lambda n: self.highlight_ring(n, "orange"))
        else:
            self.add_label("Tree is empty")
            self.canvas.delete(temp_node)
            self.canvas.delete(temp_text)



    # This is for search result label
    def add_label(self, text): 

        self.canvas_label.config(text=text)

        self.canvas_label.place(relx=0.5, # Adjusted placement
                                rely=0.9, 
                                anchor=tk.CENTER) 


    def find_value(self):
        try:

            value = int(self.entry.get())
            found = self.bst.find(value)
            if found:
                txt = f"{value} found"
                tag = f"node_{value}"
                items = self.canvas.find_withtag(tag)
                print(f"Items with tag '{tag}':", items)
                for item in items:
                    item_type = self.canvas.type(item)
                    if item_type == "oval":
                        #self.canvas.itemconfig(item, fill="blue")
                        coords = self.canvas.coords(item)  # returns [x1, y1, x2, y2]
                        x = (coords[0] + coords[2]) / 2
                        y = (coords[1] + coords[3]) / 2
                        self.highlight_node(x, y, radius=25, 
                                            color="blue", duration=500)
                    #elif item_type == "text":
                    #    self.canvas.itemconfig(item, fill="red")  

                self.add_label(txt) 
            else:
                txt = f"{value} not found"
                self.add_label(txt) 

            self.entry.delete(0,tk.END)
        except ValueError:
            pass

#-------------------- Animate tree traversals helper function ------------------


    def animate_traversal(self, order_list, color="blue", label="Traversal"):
        if not order_list:
            self.add_label(f"{label}: Tree is empty")
            return

        # Transparent ring
        ring = self.canvas.create_oval(0, 0, 0, 0, outline=color, width=2)

        traversal_values = [str(node.value) for node in order_list]

        # Visit the next node in the traversal order
        def visit_next(i=0):
            if i >= len(order_list):
                self.canvas.delete(ring)
                self.add_label(f"{label}: {' → '.join(traversal_values)}")
                return

            node = order_list[i]
            self.add_label(f"Visiting: {node.value}")   # live log update

            # Target coords for ring
            x1 = node.x - self.bst.node_radius - 5
            y1 = node.y - self.bst.node_radius - 5
            x2 = node.x + self.bst.node_radius + 5
            y2 = node.y + self.bst.node_radius + 5

            # The callback function for glide 
            def after_glide():
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

    # --- Actual tree traversals are wrappers over animate_traveral  ---

    def animate_preorder(self):
        self.animate_traversal(self.bst.pre_list(), color="purple", 
                               label="Preorder")

    def animate_inorder(self):
        self.animate_traversal(self.bst.in_list(), color="green",
                               label="Inorder")

    def animate_postorder(self):
        self.animate_traversal(self.bst.post_list(), color="blue", 
                               label="Postorder")


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

        self.bst.redraw()
        

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
        self.bst_var = tk.StringVar()
        bst_ops = ttk.OptionMenu(self.bottom_menu_frame, self.bst_var, 
                "BST Ops")
        bst_ops.pack(side="left", padx=10, pady=5)
        bst_ops["menu"].add_command(label="Insert", 
                command=lambda: self.widgets.setup_animation_ui("Insert"))
        bst_ops["menu"].add_command(label="Delete", 
                command=lambda: self.widgets.setup_animation_ui("Delete"))
        bst_ops["menu"].add_command(label="Search", 
                command=lambda: self.widgets.setup_animation_ui("Search"))

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


    def show_single_input(self, var, label_text="Enter value"):
        # Show only one input field + setup button.
        self.clear_inputs()
        self.txt_label1.config(text=label_text)
        self.txt_label1.pack(side="left", padx=5, pady=5)
        self.data_entry1.pack(side="left", padx=5, pady=5)
        if var == "Insert":
            self.setup_btn.configure(text="Insert")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var == "Delete":
            self.setup_btn.configure(text="Delete")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var == "Search":
            self.setup_btn.configure(text="Search")
            self.setup_btn.pack(side="left", padx=10, pady=5)


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

    def reset(self):
        #Clear inputs and reset dropdown selections.

        self.clear_inputs()
        self.single_var.set("Single Input Ops")
        self.no_var.set("No Input Ops")


if __name__ == "__main__":
    App()
