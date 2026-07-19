import tkinter as tk
from stackOps import Stack  # Import your Stack class
from queueOps import QueueArray # Import your Queue class
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox as mb 

#from wcwidth import wcwidth, wcswidth

import os
import fitz 
from PIL import Image, ImageTk, ImageFont

# Create the main window
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stack Animation")
        self.geometry("850x800") # Display window

        self.delay = 10 # Default value
        self.widgets = Stack_and_Queue(self) # Instance of widget class


        self.mainloop() 


class Stack_and_Queue:
    def __init__(self, parent):
        self.parent = parent 
        self.stack_obj = Stack()  # Initialize stack
        self.queue_obj = QueueArray()  # Initialize stack

        self.create_widgets()

        
        self.execute_home()


    def create_widgets(self):
        self.bg_color = "#383839" # Define widget background color
        
        self.delay = 50

        self.rect_position = []

        # Header frame
        self.head_frame = tk.Frame(self.parent, bg=self.bg_color, 
                highlightbackground='white', highlightthickness=1)
        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.configure(height=50)

        # Title bar for the header frame
        self.title_lb = tk.Label(self.head_frame, text='Data structure:', 
                bg=self.bg_color, fg='white', font=('Bold', 20))
        self.title_lb.pack(side=tk.LEFT, padx=10)

        self.subtitle_lb = tk.Label(self.head_frame, text='Stack & Queue Animation', 
                bg=self.bg_color, fg='white', font=('Regular', 15))
        self.subtitle_lb.place(relx=0.35, rely=0.2)


        # Menu specitication in a separate class
        self.bottom_menu = BottomMenu(self.parent, self)

        # Define canvas frame and canvas
        self.canvas_display_frame = tk.Frame(self.parent)

        self.canvas = tk.Canvas(self.canvas_display_frame, bg="white")


        # Fix Scrollbar Size & Placement
        self.v_scrollbar = ttk.Scrollbar(self.canvas_display_frame,
                orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self.canvas_display_frame, 
                orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, 
                xscrollcommand=self.h_scrollbar.set)

        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        # Text Widget (Correct Placement)
        self.text_widget = scrolledtext.ScrolledText(self.parent, wrap=tk.WORD,
                width=75, height=10)
        # Set window title
        self.parent.title("Stack & Queue Animation")

        self.item_size = 50 # Define a size for items 

        self.text_to_rect = {}

        self.block_height = 30          # height of each rectangle
        self.vertical_spacing = self.item_size * .75  # vertical spacing 
        

        # Close Button for closing pdf viewer 
        self.close_btn = tk.Button(self.parent, text="Close", bg="#383839", 
                fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15), 
                command=lambda: self.close_current_view)

        # Home button takes user to description of animation
        self.home_btn = tk.Button(self.parent, text="Home", bg="#383839", 
                fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15), 
                command=lambda: self.open_pdf("Home"))

    def execute_status_message(self, message, x=180, y=500, color="blue"):
        """Display or update a persistent status message at (x,y)."""
        if not hasattr(self, "status_text_id") or not self.canvas.type(self.status_text_id):
            # Create once if it doesn't exist or was deleted
            self.status_text_id = self.canvas.create_text(
                x, y, text=message, fill=color,
                font=('Bold', 15), anchor="w"
            )
        else:
            # Update existing text
            self.canvas.itemconfig(self.status_text_id, text=message, fill=color)
            self.canvas.itemconfig(self.status_text_id, fill=color)




    # Function for display of status messages
    '''def execute_status_message(self, message, x=200, y=150, color="blue"):
        """Display a status message at loc (x, y)."""

        # Keep a dictionary of text items keyed by (x, y)
        if not hasattr(self, "status_text_items"):
            self.status_text_items = {}

        key = (x, y)

        if key not in self.status_text_items:
            # Create new text item at this position
            text_id = self.canvas.create_text(
                x, y,
                text=message,  # Variable contains the actual text
                fill=color,    # Specification of text color
                font=('Bold', 15), # Sepcify font weight and size
                anchor="w"       
            )
            self.status_text_items[key] = text_id
        else:
            # Update existing text item at this position
            text_id = self.status_text_items[key]
            self.canvas.itemconfig(text_id, text=message, fill=color)'''


    # Allows clearing of the message from the coordinate positions
    def clear_status_message(self, x=200, y=500):
        """Erase the status message at (x, y)."""
        if hasattr(self, "status_text_items"):
            key = (x, y)
            if key in self.status_text_items:
                text_id = self.status_text_items[key]
                self.canvas.delete(text_id)       # remove from canvas
                del self.status_text_items[key]   # remove from dictionary

    # Clear contents before displaying new fields, text, buttons, etc.
    def clear_main_content_area(self):
        if self.canvas_display_frame.winfo_ismapped():
            self.canvas_display_frame.pack_forget()
        self.bottom_menu.clear_inputs()



    def setup_animation_ui(self, var):
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()
        if self.home_btn.winfo_ismapped():
            self.home_btn.place_forget()

        # Keep canvas frame visible, don’t forget it
        # Reset only input frame
        self.bottom_menu.input_frame.pack_forget()
        self.bottom_menu.input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Configure inputs depending on operation
        if var == "Push": 
            self.bottom_menu.show_single_input("Push")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_push()
            )


        elif var == "Pop":
            self.bottom_menu.show_no_input("Pop")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_pop()
            )
        elif var == "New stack":
            self.bottom_menu.show_no_input("New stack")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.execute_print("Stack") 
            )

        elif var == "Enqueue":
            self.bottom_menu.show_single_input("Enqueue")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_enqueue()
            )

        elif var == "Dequeue":
            self.bottom_menu.show_no_input("Dequeue")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_dequeue()
            )
        elif var == "New queue":
            self.bottom_menu.show_no_input("New queue")
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.execute_print("Queue") 
            )
        self.parent.update_idletasks()

    # Close current view and display Home button
    def close_current_view(self):

        # 1) Clear main content area (canvas or other widgets)
        self.clear_main_content_area()

        # 2) Remove PDF-specific resources if present
        if hasattr(self, 'pdf_image_tk'):
            try:
                del self.pdf_image_tk
            except Exception:
                pass
        if hasattr(self, 'pdf_composite_image_pil'):
            try:
                del self.pdf_composite_image_pil
            except Exception:
                pass

        # 3) Reset canvas scrollregion (safe default)
        try:
            self.canvas.config(scrollregion=(0, 0, self.canvas.winfo_width(), 
                                             self.canvas.winfo_height()))

        except Exception:
            # canvas may not exist or be initialized yet; ignore safely
            pass  # Not specified

        # 4) Hide main action and close buttons if they exist
        if hasattr(self, 'home_btn') and self.home_btn.winfo_exists():
            # don't forget: we may want to hide it first if it was visible elsewhere
            try:
                self.home_btn.place_forget()
            except Exception:
                pass # Not specified

        if hasattr(self, 'close_btn') and self.close_btn.winfo_exists():
            try:
                self.close_btn.place_forget()
            except Exception:
                pass # Not specified

        # 5) Ensure home button exists and is configured
        if not hasattr(self, 'home_btn') or not self.home_btn.winfo_exists():
            # Create a simple Home button if it doesn't exist yet.
            # Adjust parent if your button is a child of a different frame.
            self.home_btn = tk.Button(self.parent, text="Home", 
                                      command=self.open_pdf(), 
                                      bg="#383839", 
                                      fg="white"
                                     )

        try:
            self.parent.update_idletasks()
        except Exception:
            pass # You can print an error here

        try:
            # Horizontally and vertically centered
            self.home_btn.place(relx=0.5, rely=0.5, anchor='center')

            # Ensure it's above the canvas
            self.home_btn.lift()
        except Exception:
            try:
                # Fallback: absolute placement if relative placement fails
                self.home_btn.place(relx=0.5, y=0.5, anchor='center')
                self.home_btn.lift()

            except Exception:
                pass # Can print an error




    def execute_print(self, var):
        if self.home_btn.winfo_ismapped():
            self.home_btn.place_forget()

        #self.clear_main_content_area()
            # Cancel any running animation safely
        self.canvas.delete("all") # Not clearing the canvas, why?

        if var == "Stack":
            self.stack_obj.makenull() #= Stack()
            self.draw_stack()
            #self.execute_status_message("Stack is empty", 275, 500, color="blue")
            return
        elif var == "Queue": 
            self.queue_obj.makenull() #= QueueArray()
            self.draw_queue()
            return



    def draw_queue(self):

                # Keep canvas frame visible
        self.canvas_display_frame.pack(padx=10, pady=(50,75), 
                                       fill=tk.BOTH, 
                                       expand=True
                                      )
        self.canvas.delete("all")

        if not self.queue_obj.is_empty():
            qlist = self.queue_obj.to_list()

            item_width = 50
            spacing = 20
            x_start = 100
            y1 = 310
            y2 = 340

            for i, val in enumerate(qlist):
                x1 = x_start +  i * (self.item_size + spacing)
                x2 = x1 + item_width
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags=f"block_{i}")
                self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(val), font=('Bold', 15),  fill="white", tags=f"text_{i}")
        
                if i > 0: 
                    self.canvas.create_line(x1-10, y1-2, x1-10, y2+2, fill="black", width=3)

            # Create line with arrow head for identity of front 
            line_id1 = self.canvas.create_line(x_start-45, (y1+y2)//2, x_start, (y1+y2)//2, fill="black", width=3, arrow="last")

            # Add a label at the tail of the line
            label_id1 = self.canvas.create_text(x_start-70, (y1+y2)//2, text="front", font=("Arial", 15), fill="black")

            # Put parallel lines for display of queue 
            line_id3 = self.canvas.create_line(x2, (y1+y2)//2, x2+45, (y1+y2)//2, fill="black", width=3, arrow="first")

            # Create line with arrow head for identity of rear 
            label_id2 = self.canvas.create_text(x2+70, (y1+y2)//2, text="rear", font=("Arial", 15), fill="black")
        
            line_id3 = self.canvas.create_line(95, y1-5, x2+8, y1-5, fill="black", width=3)
            line_id4 = self.canvas.create_line(95, y2+5, x2+8, y2+5, fill="black", width=3)
             # Create canvas header 
            #label_id3 = self.canvas.create_text(350, 100, text="Current status of Queue", font=("Arial", 15), fill="blue")
        else:
            #label_id4 = self.canvas.create_text(350, 100, text="Queue is Empty", font=("Arial", 15), fill="blue")
    
            msg = "Created an empty queue"
            x_m = 250  
            y_m = 120

            self.execute_status_message(msg, x_m, y_m, color="blue")


    def animate_enqueue(self):

        user_input = self.bottom_menu.data_entry1.get()
        if user_input.isnumeric():
            value = int(user_input)
            success = self.queue_obj.enqueue(value)

            if success:
                spacing = 20
                y_start, y_end = 310, 340
                x_start = 100 + (self.queue_obj.length()-1) * (self.item_size + spacing)
                x_end = x_start + 50

                # Temporary yellow rect with black stroke
                rect_id = self.canvas.create_rectangle(
                    x_start+80, y_start, x_end+80, y_end,
                    fill="yellow", outline="black"
                )
                text_id = self.canvas.create_text(
                    x_start+105, y_start+15, text=str(value),
                    fill="black", font=('Bold', 15)
                )

                # Movement after pulsation
                def move_left():
                    current_coords = self.canvas.coords(rect_id)
                    if current_coords[0] > x_start:
                        self.canvas.move(rect_id, -5, 0)
                        self.canvas.move(text_id, -5, 0)

                        self.parent.after(50, move_left)

                    else:
                        # Finalize as green block
                        self.canvas.itemconfig(rect_id, fill="yellow", outline="")
                        self.canvas.itemconfig(text_id, fill="black")
                        self.draw_queue()

                        l_s = self.queue_obj.length() # Message after draw_queue 
                        msg = f"Enqueue successful: queue length = {l_s}"
                        self.execute_status_message(msg, 180, 200, color="blue")

                        

                # Pulsate before moving
                self.pulsate(rect_id, x_start+40, (y_start+y_end)//2, 
                             pulses=6, callback=move_left)

                self.bottom_menu.data_entry1.delete(0, tk.END)



            else:
                self.execute_status_message("Queue is full: Enqueue failed")
        else:
            self.execute_status_message("Invalid input: Enter a number")
            self.bottom_menu.data_entry1.delete(0, tk.END)


    def animate_dequeue(self):
        if not self.queue_obj.is_empty():
            block_items = self.canvas.find_withtag("block_0")
            text_items = self.canvas.find_withtag("text_0")

            if block_items and text_items:
                block_id, text_id = block_items[0], text_items[0]
                dequeued_val = self.queue_obj.dequeue()

                def move_left():
                    rect_coords = self.canvas.coords(block_id)
                    if rect_coords and rect_coords[0] > -60:  # move off canvas
                        self.canvas.itemconfig(block_id, fill="yellow")
                        self.canvas.itemconfig(text_id, fill="black")

                        self.canvas.move(block_id, -5, 0)
                        self.canvas.move(text_id, -5, 0)
                        self.parent.after(50, move_left)
                    else:
                        self.canvas.delete(block_id)
                        self.canvas.delete(text_id)
                        print(f"Dequeued: {dequeued_val}")

                        self.draw_queue()

                        l_s = self.queue_obj.length() # Message after draw_queue 
                        msg = f"Successfully dequeued {dequeued_val}, queue length = {l_s}"
                        self.execute_status_message(msg, 180, 200, color="blue")
                        

                # Pulsate before moving out
                rect_coords = self.canvas.coords(block_id)
                x_center = (rect_coords[0] + rect_coords[2]) / 2
                y_center = (rect_coords[1] + rect_coords[3]) / 2
                self.pulsate(block_id, x_center, y_center, 
                             pulses=6, callback=move_left)

            else:
                self.execute_status_message("Queue is empty: Dequeue failed")
        else:
            self.execute_status_message("Queue is empty: Dequeue failed")




    def animate_pop(self):
        """Animates pop operation with pulsate + upward move + disappear"""

        if self.stack_obj.is_empty():
            self.execute_status_message("Stack is empty: pop failed", 180, 500, color="red")
            return

        top_index = self.stack_obj.size() - 1
        block_id = self.canvas.find_withtag(f"block_{top_index}")
        text_id = self.canvas.find_withtag(f"text_{top_index}")

        popped_value = self.stack_obj.pop()

        if block_id and text_id:
            rect_coords = self.canvas.coords(block_id)
            if not rect_coords:
                return

            # Compute center for pulsation
            x_center = (rect_coords[0] + rect_coords[2]) // 2
            y_center = (rect_coords[1] + rect_coords[3]) // 2
            self.canvas.itemconfig(block_id, fill="yellow")
            self.canvas.itemconfig(text_id, fill="black")

            # After pulsation, move upward until it disappears
            def move_up():
                rect_coords = self.canvas.coords(block_id)
                if rect_coords and rect_coords[1] > 30:  # stop near top edge
                    self.canvas.move(block_id, 0, -10)
                    self.canvas.move(text_id, 0, -10)

                    # store anim_id
                    self.parent.after(50, move_up)

                else:
                    # Remove block + text
                    self.canvas.delete(block_id)
                    self.canvas.delete(text_id)
                    # Redraw stack and show status
                    self.draw_stack()
                    msg = f"Successfully popped {popped_value}, stack length = {self.stack_obj.size()}"
                    x_m = 250
                    y_m = 120
                    self.execute_status_message(msg, x_m, y_m, color="blue")

            # Use the reusable pulsate helper, then call move_up
            self.pulsate(block_id, x_center, y_center, pulses=6, callback=move_up)

    def draw_stack_boder(self, x1, x2):
        self.canvas.create_line(x1-8, 485, x2+8, 485, fill="black",
                width=3, tags="stack-boder")
        self.canvas.create_line(x1-8, 485, x1-8, 180, fill="black",
                width=3, tags="stack-boder")
        self.canvas.create_line(x2+8, 485, x2+8, 180, fill="black",
                width=3, tags="stack-boder")
        self.canvas.create_line(x1-8, 180, x1-24, 180, fill="black",
                width=3, tags="stack-boder")
        self.canvas.create_line(x2+8, 180, x2+24, 180, fill="black",
                width=3, tags="stack-boder")


    def draw_stack(self):
        """Redraws the stack visually"""

        # Keep canvas frame visible
        self.canvas_display_frame.pack(padx=10, pady=(50,75), 
                                       fill=tk.BOTH, 
                                       expand=True
                                      )
        self.canvas.delete("all")
        x1, y1 = 300, 450
        x2, y2 = 400, 480
        for i, val in enumerate(self.stack_obj.get_stack()):

            y1 = 450 - i * self.vertical_spacing
            y2 = y1 + self.block_height
            self.canvas.create_rectangle(x1, y1, x2, y2, 
                    fill="blue", tags=f"block_{i}")
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(val),
                    fill="white", font=('Regular',15), tags=f"text_{i}")
            self.canvas.create_line(x1, y2 + 2, x2, y2 + 2, 
                    fill="white", width=2)

        if self.stack_obj.is_empty():
            line_id1 = self.canvas.create_line((x1+x2)//2, y1+35, (x1+x2)//2,
                    y1, fill="black", width=3, arrow="first")

            label_id1 = self.canvas.create_text((x1+x2)//2,y1-10, text="Top", 
                    font=("Arial", 12), fill="black")
        else:
            line_id1 = self.canvas.create_line((x1+x2)//2, y1, (x1+x2)//2,
                    y1-40, fill="black", width=3, arrow="first")

             # Add a label at the tail of the line
            label_id1 = self.canvas.create_text((x1+x2)//2,y1-50, text="Top", 
                    font=("Arial", 12), fill="black")

        self.draw_stack_boder(x1, x2) 

        msg = "Created an empty Stack"
        x_m = 250  
        y_m = 120
        #x_m = 300 - offset_m 

        self.execute_status_message(msg, x_m, y_m, color="blue")


    def pulsate(self, rect_id, x_center, y_center, pulses=6, callback=None):
        """Make a canvas rectangle pulsate horizontally around its center."""
        def _pulse(count=0):
            if count < pulses:
                scale = 1.1 if count % 2 == 0 else 0.9
                self.canvas.scale(rect_id, x_center, y_center, scale, 1.0)

                # store anim_id
                self.parent.after(100, lambda: _pulse(count + 1))

            else:
                if callback:
                    callback()
        _pulse()
    

    def drop_down(self, rect_id, text_id, y_target, step=10, delay=50, callback=None):
        """Drop a rectangle + text vertically until y_target, then call callback."""
        def _drop():
            current_coords = self.canvas.coords(rect_id)
            if current_coords and current_coords[1] < y_target:
                self.canvas.move(rect_id, 0, step)
                self.canvas.move(text_id, 0, step)

                # store anim_id
                self.parent.after(delay, _drop)

            else:
                if callback:
                    callback()
        _drop()

    def animate_push(self):
        """Animates push operation with user input"""

        user_input = self.bottom_menu.data_entry1.get()
        if not user_input.isnumeric():
            self.execute_status_message("Invalid input: Enter a number", 350, 500, color="red")
            return

        value = int(user_input)

        if self.stack_obj.is_full():
            self.execute_status_message("Stack is full: Push failed", 350, 500, color="red")
            return


        success = self.stack_obj.push(value)
        if not success:
            self.execute_status_message("Push failed unexpectedly", 350, 500, color="red")
            return

        # Starting position just above stack border
        x_center = 350
        y_start = 30
        y_target = 450 - (self.stack_obj.size() - 1) * (self.vertical_spacing + self.block_height)
        y_target = max(y_target, y_start)

        rect_id = self.canvas.create_rectangle(
            x_center - 50, y_start, x_center + 50, 
            y_start + self.block_height,
            fill="yellow", tags="anim",
        )
        text_id = self.canvas.create_text(
            x_center, y_start + self.block_height // 2,
            text=str(value), fill="black", font=('Bold', 15), tags="anim"
        )

        def after_drop():
            self.draw_stack()
            l_s = len(self.stack_obj.to_list())
            msg = f"Successfully pushed {value}: stack length = {l_s}"
            self.execute_status_message(msg, 180, 500, color="blue")

        # Run pulsate, then drop
        self.pulsate(rect_id, x_center, y_start, pulses=6,
                callback=lambda: self.drop_down(rect_id, 
                    text_id, y_target, callback=after_drop))


        # Clear input field
        self.bottom_menu.data_entry1.delete(0, tk.END)




    def open_pdf(self, fx):
        self.clear_main_content_area() # Hide other content first
        if self.home_btn.winfo_ismapped():
            self.home_btn.place_forget()

        # Make the canvas frame visible for PDF display
        self.canvas_display_frame.pack(padx=10, pady=(10,75), fill=tk.BOTH, expand=True) # pady bottom for close_btn
        self.canvas.delete("all") # Clear previous canvas content

        file_name = ""
        if fx == "Home": file_name = "explanation.pdf"
        elif fx == "Stack": file_name = "stack_description.pdf"
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
                # zoom_factor = 1.0 for 72 DPI (1 PDF point = 1 pixel)
                # zoom_factor = 1.33 for ~96 DPI (often better for screen)
                zoom_factor = 1.33
                mat = fitz.Matrix(zoom_factor, zoom_factor)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                
                img_pil = Image.frombytes("RGB", [pix.width, pix.height], 
                        pix.samples)
                page_images_pil.append(img_pil)
                
                total_height += img_pil.height
                if page_num < len(doc) - 1: # Add padding for all but the last page
                    total_height += page_padding
                if img_pil.width > max_width:
                    max_width = img_pil.width
            doc.close()

            if not page_images_pil: 
                return

            # Store composite PIL image as an instance variable to keep it in memory
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



    # In execute_home, if it opens a PDF: This should be modifed now
    def execute_home(self):
        # Original: self.close_btn.configure(command=self.close_file)
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
        self.stack_var = tk.StringVar()
        stack_ops = ttk.OptionMenu(self.bottom_menu_frame, self.stack_var, 
                "Stack Ops")
        stack_ops.pack(side="left", padx=10, pady=5)
        stack_ops["menu"].add_command(label="Push", 
                command=lambda: self.widgets.setup_animation_ui("Push"))
        stack_ops["menu"].add_command(label="Pop", 
                command=lambda: self.widgets.setup_animation_ui("Pop"))
        stack_ops["menu"].add_command(label="New stack", 
                command=lambda: self.widgets.setup_animation_ui("New stack"))

        self.queue_var = tk.StringVar()
        queue_ops = ttk.OptionMenu(self.bottom_menu_frame, self.queue_var, 
                "Queue Ops")
        queue_ops.pack(side="left", padx=10, pady=5)
        queue_ops["menu"].add_command(label="Enqueue", 
                command=lambda: self.widgets.setup_animation_ui("Enqueue"))
        queue_ops["menu"].add_command(label="Dequeue", 
                command=lambda: self.widgets.setup_animation_ui("Dequeue"))
        queue_ops["menu"].add_command(label="New queue", 
                command=lambda: self.widgets.setup_animation_ui("New queue"))

    # --- Public API methods ---
    def clear_inputs(self):
        """Hide input frame and all input widgets."""
        for widget in (self.txt_label1, self.data_entry1,
                       self.setup_btn): widget.pack_forget()


    def show_single_input(self, var, label_text="Enter value"):
        """Show only one input field + setup button."""
        self.clear_inputs()
        self.txt_label1.config(text=label_text)
        self.txt_label1.pack(side="left", padx=5, pady=5)
        self.data_entry1.pack(side="left", padx=5, pady=5)
        if var == "Push":
            self.setup_btn.configure(text="Push")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var == "Enqueue":
            self.setup_btn.configure(text="Enqueue")
            self.setup_btn.pack(side="left", padx=10, pady=5)


    def show_no_input(self, var):
        """Show only setup button (no input required)."""
        self.clear_inputs()
        if var == "Pop":
            self.setup_btn.configure(text="Pop")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var == "New stack":
            self.setup_btn.configure(text="New stack")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var=="Dequeue":
            self.setup_btn.configure(text="Dequeue")
            self.setup_btn.pack(side="left", padx=10, pady=5)
        elif var == "New queue":
            self.setup_btn.configure(text="New queue")
            self.setup_btn.pack(side="left", padx=10, pady=5)

    def reset(self):
        """Clear inputs and reset dropdown selections."""
        self.clear_inputs()
        self.single_var.set("Single Input Ops")
        self.no_var.set("No Input Ops")


if __name__ == "__main__":
    App()


