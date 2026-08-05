import tkinter as tk
from hash_class import Node, List, Hash 

import tkinter as ttk
from tkinter import messagebox
from tkinter import scrolledtext
import os
import fitz
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chained Hashing Visualizer")
        self.geometry("850x850")

        self.widgets = HashVisualizer(self)

        self.mainloop()

class HashVisualizer(tk.Tk):
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Hash Visualizer")
        self.create_widgets()
        
        self.node_radius = 20
        self.v_gap = 30
        self.h_gap = 20

        # Keep canvas display frame open 
        self.canvas_display_frame.pack(padx=10, pady=(50,75), fill=tk.BOTH,
                expand=True)

        self.hash_obj = Hash(size=10, capacity=20) #hash_obj

        self.execute_home()


    # Creates buttons and frames needed for the GUI
    def create_widgets(self):

        self.bg_color = '#383839'

        # Header frame will embed title and short title
        self.head_frame = tk.Frame(self.parent, bg=self.bg_color, 
                highlightbackground='white', highlightthickness=1)

        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.configure(height=50)


        # Defines header title bar
        self.title_lb = tk.Label(self.head_frame, text='Data structure:', 
                bg=self.bg_color, fg='white', font=('Bold', 20))
        self.title_lb.pack(side=tk.LEFT)

        self.subtitle_lb = tk.Label(self.head_frame, 
                                    text='Binary Tree Animation', 
                                    bg=self.bg_color, fg='white',
                                    font=('Regular', 15))

        self.subtitle_lb.place(relx=0.35, rely=0.2)


        # Menu specification in a separate BottomMenu class 
        self.bottom_menu = BottomMenu(self.parent, self, self)

        # Define canvas frame and the canvas
        self.canvas_display_frame = tk.Frame(self.parent)
        self.canvas = tk.Canvas(self.canvas_display_frame, bg="white")

        # Create a frame to hold scrollbars 
        canvas_scroll_frame = tk.Frame(self.canvas_display_frame)
        canvas_scroll_frame.pack(fill=tk.BOTH, expand=True)


        # Now place canvas inside the scroll frame
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


        # Close button for closing current view inside the canvas
        self.close_btn = tk.Button(self.parent, text="Close", bg="#383839", 
                                   fg="white", activebackground="#383839", 
                                   activeforeground="white", font=('Bold', 15), 
                                   command=lambda: self.close_current_view)

        # Home button takes user to description of animation
        self.home_btn = tk.Button(self.parent, text="Home", bg="#383839", 
                                  fg="white", activebackground="#383839", 
                                  activeforeground="white", font=('Bold', 15), 
                                  command=lambda: self.open_pdf("Home"))

    # In execute_home opens a PDF describing the animation
    def execute_home(self):
        self.clear_main_content_area()

        self.open_pdf("Home") # It will use the scrollable PDF viewer

        # Place the close button to close the PDF 
        self.close_btn.configure(command=self.close_current_view)


    # Clears the current view (PDF, Text, Animation Input/Setup). 
    def close_current_view(self):
        
        # Clear the canvas
        self.clear_main_content_area() 

        # Clear the PDF specific resources if they exist
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

    # Clears the content before displaying new fields, text, buttons, etc.
    def clear_main_content_area(self):

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


    def accept_key_input(self):
        user_input = self.bottom_menu.data_entry1.get()
        if not user_input.isnumeric():
           self.add_label("Invalid key: Enter a number", "red") 
           return -1
        return int(user_input)

    def accept_value_input(self):
        # Get and validate user's input
        user_input = self.bottom_menu.data_entry2.get()

        if not user_input.isnumeric(): #or not user_input2.isnumeric():
           self.add_label("Invalid value: Enter a number", "red") 
           return -1
        else:
            return int(user_input)


    def setup_animation_ui(self, var):
        
        # Erase the earlier instance of the buttons
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()
        if self.home_btn.winfo_ismapped():
            self.home_btn.place_forget()

        # Canvas frame remains visible, don’t forget it
        # Reset only the input frame 
        self.bottom_menu.input_frame.pack_forget()
        self.bottom_menu.input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Configure inputs according to push operation 
        if var == "Create": 
            self.bottom_menu.show_no_input("Create")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_creation()
            )
        elif var == "Avg length":
            self.bottom_menu.show_no_input("Avg length")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_avg_chain_length()
            )
        elif var == "Max length":
            self.bottom_menu.show_no_input("Max length")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_max_chain_length()
                )

        elif var == "Collisions":
            self.bottom_menu.show_no_input("Collisions")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_collision_count()
                )
        # Configure traversal buttons
        elif var == "Insert":
            self.bottom_menu.show_two_inputs("Insert")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.insert()
            )
        elif var == "Delete":
            self.bottom_menu.show_one_input("Delete")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.delete() 
            )
        elif var == "Search":
            self.bottom_menu.show_one_input("Search")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.search()
            )
        self.parent.update_idletasks()

    
    # Generic fade-out for any Tkinter widget with fg color.
    def fade_out_label(self, widget, color="blue", duration=2000, steps=10):
        try:
            # get 16-bit RGB values
            r, g, b = widget.winfo_rgb(color)
        except tk.TclError:
            # fallback if color string invalid
            r, g, b = widget.winfo_rgb("blue")

        # convert to 8-bit
        r, g, b = r // 256, g // 256, b // 256

        def fade(step=0):
            if step < steps:
                factor = 1 - (step / steps)
                rf = int(r * factor)
                gf = int(g * factor)
                bf = int(b * factor)
                faded = f"#{rf:02x}{gf:02x}{bf:02x}"
                widget.config(fg=faded)
                widget.after(duration // steps, lambda: fade(step+1))
            else:
                widget.place_forget()

        fade()
    

    # Adds message to canvas about the animation steps.
    def add_label(self, text, color="blue"):
        self.canvas_label.config(text=text, fg=color)
        self.canvas_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        self.fade_out_label(self.canvas_label, color=color, 
                            duration=2000, steps=10)

 
    # Animates creation of buckets
    def animate_creation(self, delay=800):
        self.bucket_width = 60
        self.bucket_height = 40
        self.node_radius = 20
        self.bucket_coords = []
        self.bucket_nodes = [[] for _ in range(self.hash_obj.size)]

        def create_bucket(i=0):
            if i < self.hash_obj.size:
                # horizontal row layout
                bx = 100 + i * 75   # x position for bucket center
                by = 100            # fixed y position for all buckets

                rect = self.canvas.create_rectangle(
                    bx - self.bucket_width//2,
                    by - self.bucket_height//2,
                    bx + self.bucket_width//2,
                    by + self.bucket_height//2,
                    outline="black", width=2, fill="white"
                )

                # draw text inside the rectangle
                self.canvas.create_text(bx, by, text=str(i), fill="black",
                                        font=("Arial", 12, "bold"))

                # store bucket center X and bottom Y
                b_bottom = by + self.bucket_height//2
                self.bucket_coords.append((bx, b_bottom))

                self.add_label(f"Created bucket {i+1}")

                # schedule next bucket
                self.parent.after(delay, lambda: create_bucket(i+1))

        create_bucket()


    # Animates insertion.
    def animate_insert(self, key, value, index):
        node = self.canvas.create_rectangle(10, 10, 50, 35, fill="lightyellow")
        text = self.canvas.create_text(30, 20, text=f"{key}:{value}")

        bx, b_bottom = self.bucket_coords[index]
        target_y = b_bottom + (len(self.bucket_nodes[index]) + 1) * 50

        def move():
            coords = self.canvas.coords(node)
            cx = (coords[0] + coords[2]) / 2
            cy = (coords[1] + coords[3]) / 2

            if cx < bx:
                self.canvas.move(node, 5, 0)
                self.canvas.move(text, 5, 0)
                self.parent.after(20, move)
            elif cy < target_y:
                self.canvas.move(node, 0, 5)
                self.canvas.move(text, 0, 5)
                self.parent.after(20, move)
            else:
                dx = bx - cx
                dy = target_y - cy
                self.canvas.move(node, dx, dy)
                self.canvas.move(text, dx, dy)

                new_coords = self.canvas.coords(node)
                new_cx = (new_coords[0] + new_coords[2]) / 2
                new_top = new_coords[1]

                if self.bucket_nodes[index]:
                    last_node, _ = self.bucket_nodes[index][-1]
                    last_coords = self.canvas.coords(last_node)
                    last_cx = (last_coords[0] + last_coords[2]) / 2
                    last_bottom = last_coords[3]

                    self.canvas.create_line(last_cx, last_bottom,
                                            new_cx, new_top,
                                            arrow=tk.LAST, width=2, fill="black",
                                            tags=f"arrow_{index}")
                else:
                    self.canvas.create_line(bx, b_bottom,
                                            new_cx, new_top,
                                            arrow=tk.LAST, width=2, fill="black",
                                            tags=f"arrow_{index}")

                self.bucket_nodes[index].append((node, text))
                self.canvas.itemconfig(node, fill="lightblue")

        move()

    
    # Controls insertion into hash table object
    def insert(self):
        try:
            key = self.accept_key_input()
            if key == -1:
                self.add_label("Invalid key", "red")
                return
            val = self.accept_value_input()
            if val == -1:
                self.add_label("Invalid value", "red")
                return
            print(key, val)

        except ValueError:
            messagebox.showerror("Error", "Key and Value must be integers")
            return

        # Find the table slot/bucket for insertion
        index = self.hash_obj._hash(key)
        rt_value = self.hash_obj.insert(key, val)   # backend returns status code

        if rt_value == 0:
            # Animate insertion
            self.animate_insert(key, val, index)
            self.add_label(f"Successfully inserted {key}:{val} in bucket {index}") 

        else:
            # Rejection feedback
            bx, b_bottom = self.bucket_coords[index]

            # Optional pulsating ring around bucket
            rect_coords = (bx - self.bucket_width//2,
                           b_bottom - self.bucket_height,
                           bx + self.bucket_width//2,
                           b_bottom)
            ring = self.canvas.create_oval(rect_coords[0]-10, rect_coords[1]-10,
                                           rect_coords[2]+10, rect_coords[3]+10,
                                           outline="red", width=3)

            def pulsate(step=0):
                if step < 6:
                    width = 3 + step % 2
                    self.canvas.itemconfig(ring, width=width)
                    self.parent.after(200, lambda: pulsate(step+1))
                else:
                    self.canvas.delete(ring)

            pulsate()

            self.add_label(f"Insertion of {key}:{val} rejected (load factor exceeded)", "red")


    def search(self):
        try:
            key = self.accept_key_input()
            if key == -1: 
                self.add_label("Invalid key", "red")
                return

        except ValueError:
            messagebox.showerror("Error", "Key and Value must be integers")
            return

        print("search key: ", key)

        self.animate_search(key)


    # Creates a pulsating ring around element in focus.
    def pulsate_ring(self, node, pulses=6, color="orange", 
                     message=None, callback=None):

        # Draw a pulsating outline ring around a node
        # flash message, then run callback.
        coords = self.canvas.coords(node)
        cx = (coords[0] + coords[2]) / 2
        cy = (coords[1] + coords[3]) / 2
        r = (coords[2] - coords[0]) / 2 + 10  # bigger than node

        ring = self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, 
                                       outline=color, width=2)

        def pulse(count=0):
            if count < pulses:
                width = 2 + (count % 2) * 3
                self.canvas.itemconfig(ring, width=width)
                self.parent.after(200, lambda: pulse(count+1))
            else:
                self.canvas.delete(ring)
                if message:
                    self.add_label(message)
                if callback:
                    callback()

        pulse()

        
    def animate_search(self, key, value=None):
        index = self.hash_obj._hash(key)
        chain = self.bucket_nodes[index]

        def check_node(i=0):
            if i < len(chain):
                node, text = chain[i]
                node_text = self.canvas.itemcget(text, "text")  # "key:value"
                try:
                    node_key, node_val = map(int, node_text.split(":"))
                except ValueError:
                    node_key, node_val = None, None

                if node_key == key and (value is None or node_val == value):
                    # Found → pulsate green and stop
                    self.pulsate_ring(node,
                                      color="green",
                                      message=f"Search success: Found {key} in bucket {index}")
                else:
                    # Not this one → pulsate orange then move to next
                    self.pulsate_ring(node,
                                      color="orange",
                                      message=f"Comparing key {key} at bucket {index}",
                                      callback=lambda: check_node(i+1))
            else:
                # End of chain → not found
                self.add_label(f"Search failed: {key} not found in bucket {index}")

        check_node()


    # Animates delete, fades out deletion, and compacts list
    def animate_delete(self, key, value=None):
        index = self.hash_obj._hash(key)
        deleted = self.hash_obj.delete(key, value)

        if not deleted:
            self.add_label(f"Delete failed: {key} not found", "red")
            return

        chain = self.bucket_nodes[index]
        if not chain:
            return

        # Find the matching node in the chain
        target_idx = None
        for i, (node, text) in enumerate(chain):
            node_text = self.canvas.itemcget(text, "text")  # e.g. "key:value"
            try:
                node_key, node_val = map(int, node_text.split(":"))
            except ValueError:
                continue
            if node_key == key and (value is None or node_val == value):
                target_idx = i
                break

        if target_idx is None:
            self.add_label(f"Delete failed: {key} not found in bucket {index}", "red")
            return

        node, text = chain[target_idx]

        def fade_out(step=0):
            if step < 10:
                shade = 255 - step*20
                color = f"#{shade:02x}{shade:02x}{shade:02x}"
                self.canvas.itemconfig(node, fill=color)

                coords = self.canvas.coords(node)
                self.canvas.coords(node,
                                   coords[0]+1, coords[1]+1,
                                   coords[2]-1, coords[3]-1)

                self.parent.after(100, lambda: fade_out(step+1))
            else:
                # remove node + text
                self.canvas.delete(node)
                self.canvas.delete(text)
                self.bucket_nodes[index].pop(target_idx)

                # compact remaining nodes
                bx, by = self.bucket_coords[index]
                for j, (n, t) in enumerate(self.bucket_nodes[index]):
                    target_y = by + (j+1) * 50
                    coords = self.canvas.coords(n)
                    cx = (coords[0] + coords[2]) / 2
                    cy = (coords[1] + coords[3]) / 2
                    dx = bx - cx
                    dy = target_y - cy
                    self.canvas.move(n, dx, dy)
                    self.canvas.move(t, dx, dy)

                # remove all arrows for this bucket
                self.canvas.delete(f"arrow_{index}")

                # redraw arrows for remaining nodes
                if self.bucket_nodes[index]:
                    # arrow from bucket to first node
                    first_node, _ = self.bucket_nodes[index][0]
                    fcoords = self.canvas.coords(first_node)
                    fcx = (fcoords[0] + fcoords[2]) / 2
                    ftop = fcoords[1]
                    self.canvas.create_line(bx, by, fcx, ftop,
                                            arrow=tk.LAST, width=2, fill="black",
                                            tags=f"arrow_{index}")

                    # arrows between nodes
                    for j in range(len(self.bucket_nodes[index]) - 1):
                        n1, _ = self.bucket_nodes[index][j]
                        n2, _ = self.bucket_nodes[index][j+1]
                        c1 = self.canvas.coords(n1)
                        c2 = self.canvas.coords(n2)
                        c1x = (c1[0] + c1[2]) / 2
                        c1b = c1[3]
                        c2x = (c2[0] + c2[2]) / 2
                        c2t = c2[1]
                        self.canvas.create_line(c1x, c1b, c2x, c2t, 
                                                arrow=tk.LAST, width=2, 
                                                fill="black",
                                                tags=f"arrow_{index}")

                self.add_label(f"Deleted key {key} from bucket {index}")


        # pulsate first, then fade out
        self.pulsate_ring(node,
                          color="red",
                          message=f"Deleting key {key} from bucket {index}",
                          callback=fade_out)



    def delete(self):
        try:
            key = self.accept_key_input()
            if key == -1: 
                self.add_label("Invalid key", "red")
                return

        except ValueError:
            messagebox.showerror("Error", "Key and Value must be integers")
            return

        print("delete key: ", key)

        self.animate_delete(key)


    # Reports collisions,average chain length and max chain length
    def animate_statistic(self, bucket_message_fn, 
                          final_backend_fn, color="blue"):

        total = len(self.bucket_nodes)

        def process_bucket(i=0):
            if i < total:
                chain = self.bucket_nodes[i]
                length = len(chain)
                if length > 0:
                    node = chain[0][0]  # highlight first node
                    self.pulsate_ring(node,
                                      color=color,
                                      message=bucket_message_fn(i, length),
                                      callback=lambda: self.parent.after(800, lambda: process_bucket(i+1)))
                else:
                    self.add_label(bucket_message_fn(i, 0))
                    self.parent.after(500, lambda: process_bucket(i+1))
            else:
                # final summary from backend
                result = final_backend_fn()
                self.add_label(result)

        process_bucket()



    def animate_statistic(self, bucket_message_fn, backend_fn, color="blue"):
        total = len(self.bucket_nodes)

        def process_bucket(i=0):
            if i < total:
                chain = self.bucket_nodes[i]
                length = len(chain)
                if length > 0:
                    node = chain[0][0]  # highlight first node
                    self.pulsate_ring(node,
                                  color=color,
                                  message=bucket_message_fn(i, length),
                                  callback=lambda: self.parent.after(500, lambda: process_bucket(i+1)))
                else:
                    self.add_label(bucket_message_fn(i, 0))
                    self.parent.after(500, lambda: process_bucket(i+1))
            else:
                # final summary from backend
                result = backend_fn(self.hash_obj)   # <-- call backend on hash object
                self.add_label(result)

        process_bucket()


    
    # Uses backend function to calculate max chain length     
    def animate_max_chain_length(self):
        def bucket_message_fn(i, length):
            return f"Bucket {i} length = {length}"

        def backend_fn(hash_obj):
            max_len = hash_obj.max_chain_length()  # backend call
            return f"Max chain length = {max_len}"

        self.animate_statistic(bucket_message_fn, backend_fn, color="blue")

    # Uses backend function to calculate number of collisions 
    def animate_collision_count(self):
        def bucket_message_fn(i, length):
            if length > 1:
                return f"Collision at bucket {i}"
            elif length == 1:
                return f"No collision at bucket {i}"
            else:
                return f"Bucket {i} is empty"

        def backend_fn(hash_obj):
            collisions = hash_obj.collision_count()  # backend call
            return f"Total collisions = {collisions}"

        self.animate_statistic(bucket_message_fn, backend_fn, color="red")



    # Uses backend function to calculate average chain length     
    def animate_avg_chain_length(self):
        def bucket_message_fn(i, length):
            return f"Bucket {i} length = {length}"

        def backend_fn(hash_obj):
            total, avg = hash_obj.average_chain_length()  # backend returns tuple
            return f"Average chain length = {total}/{len(hash_obj.table)} = {avg:.2f}"

        self.animate_statistic(bucket_message_fn, backend_fn, color="blue")

 

