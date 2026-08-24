import tkinter as tk
from hash_class import HashTable  # Import backend class

import tkinter as ttk
from tkinter import messagebox
from tkinter import scrolledtext
import os
import fitz # For pdf viewer 
from PIL import Image, ImageTk # For images

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Open Adress Hashing Animator")
        self.geometry("850x850")

        self.widgets = OpenAddr(self) # Main class for animation

        self.mainloop()

class OpenAddr(tk.Tk):
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Open Address Hashing")
        self.create_widgets()
        
        # Constants for animation
        self.node_radius = 20
        self.v_gap = 30
        self.h_gap = 20

        self.bucket_width = 100
        self.bucket_height = 35
        self.v_spacing = 45

        # Keep canvas display frame open 
        self.canvas_display_frame.pack(padx=10, pady=(50,75), fill=tk.BOTH,
                expand=True)

        # Initialize entry_nodes here
        self.execute_home()


    # Creates buttons and frames needed for the GUI
    def create_widgets(self):

        self.bg_color = '#383839' # Define background color

        # Defines a header frame will embed title and short title
        self.head_frame = tk.Frame(self.parent, bg=self.bg_color, 
                highlightbackground='white', highlightthickness=1)

        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.configure(height=50)


        # Defines title bar for the header frame
        self.title_lb = tk.Label(self.head_frame, text='Data structure:', 
                bg=self.bg_color, fg='white', font=('Bold', 20))
        self.title_lb.pack(side=tk.LEFT)

        self.subtitle_lb = tk.Label(self.head_frame, 
                                    text='Open Address Hashing Animation', 
                                    bg=self.bg_color, fg='white',
                                    font=('Regular', 15))

        self.subtitle_lb.place(relx=0.35, rely=0.2)


        # Menu specification defined in a BottomMenu class 
        self.bottom_menu = BottomMenu(self.parent, self, self)

        # Defines canvas frame and the canvas where animation happen
        self.canvas_display_frame = tk.Frame(self.parent)
        self.canvas = tk.Canvas(self.canvas_display_frame, bg="white")

        # Defines scroll-frame to hold canvas with scrollbars.
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

    # Hides input frame and its buttons, not used
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
        elif fx == "Open hashing": file_name = "open_address_hashing.pdf"
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


    # Accepts user input for first data entry field 
    def accept_key_input(self):
        user_input = self.bottom_menu.data_entry1.get()
        if not user_input.isnumeric():
           self.add_label("Invalid key: Enter a number", "red") 
           return -1
        return int(user_input)

    # Accepts user input for second data entry field
    def accept_value_input(self):
        # Get and validate user's input
        user_input = self.bottom_menu.data_entry2.get()

        if not user_input.isnumeric(): 
           self.add_label("Invalid value: Enter a number", "red") 
           return -1
        else:
            return int(user_input)


    # Dynamically sets the button titles and entry fields
    def setup_animation_ui(self, var):
        # Hide close/home buttons if visible
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()
        if self.home_btn.winfo_ismapped():
            self.home_btn.place_forget()

        # Reset only the input frame
        self.bottom_menu.input_frame.pack_forget()
        self.bottom_menu.input_frame.pack(fill=tk.X, padx=10, pady=5)

        # --- Operation-specific UI ---
        if var == "Create":
            self.bottom_menu.clear_inputs()

            # Size label + entry (from main visualizer)
            self.bottom_menu.txt_label1.config(text="Size")
            self.bottom_menu.txt_label1.pack(side="left", padx=5, pady=5)
            self.bottom_menu.data_entry1.pack(side="left", padx=5, pady=5)

            # Conflict resolution dropdown
            self.bottom_menu.txt_label2.config(text="Conflict Res.")
            self.bottom_menu.txt_label2.pack(side="left", padx=5, pady=5)
            self.bottom_menu.crm_dropdown.pack(side="left", padx=5, pady=5)

            # Create button calls animate_creation directly
            self.bottom_menu.setup_btn.configure(
                text="Create",
                command=lambda: self.animate_creation(
                    size=int(self.bottom_menu.data_entry1.get()),
                    crm=0 if self.bottom_menu.crm_var.get() == "Linear" else 1
                )
            )
            self.bottom_menu.setup_btn.pack(side="left", padx=10, pady=5)


        elif var == "Insert":
            self.bottom_menu.show_two_inputs("Insert")
            self.bottom_menu.setup_btn.configure(
                text="Insert", command=lambda: self.insert()
            )

        elif var == "Delete":
            self.bottom_menu.show_one_input("Delete")
            self.bottom_menu.setup_btn.configure(
                text="Delete", command=lambda: self.delete()
            )

        elif var == "Search":
            self.bottom_menu.show_one_input("Search")
            self.bottom_menu.setup_btn.configure(
                text="Search", command=lambda: self.search()
            )

        else:
            self.visualizer.add_label("Invalid operation", "red")

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

    # Creates a hash table of specified size using a specified 
    # collision resolution technique.
    def animate_creation(self, size, crm):
        resolution = "Linear" if crm == 0 else "Quadratic"

        # Initialize hash table object
        self.hash_obj = HashTable(size=size, crm=crm)
        # Initialize entry_nodes here
        self.entry_nodes = [None] * size

        # Clear canvas before drawing
        self.canvas.delete("all")

        # Bucket dimensions
        start_x = 150
        start_y = 50

        self.bucket_coords = []
        self.bucket_nodes = []   # Store rect/text IDs here

        def create_bucket(i=0):
            if i < size:
                bx = start_x
                by = start_y + i * self.v_spacing

                # Draw rectangle for bucket
                rect = self.canvas.create_rectangle(
                    bx - self.bucket_width//2, by - self.bucket_height//2,
                    bx + self.bucket_width//2, by + self.bucket_height//2,
                    outline="black", width=2, fill="white"
                )

                # Draw index label to the left of bucket
                label = self.canvas.create_text(
                    bx-60, by, text=str(i), fill="black", font=("Arial", 12, "bold")
                )

                self.bucket_coords.append((bx, by))
                self.bucket_nodes.append((rect, label))  # Save rect + label IDs

                # Schedule next bucket after 300ms
                self.parent.after(400, lambda: create_bucket(i+1))
            else:
                self.add_label(
                    f"Created hash table of size {size} with {resolution} resolution",
                    "green"
                )

        create_bucket()

    def reset_bucket_colors(self):
        for rect, _ in self.bucket_nodes:
            self.canvas.itemconfig(rect, fill="white")
        # Re‑color occupied slots
        for i, entry in enumerate(self.hash_obj.table):
            if entry is not None and entry != self.hash_obj.deleted:
                rect, _ = self.bucket_nodes[i]
                self.canvas.itemconfig(rect, fill="lightblue")


    # Wrapped for animate_insert. Reads input key:value pair and call
    # animate_insert
    def insert(self):

        key = self.accept_key_input()
        if key == -1:
            self.add_label("Key is invalid", "red")
            return

        value = self.accept_value_input()
        if value == -1:
            self.add_label("Value is invalid", "red")
            return

         
        self.animate_insert(key, value)
 


    # Animation of insertion
    def animate_insert(self, key, value):
        # Create a temporary widget for holding key:value pair
        node = self.canvas.create_rectangle(20, 26, 90, 54, fill="yellow")
        text = self.canvas.create_text(55, 41, text=f"{key}:{value}")

        # Get probe sequence and the final slot from backend
        # depending on collision resolution method.
        if self.hash_obj.crm == 0:
            probes, idx = self.hash_obj.linear_resolution(key, value)
        else:
            probes, idx = self.hash_obj.quadratic_resolution(key, value)

        # If table is full idx from backend will be None.
        if idx is None:
            self.add_label("Insert failed: table full", "red")
            self.parent.after(800, lambda: (self.canvas.delete(node),
                                            self.canvas.delete(text)))
            return

        # Animate probe sequence moving to probe slots.
        def animate_probe(step=0):
            if step < len(probes):
                target_index = probes[step]
                bx, by = self.bucket_coords[target_index]

                coords = self.canvas.coords(node)
                cx = (coords[0] + coords[2]) / 2
                cy = (coords[1] + coords[3]) / 2

                if abs(cx - bx) > 2 or abs(cy - by) > 2:
                    dx = 5 if cx < bx else -5 if cx > bx else 0
                    dy = 5 if cy < by else -5 if cy > by else 0
                    self.canvas.move(node, dx, dy)
                    self.canvas.move(text, dx, dy)
                    self.parent.after(50, lambda: animate_probe(step))
                    return

                # At bucket center
                if target_index == idx:
                    move_to_final(idx)  # explicitly move to final slot
                else:
                    flash_collision(target_index, lambda: animate_probe(step+1))
            else:
                move_to_final(idx)

        def move_to_final(target_index):
            bx, by = self.bucket_coords[target_index]
            coords = self.canvas.coords(node)
            cx = (coords[0] + coords[2]) / 2
            cy = (coords[1] + coords[3]) / 2

            if abs(cx - bx) > 2 or abs(cy - by) > 2:
                dx = 5 if cx < bx else -5 if cx > bx else 0
                dy = 5 if cy < by else -5 if cy > by else 0
                self.canvas.move(node, dx, dy)
                self.canvas.move(text, dx, dy)
                self.parent.after(50, lambda: move_to_final(target_index))
            else:
                settle(target_index)

        # Function settles the key:value pair to correct slot.
        def settle(target_index):
            existing = self.hash_obj.table[target_index]

            success = self.hash_obj.insert(key, value)

            if success:
                if existing is not None and existing != self.hash_obj.deleted and existing[0] == key:
                    # Key already existed → overwrite
                    self.canvas.itemconfig(node,fill="lightblue", outline="orange", width=3)
                    self.add_label(f"Overwrote {key} with new value {value} at slot {target_index}", "blue")
                else:
                    # Fresh insertion
                    self.canvas.itemconfig(node, fill="lightblue", outline="")
                    self.add_label(f"Inserted {key}:{value} at slot {target_index}", "green")

                self.entry_nodes[target_index] = (node, text)
            else:
                self.canvas.itemconfig(node, fill="red")
                self.add_label(f"Insert failed for {key}:{value}", "red")
                self.parent.after(800, lambda: (self.canvas.delete(node),
                                                self.canvas.delete(text)))

            self.reset_bucket_colors()



        # Flashes collision for slot.
        def flash_collision(target_index, callback):
            rect, _ = self.bucket_nodes[target_index]
            # temporarily highlight the collided bucket
            self.canvas.itemconfig(rect, fill="pink")
            self.add_label(f"Collision at slot {target_index}", "red")
            # reset color back to white after 600ms
            self.parent.after(800, lambda: (self.canvas.itemconfig(rect, fill="white"), callback()))

        # Start animation
        animate_probe(0)



    def animate_search(self, key, on_found, on_not_found):
        idx, probes = self.hash_obj.find(key)

        # If key was found, only animate up to that slot
        if idx is not None and idx in probes:
            probes = probes[:probes.index(idx)+1]

        def flash_probe_sequence(probes):
            if not probes:
                if idx is not None:
                    on_found(idx)
                else:
                    on_not_found()
                return

            target_index = probes[0]
            bx, by = self.bucket_coords[target_index]
            rect = self.canvas.create_rectangle(
                bx - 50, by - 20, bx + 50, by + 20,
                outline="orange", width=3
            )
            self.add_label(f"Probing slot {target_index}", "orange")
            self.parent.after(800, lambda: (self.canvas.delete(rect),
                                        flash_probe_sequence(probes[1:])))

        flash_probe_sequence(probes)


    # Used to mark the slot deleted if the entry deleted
    def mark_deleted_entry(self, slot_index):
        entry = self.entry_nodes[slot_index]
        if entry:
            rect_id, text_id = entry
            # Paint entry red immediately
            self.canvas.itemconfig(rect_id, fill="red")
            self.canvas.itemconfig(text_id, text="<deleted>")
            self.add_label(f"Entry at slot {slot_index} marked deleted", "red")

            # Start fade to gray
            self.fade_to_gray(rect_id)


    # Animates deleted entry from red to gray
    def fade_to_gray(self, rect_id, steps=10, delay=100):
        
        '''
           rect_id: canvas rectangle ID
           steps: number of fade steps
           delay: ms between steps
        '''
        
        # Start with red (255,0,0), end with gray (200,200,200)
        start_color = (255, 0, 0)
        end_color = (200, 200, 200)

        def interpolate_color(step):
            r = int(start_color[0] + (end_color[0] - start_color[0]) * step / steps)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * step / steps)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * step / steps)
            return f"#{r:02x}{g:02x}{b:02x}"

        def do_step(step=0):
            if step <= steps:
                color = interpolate_color(step)
                self.canvas.itemconfig(rect_id, fill=color)
                self.parent.after(delay, lambda: do_step(step+1))

        do_step()


    # Function to animate deletion of an entry 
    def animate_delete(self, key):

        def on_found(idx): # Delete element if it is found in table. 
            success, probes, actual_idx, val_deleted = self.hash_obj.delete(key)

            if success:
                bx, by = self.bucket_coords[actual_idx]

                #print("bx=", bx, "by=", by)

                rect = self.canvas.create_rectangle(
                    bx - 50, by - 20, bx + 50, by + 20,
                    outline="red", width=3
                )
                entry = self.bucket_nodes[actual_idx]

                self.add_label(f"Deleted {val_deleted} at slot {actual_idx}", 
                               "green")
                self.mark_deleted_entry(actual_idx)
                
                self.parent.after(800, lambda: self.canvas.delete(rect))

        def on_not_found(): # Flashes message if key is not found
            self.add_label(f"Delete failed: {key} not found", "red")

        # First animate search, then delete
        self.animate_search(key, on_found, on_not_found)


    # Main search function
    def search(self):
        try:
            key = self.accept_key_input()
            if key == -1: 
                self.add_label("Invalid key", "red")
                return

        except ValueError:
            messagebox.showerror("Error", "Key and Value must be integers")
            return

        #print("search key: ", key)

            # Call animate_search with callbacks
        self.animate_search(
            key,
            on_found=lambda idx: self.add_label(f"Key {key} found at slot {idx}",
                                                "green"),
            on_not_found=lambda: self.add_label(f"Key {key} not found", "red")
        )


    def delete(self):
        try:
            key = self.accept_key_input()
            if key == -1: 
                self.add_label("Invalid key", "red")
                return

        except ValueError:
            messagebox.showerror("Error", "Key and Value must be integers")
            return


        self.animate_delete(key)



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

        # --- Input frame ---
        self.input_frame = tk.Frame(self.footer_frame, height=40)
        self.input_frame.pack(side="top", fill=tk.X)
        self.input_frame.pack_propagate(False)

        # --- Bottom menu frame ---
        self.bottom_menu_frame = tk.Frame(self.footer_frame, height=40)
        self.bottom_menu_frame.pack(side="bottom", fill=tk.X)
        self.bottom_menu_frame.pack_propagate(False)

        # --- Input widgets ---
        self.data_entry1 = tk.Entry(self.input_frame, width=20)
        self.txt_label1 = tk.Label(self.input_frame, text="Enter value", 
                                   font=('Regular', 15))

        self.data_entry2 = tk.Entry(self.input_frame, width=20)
        self.txt_label2 = tk.Label(self.input_frame, text="Enter value", 
                                   font=('Regular', 15))

        self.setup_btn = tk.Button(
            self.input_frame, text="", font=('Regular', 15),
            bg=self.bg_color, fg="white",
            activebackground=self.bg_color, activeforeground="white"
        )

        # --- Conflict resolution dropdown (defined once here) ---
        self.crm_var = tk.StringVar(value="Linear")
        self.crm_dropdown = tk.OptionMenu(self.input_frame, self.crm_var, 
                                          "Linear", "Quadratic")

        # --- Menus ---
        self._create_operations_menu()
        #self._create_statistics_menu()
        self._create_descriptions_menu()
        return

    def _create_operations_menu(self):
        hash_btn = tk.Menubutton(self.bottom_menu_frame, 
                                 text="Operations", relief="raised")
        hash_btn.grid(row=0, column=1, padx=20, pady=5, sticky="w")
        hash_menu = tk.Menu(hash_btn, tearoff=False)
        hash_btn.config(menu=hash_menu)

        subList1 = tk.Menu(hash_menu, tearoff=False)
        hash_menu.add_cascade(label="Hashing", menu=subList1)

        subList1.add_command(label="Create", 
                             command=lambda: self.widgets.setup_animation_ui("Create"))
        subList1.add_command(label="Insert", 
                             command=lambda: self.widgets.setup_animation_ui("Insert"))
        subList1.add_command(label="Delete", 
                             command=lambda: self.widgets.setup_animation_ui("Delete"))
        subList1.add_command(label="Search", 
                             command=lambda: self.widgets.setup_animation_ui("Search"))


    def _create_descriptions_menu(self):
        desc_btn = tk.Menubutton(self.bottom_menu_frame, text="Descriptions", 
                                 relief="raised")
        desc_btn.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        desc_menu = tk.Menu(desc_btn, tearoff=False)
        desc_btn.config(menu=desc_menu)

        subList3 = tk.Menu(desc_menu, tearoff=False)
        desc_menu.add_cascade(label="Animation", menu=subList3)
        subList3.add_command(label="About", 
                             command=lambda: self.widgets.execute_home())
        subList3.add_command(label="Open hashing", 
                             command=lambda: self.widgets.open_pdf("Chain"))

    # --- Public API methods ---
    def clear_inputs(self):
        '''Hide input frame and all input widgets.'''

        for widget in (self.txt_label1, self.data_entry1,
                       self.txt_label2, self.data_entry2,
                       self.setup_btn, self.crm_dropdown):
            widget.pack_forget()
        return

    def show_two_inputs(self, var, label_text1="Enter key", 
                        label_text2="Enter value"):
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
            return
        elif var == "Create":
            self.setup_btn.configure(text="Create")
            self.setup_btn.pack(side="left", padx=10, pady=5)
            self.crm_var.set("Linear")  # reset default
            self.crm_dropdown.pack(side="left", padx=5, pady=5)
            return
        else:
            self.visualizer.add_label("Invalid operation", "red")
            return

    def show_one_input(self, var, label_text1="Enter key"):
        self.clear_inputs()
        self.txt_label1.config(text=label_text1)
        self.txt_label1.pack(side="left", padx=5, pady=5)
        self.data_entry1.pack(side="left", padx=5, pady=5)

        if var == "Delete":
            self.setup_btn.configure(text="Delete")
            self.setup_btn.pack(side="left", padx=10, pady=5)
            return
        elif var == "Search":
            self.setup_btn.configure(text="Search")
            self.setup_btn.pack(side="left", padx=10, pady=5)
            return
        else:
            self.visualizer.add_label("Invalid operation", "red")
            return

    def show_no_input(self, var):
        self.clear_inputs()
        if var == "Collisions":
            self.setup_btn.configure(text="Collisions")
            self.setup_btn.pack(side="left", padx=10, pady=5)
            return

        else:
            self.add_label("Invalid operation", color="red")
            return

# Usage
if __name__ == "__main__":
    App()

