# graph_animator.py
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import os
import fitz # For pdf viewer 
from PIL import Image, ImageTk #
import networkx as nx
from collections import deque
from graph_backend_class import Graph

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Animator")

        # Define window geometry
        self.geometry("850x800")

        # 1. Initialize the Main class for animation first
        self.widgets = GraphAnimator(self) 
 

        # 2. Safely launch the home PDF screen using the initialized widgets
        self.after(100, self.widgets.execute_home)

        self.mainloop()


class GraphAnimator:
    def __init__(self, parent=None):

        if parent is None: # Refers to root 
            self.root = tk.Tk()
            self.root.title("Graph Operations")
            self.parent = self.root
        else:
            self.parent = parent
            self.root = parent

        # Defines widgets of main.
        self.create_widgets()

        # Graph starts empty
        self.graph = None
        self.positions = {}

        # User can adjust layout by dragging node on canvas.
        self.drag_data = {"node": None, "dx": 0, "dy": 0}


    # Defines widgets related to main window. 
    def create_widgets(self):

        self.bg_color = '#383839' # Background color of buttons

        # Header frame (for ribbon head on top of the canvas).
        self.head_frame = tk.Frame(self.parent, bg=self.bg_color,
                                   highlightbackground='white', 
                                   highlightthickness=1)

        # Defined only onces and packed to make it visible
        self.head_frame.pack(side=tk.TOP, fill=tk.X)

        # Title of header. 
        self.title_lb = tk.Label(self.head_frame, text='Data structure:',
                             bg=self.bg_color, fg='white', font=('Bold', 20))

        self.title_lb.pack(side=tk.LEFT)

        # Subtitle or secondary ribbon title
        self.subtitle_lb = tk.Label(self.head_frame,
                                    text='Graph Animation',
                                    bg=self.bg_color, fg='white',
                                    font=('Regular', 15))

        self.subtitle_lb.place(relx=0.35, rely=0.2)

        # Define menu vis BottomMenu class.
        self.bottom_menu = BottomMenu(self.parent, self, self)

        # Main Workspace Wrapper (Holds everything cleanly under the header)
        main_workspace = tk.Frame(self.parent, bg="white")
        main_workspace.pack(fill=tk.BOTH, expand=True)

        # Dedicated control cluster layout panel at the absolute base
        btn_frame = tk.Frame(main_workspace, bg=self.bg_color)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Leave un-packed initially, open_pdf and setup_ui invokes it cleanly
        self.home_btn = tk.Button(btn_frame, text="Home", bg="#383839",
                                  fg="white", font=('Bold', 15),
                                  command=lambda: self.open_pdf("Home"))

        
        self.close_btn = tk.Button(btn_frame, text="Close", bg="#383839",
                                   fg="white", font=('Bold', 15),
                                   command=self.close_current_view)

        # Canvas container frame (Takes up ALL remaining upper space cleanly)
        self.canvas_display_frame = tk.Frame(main_workspace, bg="white")
        self.canvas_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas_scroll_frame = tk.Frame(self.canvas_display_frame, bg="white")
        canvas_scroll_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_scroll_frame, bg="white", 
                                highlightthickness=0)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_label = tk.Label(self.root, text="",
                             bg='white', fg='black', font=('Bold', 20))

        # Scrollbars
        self.v_scrollbar = ttk.Scrollbar(canvas_scroll_frame, orient=tk.VERTICAL,
                                         command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.h_scrollbar = ttk.Scrollbar(self.canvas_display_frame,
                                         orient=tk.HORIZONTAL,
                                         command=self.canvas.xview)
        self.h_scrollbar.pack(fill=tk.X)

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set,
                              xscrollcommand=self.h_scrollbar.set)

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

        #if self.text_widget.winfo_ismapped():
        #    self.text_widget.pack_forget()
        
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()

    def open_pdf(self, fx):
        # 1. Force the main parent window to update its layout metrics 
        # Ensures accurate width/height values even if it was just resized.
        self.parent.update_idletasks()

        # 2. Extract current coordinates and size from the parent window
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()

        # 3. Create the child window
        pdf_win = tk.Toplevel(self.parent)
       
        # 4. Strip the OS border and title bar 
        pdf_win.overrideredirect(True)

        # 5. Apply matching dimensions and overlay coordinates exactly
        pdf_win.geometry(f"{parent_width}x{parent_height}+{parent_x}+{parent_y}")
        pdf_win.title(f"PDF Viewer")

        # --- State Variables ---
        # Store state inside the window object. Keeps track of current file/zoom
        pdf_win.current_file = ""
        pdf_win.zoom_factor = 1.5
        pdf_win.pdf_document = None
        pdf_win.img_references = []  # Keep references, prevent garbage collection

        def start_move(event):
            pdf_win._drag_x = event.x
            pdf_win._drag_y = event.y

        def do_move(event):
            x = pdf_win.winfo_x() + (event.x - pdf_win._drag_x)
            y = pdf_win.winfo_y() + (event.y - pdf_win._drag_y)
            pdf_win.geometry(f"+{x}+{y}")

        # --- Top Toolbar Frame ---
        toolbar = tk.Frame(pdf_win, bg="#e0e0e0", padx=5, pady=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Bind the drag functions to the toolbar frame safely
        toolbar.bind("<Button-1>", start_move)
        toolbar.bind("<B1-Motion>", do_move)

        # Map initial fx keys to file paths
        if fx == "Home":
            pdf_win.current_file = "explanation.pdf"
        elif fx == "Open hashing":
            pdf_win.current_file = "open_address_hashing.pdf"
        else:
            pdf_win.current_file = fx  # Assume direct file path if passed

        # Open File Button
        open_btn = tk.Button(toolbar, text="📁 Open File", font=('Arial', 11),
                             command=lambda: self.browse_new_pdf(pdf_win))
        open_btn.pack(side=tk.LEFT, padx=5)

        # Zoom In Button
        zoom_in_btn = tk.Button(toolbar, text="➕ Zoom In", font=('Arial', 11),
                                command=lambda: self.change_zoom(pdf_win, 0.2))
        zoom_in_btn.pack(side=tk.LEFT, padx=5)

        # Zoom Out Button
        zoom_out_btn = tk.Button(toolbar, text="➖ Zoom Out", font=('Arial', 11),
                                 command=lambda: self.change_zoom(pdf_win, -0.2))
        zoom_out_btn.pack(side=tk.LEFT, padx=5)

        # --- Main Display Layout ---
        # 1. Pack the Horizontal Scrollbar so that it spans entire bottom width
        h_scrollbar = ttk.Scrollbar(pdf_win, orient=tk.HORIZONTAL, 
                                    command=lambda *args: pdf_canvas.xview(*args))
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # 2. Pack the Vertical Scrollbar on the right side
        v_scrollbar = ttk.Scrollbar(pdf_win, orient=tk.VERTICAL, 
                                    command=lambda *args: pdf_canvas.yview(*args))
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas + scrollbars inside child window
        pdf_canvas = tk.Canvas(pdf_win, bg="white")
        pdf_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Link canvas to window state so rendering helper functions can access it
        pdf_win.canvas = pdf_canvas

        # --- Bottom Close Button ---
        close_btn = tk.Button(toolbar, text="❌ Close", bg="#383839", fg="white",
                              font=('Arial', 14, 'bold'), 
                              command=pdf_win.destroy)

        close_btn.pack(side=tk.RIGHT, padx=5)

        # Initial Load
        self.load_and_render_pdf(pdf_win)

    # Handles document opening and page rendering on the canvas.
    def load_and_render_pdf(self, pdf_win):
        canvas = pdf_win.canvas
        canvas.delete("all")  # Clear previous drawings
        pdf_win.img_references = []  # Clear previous image caches

        file_name = pdf_win.current_file

        # Validation
        if not file_name:
            canvas.create_text(450, 300, text="No PDF file selected.", 
                               anchor=tk.CENTER, font=('Arial', 14))
            return

        if not os.path.exists(file_name):
            canvas.create_text(450, 300, text=f"File not found: {file_name}", 
                               anchor=tk.CENTER, fill="red", font=('Arial', 14))
            return

        try:
            # Update title bar
            pdf_win.title(f"PDF Viewer - {os.path.basename(file_name)} ({int(pdf_win.zoom_factor * 100)}%)")
            
            # Open document
            pdf_win.pdf_document = fitz.open(file_name)
            
            # Vertical offset tracking to render pages sequentially downwards
            y_offset = 10
            max_width = 0

            for page_num in range(len(pdf_win.pdf_document)):
                page = pdf_win.pdf_document[page_num]
                
                # Apply zoom factor matrix
                matrix = fitz.Matrix(pdf_win.zoom_factor, pdf_win.zoom_factor)
                pix = page.get_pixmap(matrix=matrix)
                
                # Convert PyMuPDF Pixmap to PIL Image, then to Tkinter PhotoImage
                img_data = pix.tobytes("ppm")
                pil_img = Image.open(io.BytesIO(img_data)) if 'io' in globals() else Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                tk_img = ImageTk.PhotoImage(pil_img)
                
                # Save reference to avoid garbage collection blanking out images
                pdf_win.img_references.append(tk_img)
                
                # Draw on canvas
                canvas.create_image(10, y_offset, anchor=tk.NW, image=tk_img)
                
                y_offset += pix.height + 15  # Increment spacing for next page
                if pix.width > max_width:
                    max_width = pix.width

            # Configure scrollable region area dynamically
            canvas.configure(scrollregion=(0, 0, max_width + 20, y_offset))

        except Exception as e:
            canvas.create_text(450, 300, text=f"Error rendering PDF: {str(e)}", anchor=tk.CENTER, fill="red")

    # Modifies the zoom factor within safe bounds and re-renders.
    def change_zoom(self, pdf_win, amount):
        new_zoom = pdf_win.zoom_factor + amount
        # Safe boundary guard rails (50% minimum up to 300% maximum zoom)
        if 0.5 <= new_zoom <= 3.0:
            pdf_win.zoom_factor = round(new_zoom, 1)
            self.load_and_render_pdf(pdf_win)

    # Launches a native OS file dialog box on top of pdf viewer window 
    def browse_new_pdf(self, pdf_win):
        file_path = filedialog.askopenfilename(
            parent=pdf_win,  # <-- This forces it to stay on top of the child window
            title="Select a PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:  # Ensure user didn't hit cancel
            pdf_win.current_file = file_path
            pdf_win.zoom_factor = 1.0  # Reset zoom factor back to baseline scale
            self.load_and_render_pdf(pdf_win)


    # Accepts user input for first data entry field 
    def accept_num_nodes(self):
        user_input = self.bottom_menu.data_entry1.get().strip()
        if not user_input.isdigit():
            self.add_label("Invalid input: Enter a positive integer", "red")
            return None 

        # 1. Catch completely blank or empty entries explicitly
        if not user_input:
            self.add_label("Invalid input: Field cannot be empty", "red")
            return None

        # 2. Check if the remaining string is a valid integer digit structure
        # (Handling negative values explicitly through ValueError instead of ignoring them)
        try:
            num_nodes  = int(user_input)
        except ValueError:
            self.add_label("Invalid input: Please enter a valid whole number", "red")
            return None

        # 3. Check value constraints safely
        if num_nodes < 1:
            self.add_label("Invalid input: Max connections must be >= 1", "red")
            return None 

        return num_nodes 

    # Accepts user input for second data entry field
    def accept_max_connections(self):
        user_input = self.bottom_menu.data_entry2.get().strip()
        
        # 1. Catch completely blank or empty entries explicitly
        if not user_input:
            self.add_label("Invalid input: Field cannot be empty", "red")
            return None

        # 2. Check if the remaining string is a valid integer digit structure
        # (Handling negative values explicitly through ValueError instead of ignoring them)
        try:
            max_conn = int(user_input)
        except ValueError:
            self.add_label("Invalid input: Please enter a valid whole number", "red")
            return None

        # 3. Check value constraints safely
        if max_conn < 1:
            self.add_label("Invalid input: Max connections must be >= 1", "red")
            return None 

        return max_conn

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
        if var == "Draw Graph":
            self.bottom_menu.clear_inputs()

            self.bottom_menu.txt_label1.config(text="Nodes")
            self.bottom_menu.txt_label1.pack(side="left", padx=5, pady=5)
            self.bottom_menu.data_entry1.pack(side="left", padx=5, pady=5)

            self.bottom_menu.txt_label2.config(text="Max Connections")
            self.bottom_menu.txt_label2.pack(side="left", padx=5, pady=5)
            self.bottom_menu.data_entry2.pack(side="left", padx=5, pady=5)

            self.bottom_menu.setup_btn.configure(
                text="Draw Graph",
                command=lambda: self.animate_draw_graph()
            )
            self.bottom_menu.setup_btn.pack(side="left", padx=10, pady=5)

        elif var == "Animate DFS":
            self.bottom_menu.clear_inputs()
            self.bottom_menu.txt_label1.config(text="Start Node")
            self.bottom_menu.txt_label1.pack(side="left", padx=5, pady=5)
            self.bottom_menu.data_entry1.pack(side="left", padx=5, pady=5)

            self.bottom_menu.setup_btn.configure(
                text="Animate DFS",
                command=lambda: self.animate_dfs(
                    start_node=int(self.bottom_menu.data_entry1.get() or 0)
                )
            )
            self.bottom_menu.setup_btn.pack(side="left", padx=10, pady=5)

        elif var == "Animate BFS":
            self.bottom_menu.clear_inputs()
            self.bottom_menu.txt_label1.config(text="Start Node")
            self.bottom_menu.txt_label1.pack(side="left", padx=5, pady=5)
            self.bottom_menu.data_entry1.pack(side="left", padx=5, pady=5)

            self.bottom_menu.setup_btn.configure(
                text="Animate BFS",
                command=lambda: self.animate_bfs(
                    start_node=int(self.bottom_menu.data_entry1.get() or 0)
                )
            )
            self.bottom_menu.setup_btn.pack(side="left", padx=10, pady=5)

        else:
            self.visualizer.add_label("Invalid operation", "red")

        self.parent.update_idletasks()


    def add_label(self, text, color="blue"):
        # 1. Stop any ongoing fade cycles by updating a unique tracking ID
        if not hasattr(self, 'fade_id_counter'):
            self.fade_id_counter = 0
        self.fade_id_counter += 1
        current_fade_id = self.fade_id_counter

        # 2. Config text and position it where it can be seen 
        self.canvas_label.config(text=text, fg=color)
        
        # Tip: relative coordinates position against the parent widget size.
        # If it's attached to 'self' (the full window), relx=0.5, rely=0.85 is perfect.
        self.canvas_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
        self.root.update()

        # 3. Trigger the safe fade-out loop sequence
        self.fade_out_animation(self.canvas_label, color, current_fade_id, duration=2000, steps=20)


    def fade_out_animation(self, label, target_color, fade_id, current_step=0, duration=2000, steps=20):
        # Safety Check: If a new message was generated, cancel this old fade thread loop
        if fade_id != self.fade_id_counter:
            return
        if not label.winfo_exists():
            return

        bg_hex = self.bg_color  # e.g., "#383839"

        def hex_to_rgb(hex_str):
            hex_str = hex_str.lstrip('#')
            return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

        try:
            # Safely grab RGB bytes from any color string or format type
            rgb_start = label.winfo_rgb(target_color)
            r1, g1, b1 = [x >> 8 for x in rgb_start]
            r2, g2, b2 = hex_to_rgb(bg_hex)
        except Exception:
            # Strict fallback safety defaults
            r1, g1, b1 = (0, 0, 255) if target_color == "blue" else (255, 0, 0)
            r2, g2, b2 = hex_to_rgb(bg_hex)

        if current_step <= steps:
            alpha = current_step / steps
            curr_r = int(r1 + (r2 - r1) * alpha)
            curr_g = int(g1 + (g2 - g1) * alpha)
            curr_b = int(b1 + (b2 - b1) * alpha)
            
            new_hex = f"#{curr_r:02x}{curr_g:02x}{curr_b:02x}"
            label.config(fg=new_hex)
            
            delay = duration // steps
            self.root.after(delay, lambda: self.fade_out_animation(
                label, target_color, fade_id, current_step + 1, duration, steps
            ))
        else:
            # Completely clear and un-map layout space when visibility hits zero
            label.config(text="")
            label.place_forget()


    def animate_draw_graph(self):
        self.canvas.delete("all")
        num_nodes = self.accept_num_nodes()
        max_conn = self.accept_max_connections()
        if num_nodes is None or max_conn is None:
            self.add_label("No input to draw the graph", color="red")
            return

        # Create backend graph
        self.graph = Graph(num_nodes, 3)
        self.graph.prob = self.graph.calculate_probability(num_nodes, max_conn)
        self.graph.generate_random_graph(max_conn)
        self.add_label("Drag nodes to readjus graph", color="green")

        # Layout and draw
        self.positions = {}
        self._auto_layout()
        self._draw_nodes()
        self._draw_edges()


    def _auto_layout(self):
        G = nx.Graph()

        for v, neighbors in self.graph.adj_list.items():
            for nbr, w in neighbors:
                G.add_edge(v, nbr, weight=w)
        pos = nx.spring_layout(G, scale=300, center=(400, 300))
        for node, (x, y) in pos.items():
            self.positions[node] = (x, y)

    def _draw_nodes(self):
        radius = 20
        for i, (x, y) in self.positions.items():
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                                    fill="lightblue", tags=(f"node{i}", "node"))
            self.canvas.create_text(x, y, text=chr(65+i), tags=f"label{i}")
            # Bind drag events
            self.canvas.tag_bind(f"node{i}", "<ButtonPress-1>", 
                                 self.on_node_press)
            self.canvas.tag_bind(f"node{i}", "<B1-Motion>", self.on_node_drag)
            self.canvas.tag_bind(f"node{i}", "<ButtonRelease-1>", 
                                 self.on_node_release)

    def _draw_edges(self):
        self.canvas.delete("edge")
        radius = 20
        for v, neighbors in self.graph.adj_list.items():
            for nbr, w in neighbors:
                if v < nbr:  # avoid duplicate undirected edges
                    x1, y1 = self.positions[v]
                    x2, y2 = self.positions[nbr]
                    dx, dy = x2 - x1, y2 - y1
                    length = (dx**2 + dy**2) ** 0.5
                    if length == 0: continue
                    offset_x = dx / length * radius
                    offset_y = dy / length * radius
                    start_x, start_y = x1 + offset_x, y1 + offset_y
                    end_x, end_y = x2 - offset_x, y2 - offset_y
                    self.canvas.create_line(start_x, start_y, end_x, end_y,
                                            fill="gray", tags=(f"edge{v}-{nbr}",
                                                               "edge"))
                    midx, midy = (start_x + end_x) / 2, (start_y + end_y) / 2
                    offx, offy = -dy / length * 15, dx / length * 15
                    self.canvas.create_text(midx+offx, midy+offy, text=str(w),
                                            fill="black", tags="edge")

    # --- Dragging Handlers ---
    def on_node_press(self, event):
        node_tag = self.canvas.gettags("current")[0]
        node_id = int(node_tag.replace("node", ""))
        self.drag_data["node"] = node_id
        x, y = self.positions[node_id]
        self.drag_data["dx"] = x - event.x
        self.drag_data["dy"] = y - event.y

    def on_node_drag(self, event):
        node_id = self.drag_data["node"]
        if node_id is None: return
        new_x = event.x + self.drag_data["dx"]
        new_y = event.y + self.drag_data["dy"]
        self.positions[node_id] = (new_x, new_y)
        self.canvas.coords(f"node{node_id}", new_x-20, new_y-20, 
                           new_x+20, new_y+20)
        self.canvas.coords(f"label{node_id}", new_x, new_y)
        self._draw_edges()

    def on_node_release(self, event):
        self.drag_data["node"] = None

    def reset_layout(self):
        if self.graph is None:
            self.add_label("Can't reset an empty graph", color="red")
            return

        self.canvas.delete("all")
        self._auto_layout()
        #self.canvas.delete("all")
        self._draw_nodes()
        self._draw_edges()

    # Starts a continuous pulsating ring around a specified canvas node.
    # Automatically cleans up any previously running pulse.
    def start_pulsing_node(self, node_id, color="red"):

        # 1. Clean up any existing active pulse ring and its animation loop
        if hasattr(self, "_active_pulse_id") and self._active_pulse_id:
            self.root.after_cancel(self._active_pulse_id)
            self._active_pulse_id = None
        self.canvas.delete("pulse_ring")

        # 2. Get target node coordinates
        coords = self.canvas.coords(f"node{node_id}")
        if not coords:
            return

        x1, y1, x2, y2 = coords
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        base_radius = (x2 - x1) / 2

        # 3. Pulse animation state variables
        state = {"scale": 1.0, "expanding": True}

        def pulse_loop():
            self.canvas.delete("pulse_ring")
            
            # Animate scaling factor between 1.1x and 1.6x
            if state["expanding"]:
                state["scale"] += 0.05
                if state["scale"] >= 1.6:
                    state["expanding"] = False
            else:
                state["scale"] -= 0.05
                if state["scale"] <= 1.1:
                    state["expanding"] = True
            
            r = base_radius * state["scale"]
            self.canvas.create_oval(
                center_x - r, center_y - r,
                center_x + r, center_y + r,
                outline=color, width=2, tags="pulse_ring"
            )
            
            # Schedule next frame (~30 FPS) and keep track of the ID
            self._active_pulse_id = self.root.after(33, pulse_loop)

        # Start the loop
        pulse_loop()

    # Stops the pulsating ring entirely and cleans up canvas artifacts.
    def stop_pulsing(self):

        if hasattr(self, "_active_pulse_id") and self._active_pulse_id:
            self.root.after_cancel(self._active_pulse_id)
            self._active_pulse_id = None
        self.canvas.delete("pulse_ring")


    def animate_bfs(self, start_node=0):
        if self.graph is None:
            messagebox.showerror("Error", "No graph created yet. Please draw a graph first.")
            return 

        # Validate that the start node exists in the current graph
        if start_node < 0 or start_node >= self.graph.num_nodes:
            self.add_label(f"Error: Node {chr(65 + int(start_node))} does not exist!", "red")
            return

        # 1. Reset all elements on the canvas to default styling and clear old numbers
        self.canvas.itemconfig("node", fill="lightblue")
        self.canvas.itemconfig("edge", fill="gray", width=1)
        self.canvas.delete("dfs_label") # Clear DFS or older labels to avoid overlaps
        self.root.update()

        visited = set()
        
        # 2. Store elements in Queue as a tuple: (current_node, parent_node)
        # We start from the provided start_node parameter
        queue = deque([(start_node, None)])
        
        self.bfs_order_counter = 1 
        component_index = 0

        def bfs_step():
            nonlocal component_index
            
            self.stop_pulsing()

            # If queue is empty, look for disconnected graph components
            if not queue:
                while component_index < self.graph.num_nodes:
                    node_to_check = (start_node + component_index) % self.graph.num_nodes
                    component_index += 1
                    if node_to_check not in visited:
                        queue.append((node_to_check, None))
                        break
                
                if not queue:
                    return

            # Pop the current vertex and the parent vertex we traveled from (FIFO)
            v, parent = queue.popleft()

            self.start_pulsing_node(v, color="blue") 
            
            # Skip if the node was already processed via an alternate queue layer
            if v in visited:
                self.root.after(300, bfs_step)
                return
                
            node_name = chr(65 + int(v))
            self.add_label(f"Mark vertex {node_name} as visited", "green")
            visited.add(v)

            # 3. Highlight the edge that discovers the current node 
            if parent is not None:
                edge_tag1 = f"edge{parent}-{v}"
                edge_tag2 = f"edge{v}-{parent}"
                if self.canvas.find_withtag(edge_tag1):
                    edge_tag = edge_tag1
                    arrow_direction = "last"
                else: 
                    edge_tag = edge_tag2
                    arrow_direction = "first"

                self.canvas.itemconfig(edge_tag, fill="blue", width=3,
                                       arrow=arrow_direction,
                                       arrowshape=(12, 14, 5)
                                       ) # Blue for BFS Tree paths

                self.add_label(f"Added BFS edge ({chr(65 + int(parent))},{chr(65 + int(v))})")

            # Highlight current node green
            self.canvas.itemconfig(f"node{v}", fill="green")

            # 4. Add BFS sequence number label beside the node
            try:
                coords = self.canvas.coords(f"node{v}")
                if coords:
                    x1, y1, x2, y2 = coords
                    # Position text slightly above and to the right of the node circle
                    text_x = x2 + 12 
                    text_y = y1 - 8  
                    
                    self.canvas.create_text(
                        text_x, text_y,
                        text=f"#{self.bfs_order_counter}",
                        fill="darkgreen", # Dark green labels from DFS runs
                        font=("Arial", 11, "bold"),
                        tags="dfs_label" # Grouped under the same deletion tag.
                    )
                    self.bfs_order_counter += 1  
            except Exception as e:
                print(f"Error drawing label: {e}")

            self.root.update()

            # 5. Process neighbors sequentially
            for nbr, _ in self.graph.adj_list[v]:
                if nbr not in visited:
                    queue.append((nbr, v))

            # Continue to the next step after animation delay
            self.root.after(600, bfs_step)

        # Start execution
        self.root.after(300, bfs_step)



    def animate_dfs(self, start_node=0):
        if self.graph is None:
            self.add_label("Error: No graph created yet.", color="red")
            return 

        if start_node < 0 or start_node >= self.graph.num_nodes:

            self.add_label(f"Error: Node {chr(65 + int(start_node))} does not exist!", "red")
            return

        # Reset components and ensure old pulses stop
        self.canvas.itemconfig("node", fill="lightblue")
        self.canvas.itemconfig("edge", fill="gray", width=1)
        self.canvas.delete("dfs_label") 
        self.stop_pulsing() 
        self.root.update()

        visited = set()
        stack = [(start_node, None)]  
        self.dfs_order_counter = 1 
        component_index = 0

        def dfs_step():
            nonlocal component_index
            
            # Stop the ring while transitioning states or when finished
            self.stop_pulsing()

            if not stack:
                while component_index < self.graph.num_nodes:
                    node_to_check = (start_node + component_index) % self.graph.num_nodes
                    component_index += 1
                    if node_to_check not in visited:
                        stack.append((node_to_check, None))
                        break
                if not stack:
                    return

            v, parent = stack.pop() 
            
            if v in visited:
                self.root.after(300, dfs_step)
                return
                
            visited.add(v)

            self.add_label(f"Mark vertex {chr(65+int(v))}", "green")

            if parent is not None:
                edge_tag1 = f"edge{parent}-{v}"
                edge_tag2 = f"edge{v}-{parent}"

                if self.canvas.find_withtag(edge_tag1):
                    edge_tag, arrow_direction = edge_tag1, "last" 
                else:
                    edge_tag, arrow_direction = edge_tag2, "first" 

                self.canvas.itemconfig(edge_tag, fill="blue", width=3, 
                                       arrow=arrow_direction,
                                       arrowshape=(12, 14, 5))

                self.add_label(f"Added tree edge ({chr(65 + int(parent))},{chr(65 + int(v))})")

            

            self.canvas.itemconfig(f"node{v}", fill="red") 

            # Start pulsing around the current node using our new helper!
            self.start_pulsing_node(v, color="red")

            try:
                coords = self.canvas.coords(f"node{v}")
                if coords:
                    x1, y1, x2, y2 = coords
                    text_x = x2 + 12 
                    text_y = y1 - 8  
                    
                    self.canvas.create_text(
                        text_x, text_y,
                        text=f"#{self.dfs_order_counter}",
                        fill="darkred",
                        font=("Arial", 11, "bold"),
                        tags="dfs_label"
                    )
                    self.dfs_order_counter += 1  
            except Exception as e:
                print(f"Error drawing label: {e}")
                self.add_label(f"Error drawing label: {e}", "red")

            self.root.update()

            neighbors = list(self.graph.adj_list[v])
            for nbr, _ in reversed(neighbors):
                if nbr not in visited:
                    stack.append((nbr, v))

            self.root.after(600, dfs_step)

        self.root.after(300, dfs_step)




class BottomMenu:
    def __init__(self, parent, widgets, visualizer):
        self.parent = parent
        self.widgets = widgets
        self.visualizer = visualizer
        self.create_menu()

    def add_placeholder(self, entry, placeholder_text):
        entry.insert(0, placeholder_text)
        entry.config(fg="grey")

        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(fg="black")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.config(fg="grey")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
   
    def create_menu(self):
        self.bg_color = "#383839"

        # --- Footer container ---
        self.footer_frame = tk.Frame(self.parent, bg="white")
        self.footer_frame.pack(side="top", fill="x")

        # --- Input frame (dynamic inputs) ---
        self.input_frame = tk.Frame(self.footer_frame, height=40, bg="white")
        self.input_frame.pack(side="top", fill=tk.X)
        self.input_frame.pack_propagate(False)

        # --- Bottom menu frame (persistent buttons) ---
        self.bottom_menu_frame = tk.Frame(self.footer_frame, height=40, bg="white")
        self.bottom_menu_frame.pack(side="bottom", fill=tk.X)
        self.bottom_menu_frame.pack_propagate(False)

        # --- Input widgets (defined once, reused dynamically) ---
        self.data_entry1 = tk.Entry(self.input_frame, width=20)
        self.txt_label1 = tk.Label(self.input_frame, text="Value 1",
                               font=('Regular', 15), bg="white", fg="black")

        self.data_entry2 = tk.Entry(self.input_frame, width=20)
        self.txt_label2 = tk.Label(self.input_frame, text="Value 2",
                               font=('Regular', 15), bg="white", fg="black")

        # Add placeholders
        self.add_placeholder(self.data_entry1, "Enter first value...")
        self.add_placeholder(self.data_entry2, "Enter second value...")

        self.setup_btn = tk.Button(
            self.input_frame, text="", font=('Regular', 15),
            bg=self.bg_color, fg="white",
            activebackground=self.bg_color, activeforeground="white"
        )

        # --- Persistent operation buttons ---
        tk.Button(self.bottom_menu_frame, text="Draw Graph",
                  font=('Regular', 15),
                  command=lambda: self.visualizer.setup_animation_ui("Draw Graph"),
                  bg=self.bg_color, fg="white").pack(side="left", padx=5, pady=5)

        tk.Button(self.bottom_menu_frame, text="DFS",
                  font=('Regular', 15),
                  command=lambda: self.visualizer.setup_animation_ui("Animate DFS"),
                  bg=self.bg_color, fg="white").pack(side="left", padx=5, pady=5)

        tk.Button(self.bottom_menu_frame, text="BFS", font=('Regular', 15),
                  command=lambda: self.visualizer.setup_animation_ui("Animate BFS"),
                  bg=self.bg_color, fg="white").pack(side="left", padx=5, pady=5)

        tk.Button(self.bottom_menu_frame, text="Reset Layout",font=('Regular', 15),
                  command=self.visualizer.reset_layout,
                  bg=self.bg_color, fg="white").pack(side="left", padx=5, pady=5)



    # --- Public API methods ---
    def clear_inputs(self):
        # Hide input widgets.
        for widget in (self.txt_label1, self.data_entry1,
                       self.txt_label2, self.data_entry2,
                       self.setup_btn):
            widget.pack_forget()


if __name__ == "__main__":
    # Launch the application cleanly using our singular App window setup
    app = App()