class BottomMenu:

    def __init__(self, parent, widgets, visualizer):
        self.parent = parent
        self.widgets = widgets
        self.visualizer = visualizer
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

        self.data_entry2 = tk.Entry(self.input_frame, width=20)
        self.txt_label2 = tk.Label(self.input_frame, text="Enter value", 
                font=('Regular', 15))

        self.setup_btn = tk.Button(self.input_frame, text="", 
                font=('Regular', 15), bg=self.bg_color, fg="white", 
                activebackground=self.bg_color, activeforeground="white" )

        #-----------------------------------
        # Dropdown menu copied from stack and queue program
        #-----------------------------------

        # First dropdown menu
        hash_btn = tk.Menubutton(self.bottom_menu_frame, text="Operations", relief="raised")
        #hash_btn.pack(side="left", anchor="w", padx=5, pady=5)   # side="left"
        hash_btn.grid(row=0, column=1, padx=20, pady=5, sticky="w")

        hash_menu = tk.Menu(hash_btn, tearoff=False)
        hash_btn.config(menu=hash_menu)

        subList1 = tk.Menu(hash_menu, tearoff=False)
        hash_menu.add_cascade(label="Hashing", menu=subList1)

        subList1.add_command(label="Create", command=lambda: self.widgets.setup_animation_ui("Create"))
        subList1.add_command(label="Insert", command=lambda: self.widgets.setup_animation_ui("Insert"))
        subList1.add_command(label="Delete", command=lambda: self.widgets.setup_animation_ui("Delete"))
        subList1.add_command(label="Search", command=lambda: self.widgets.setup_animation_ui("Search"))

        # Second dropdown menu
        stat_btn = tk.Menubutton(self.bottom_menu_frame, text="Statistics", relief="raised")
        #desc_btn.pack(side="left", anchor="w", padx=5, pady=5)   # side="left"
        stat_btn.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        stat_menu = tk.Menu(stat_btn, tearoff=False)
        stat_btn.config(menu=stat_menu)

        subList2 = tk.Menu(stat_menu, tearoff=False)
        stat_menu.add_cascade(label="Animation", menu=subList2)

        subList2.add_command(label="Avg length", command=lambda: self.widgets.setup_animation_ui("Avg length"))
        subList2.add_command(label="Max length", command=lambda: self.widgets.setup_animation_ui("Max length"))
        subList2.add_command(label="Collisions", command=lambda: self.widgets.setup_animation_ui("Collisions"))

        # Second dropdown menu
        desc_btn = tk.Menubutton(self.bottom_menu_frame, text="Descriptions", relief="raised")
        #desc_btn.pack(side="left", anchor="w", padx=5, pady=5)   # side="left"
        desc_btn.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        desc_menu = tk.Menu(desc_btn, tearoff=False)
        desc_btn.config(menu=desc_menu)

        subList3 = tk.Menu(desc_menu, tearoff=False)
        desc_menu.add_cascade(label="Animation", menu=subList2)

        subList3.add_command(label="About", command=lambda: self.widgets.execute_home())
        subList3.add_command(label="Chained hashing", command=lambda: self.widgets.open_pdf("Chain"))

    # --- Public API methods ---
    def clear_inputs(self):
        """Hide input frame and all input widgets."""
        for widget in (self.txt_label1, self.data_entry1,
                       self.setup_btn): widget.pack_forget()
        for widget in (self.txt_label2, self.data_entry2,
                       self.setup_btn): widget.pack_forget()


    def show_two_inputs(self, var, label_text1="Enter key", label_text2 ="Enter value"):
        # Show only one input field + setup button.
        self.clear_inputs()
        self.txt_label1.config(text=label_text1)
        self.txt_label1.pack(side="left", padx=5, pady=5)
        self.data_entry1.pack(side="left", padx=5, pady=5)
        self.txt_label2.config(text=label_text2)
        self.txt_label2.pack(side="left", padx=5, pady=5)
        self.data_entry2.pack(side="left", padx=5, pady=5)
        
        if var == "Insert":
            self.setup_btn.configure(text="Insert")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        else:
            self.visualizer.add_label("Invalid operation", "red")

    def show_one_input(self, var, label_text1="Enter key"):
        # Show only one input field + setup button.
        self.clear_inputs()
        self.txt_label1.config(text=label_text1)
        self.txt_label1.pack(side="left", padx=5, pady=5)
        self.data_entry1.pack(side="left", padx=5, pady=5)

        if var == "Delete":
            self.setup_btn.configure(text="Delete")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var == "Search":
            self.setup_btn.configure(text="Search")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        else:
            self.visualizer.add_label("Invalid operation", "red")

    # Show only setup button (no input required).
    def show_no_input(self, var):
        self.clear_inputs()

        if var == "Create":
            self.setup_btn.configure(text="Create")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var == "Avg length":
            self.setup_btn.configure(text="Avg length")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var == "Max length":
            self.setup_btn.configure(text="Max length")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var == "Collisions":
            self.setup_btn.configure(text="Collisions")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        else:
            self.visualizer.add_label("Invalid operation", "red")


# Usage
if __name__ == "__main__":
    App()

