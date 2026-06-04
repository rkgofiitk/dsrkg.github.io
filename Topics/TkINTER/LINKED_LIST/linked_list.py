import tkinter as tk
from linkedListOps import LinkedList # Import linked list class
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox as mb 
from array import array
import os
import fitz 
import time
from PIL import Image, ImageTk

# Create the main window
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Linked List Animation")
        self.geometry("850x750") # Display window

        self.delay = 10 # Default value
        self.widgets = LLAnimation(self) # Instance of widget class

        self.mainloop() 


class LLAnimation:
    def __init__(self, parent):

        # Initialization
        self.parent = parent 
        self.list_obj = LinkedList() 
        self.create_widgets()
        self.execute_home()

    # Defines menu and widgets for buttons, entries and labels 
    def create_widgets(self):

        # Background color
        self.bg_color = "#383839" 

        self.delay = 50 # Animation delay
        self.rect_positions = [] # List storing rectangle positions

        # Header frame for short title for the animation
        self.head_frame = tk.Frame(self.parent, bg=self.bg_color, 
                highlightbackground='white', highlightthickness=1)
        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.configure(height=50)

        # Title bar for the header frame
        self.title_lb = tk.Label(self.head_frame, text='Data structure:', 
                bg=self.bg_color, fg='white', font=('Bold', 20))
        self.title_lb.pack(side=tk.LEFT, padx=10)

        # Creates a subtitle 
        self.subtitle_lb = tk.Label(self.head_frame, 
                                    text='Linked List Animation', 
                                    bg=self.bg_color, fg='white', 
                                    font=('Regular', 15)
                                    )

        self.subtitle_lb.place(relx=0.35, rely=0.2)


        # Menu specitication in a separate class
        self.bottom_menu = BottomMenu(self.parent, self)

        # Define canvas frame and canvas
        self.canvas_display_frame = tk.Frame(self.parent)

        self.canvas = tk.Canvas(self.canvas_display_frame, bg="white")


        # Fix scrollbar sizes and placementts along the Canvas
        # Define a horizontal and vertical scrollbars
        self.v_scrollbar = ttk.Scrollbar(self.canvas_display_frame,
                orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self.canvas_display_frame, 
                orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, 
                xscrollcommand=self.h_scrollbar.set)
         
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, 
                xscrollcommand=self.h_scrollbar.set)

        # Text Widget (correct placement inside viewing window)
        self.text_widget = scrolledtext.ScrolledText(self.parent, wrap=tk.WORD,
                width=75, height=10)

        # Set window title
        self.parent.title("Linked List Animation")

        self.item_size = 30 # Define a size for items 

        self.text_to_rect = {}

        self.current_title = None # Initializations
        self.current_line1 = None
        self.current_line2 = None
        self.current_box = None

        # close Button for closing pdf viewer 
        self.close_btn = tk.Button(self.parent, text="Close", bg="#383839", 
                fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15), 
                command=lambda: self.close_current_view)
 
        # Home button is separately defined 
        self.home_btn = tk.Button(self.parent, text="Home", 
                font=('Regular', 15), bg=self.bg_color, fg="white", 
                activebackground=self.bg_color, activeforeground="white",
                command=lambda: self.execute_print)

    # Function for display of status messages
    def execute_status_message(self, message, x=200, y=320, color="blue"):
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
            self.canvas.itemconfig(text_id, text=message, fill=color)


    # Allows clearing of the message from the coordinate positions
    def clear_status_message(self, x=200, y=320):
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
            
        
    # Set up clears the recent screen and creates new screen for operation
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
        if var in ["Append", "Prepend", "Delete", "Find", "Remove"]:
            self.bottom_menu.show_single_input()
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.animate_command(var)
            )

        elif var in ["Copy", "Reverse", "Print List"]:
            self.bottom_menu.show_no_input()
            self.bottom_menu.setup_btn.configure(
                text=var, command=lambda: self.execute_command(var)
            )

        elif var == "Insert": # Insert at defined postion of list
            self.bottom_menu.show_two_inputs()
            self.bottom_menu.setup_btn.configure(
                text="Insert At", command=lambda: self.link_modify_insert()
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
            self.canvas.config(scrollregion=(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height()))
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
                                      command=self.execute_print, 
                                      bg="#383839", 
                                      fg="white"
                                     )

        # Make sure the button is enabled and has the correct command
        self.home_btn.configure(text="Home", 
                                command=lambda: self.execute_print(), 
                                state=tk.NORMAL
                                )

        # 6) Force geometry update so relx/rely calculations are correct
        #    (this ensures winfo_width/height are up-to-date)
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


    def animate_copy_list(self, qlist, tag="copy_list", color="blue"):
        # Traverse linked list and collect values
    
        spacing, rect_width, rect_height = 40, 50, 30
        start_x, start_y = 180, 100
        self.rect_positions = []

        def animate_node(i):
            if i >= len(qlist):
                # Draw NIL at the end
                if not self.rect_positions:
                    return
                nil_x = start_x + len(qlist)*(spacing+rect_width)
                nil_y = start_y
                self.draw_node(nil_x, nil_y, "NIL", rect_width, rect_height, tag, color="blue")
                last_x, last_y = self.rect_positions[-1]
                self.canvas.create_line(
                    last_x + rect_width//2, last_y,
                    nil_x, nil_y + rect_height//2,
                    width=2, fill="black", arrow="last", arrowshape=(10,15,5), tags=tag
                )
                return

            # Target position
            x = start_x + i * (spacing + rect_width)
            y = start_y
            start_y_anim = 340

            rect_id, text_id = self.draw_node(x, start_y_anim, qlist[i], rect_width, rect_height, tag, color="green")

            steps, dy, current_step = 20, (y - start_y_anim)/20, 0

            def animate_step():
                nonlocal current_step
                if current_step < steps:
                    self.canvas.move(rect_id, 0, dy)
                    self.canvas.move(text_id, 0, dy)
                    current_step += 1
                    self.canvas.after(50, animate_step)
                else:
                    # Replace with permanent node
                    self.canvas.delete(rect_id)
                    self.canvas.delete(text_id)
                    self.draw_node(x, y, qlist[i], rect_width, rect_height, tag, color="blue")
                    mid_x, mid_y = x+rect_width//2, y+rect_height//2
                    self.rect_positions.append((mid_x, mid_y))

                    # Arrow from previous node
                    if i > 0:
                        prev_x, prev_y = self.rect_positions[i-1]
                        self.canvas.create_line(
                            prev_x + rect_width//2, prev_y,
                            mid_x - rect_width//2, mid_y,
                            width=2, fill="black", arrow="last", arrowshape=(10,15,5), tags=tag
                        )

                    # Header update
                    first_x, first_y = self.rect_positions[0]
                    head_x = first_x - rect_width//2 - spacing
                    head_y = first_y
                    self.canvas.delete("header")
                    self.canvas.create_text(head_x-10, head_y-58,
                                            text="head", font=('Bold',15), tags="header")
                    self.canvas.create_line(head_x-10, head_y-45,
                                            head_x-10, head_y,
                                            fill="black", width=3, tags="header")
                    self.canvas.create_line(head_x-10, head_y,
                                            first_x - rect_width//2, head_y,
                                            fill="black", width=3,
                                            arrow="last", arrowshape=(10,15,5), tags="header")

                    # Next node
                    self.canvas.after(300, lambda: animate_node(i+1))

            animate_step()

        animate_node(0)



           


    def draw_node(self, x, y, val, rect_width=50, rect_height=30, tag="linkedlist", color="blue"):
        rect_id = self.canvas.create_rectangle(
            x, y, x+rect_width, y+rect_height,
            fill=color, tags=tag
        )
        text_id = self.canvas.create_text(
            x+rect_width//2, y+rect_height//2,
            text=str(val), fill="white", font=('Bold', 15), tags=tag
        )
        return rect_id, text_id




    # Draws the current linked list on the canvas
    def draw_linked_list(self):

        # Keep canvas frame visible
        self.canvas_display_frame.pack(padx=10, pady=(50,75), 
                                       fill=tk.BOTH, 
                                       expand=True
                                      )

         # Clear only linked list drawings, not everything
        self.canvas.delete("linkedlist")

        qlist = self.list_obj.to_list()
        size = self.list_obj.length()

        # Specification for items
        item_width = 50
        spacing = 45
        x_start = 50
        y_start = 270
        y_end = 300

        for i, val in enumerate(qlist):
            x1 = x_start + i * (self.item_size + spacing)
            x2 = x1 + item_width

            # Node rectangle + text
            rect = self.canvas.create_rectangle(x1, y_start, x2, y_end,
                    fill="blue", tags=("linkedlist", f"block_{i}"))
            self.canvas.create_text((x1+x2)//2, (y_start+y_end)//2,
                    text=str(val), font=('Bold', 15), fill="white",
                    tags=("linkedlist", f"text_{i}"))

            self.text_to_rect[str(val)] = rect

            # Arrow to next node
            if i < size-1:
                self.canvas.create_line(x2, (y_start+y_end)//2, x2+30,
                        (y_start+y_end)//2, fill="black", width=3,
                        arrow="last", arrowshape=(10,15,5),
                        tags=("linkedlist", f"arrow_{i}"))

        # NIL tail
        x_next = x_start + (self.item_size + spacing) * size
        self.canvas.create_rectangle(x_next, y_start, x_next+50, y_end,
                fill="blue", tags=("linkedlist", "tail"))
        self.canvas.create_text(x_next+25, (y_start+y_end)//2, text="NIL",
                font=("Arial", 15), fill="white", tags=("linkedlist", "tail_text"))
        if size > 0:
            last_x2 = x_start + (size-1) * (self.item_size + spacing) + item_width
            self.canvas.create_line(last_x2, (y_start+y_end)//2, x_next,
                                    (y_start+y_end)//2, fill="black", width=3,
                                    arrow="last", arrowshape=(10,15,5),
                                    tags=("linkedlist", "nil_arrow"))

        # Header pointer
        self.canvas.create_rectangle(x_start-40, y_start-100, x_start-10,
                y_start-75, fill="white", tags=("linkedlist", "header"))
        self.canvas.create_line(x_start-25, y_start-85, x_start-25, y_start+15,
                fill="black", width=3, tags=("linkedlist", "header_line1"))
        self.canvas.create_line(x_start-25, y_start+15, x_start, y_start+15,
                fill="black", width=3, arrow="last", arrowshape=(10,15,5),
                tags=("linkedlist", "header_line2"))
        self.canvas.create_text(x_start-20, y_start-110, text="head",
                font=("Arial", 15), tags=("linkedlist", "header_text"))


    # Animate command separates out the operations and modifies links
    # for animating the actual logic behind the operation
    def animate_command(self, var):

        #self.clear_reverse_list()


        if  var == "Append": 
            self.link_modify_append()
        elif var == "Prepend":
            self.link_modify_prepend()
        elif var == "Delete":
            self.link_modify_delete()
        elif var == "Find":
            self.execute_find()
        else:
            print("Invalid command")
            self.show_status_message("Invalid command", color="red") 
             

    def animate_reverse_list(self, reversed_nodes, tag="reverse_list"):
        spacing, rect_width, rect_height = 40, 50, 30
        start_x, start_y = 180, 100
        self.rect_positions = []

        def animate_node(i):
            if i >= len(reversed_nodes):
                # Draw NIL at the end
                if not self.rect_positions:
                    return
                nil_x = start_x + len(reversed_nodes)*(spacing+rect_width)
                nil_y = start_y
                self.draw_node(nil_x, nil_y, "NIL", rect_width, rect_height, tag, color="blue")
                last_x, last_y = self.rect_positions[-1]
                self.canvas.create_line(
                    last_x + rect_width//2, last_y,
                    nil_x, nil_y + rect_height//2,
                    width=2, fill="black", arrow="last", arrowshape=(10,15,5), tags=tag
                )
                return

            # Target position
            x = start_x + i * (spacing + rect_width)
            y = start_y
            start_y_anim = 340

            rect_id, text_id = self.draw_node(x, start_y_anim, reversed_nodes[i], rect_width, rect_height, tag, color="green")

            steps, dy, current_step = 20, (y - start_y_anim)/20, 0

            def animate_step():
                nonlocal current_step
                if current_step < steps:
                    self.canvas.move(rect_id, 0, dy)
                    self.canvas.move(text_id, 0, dy)
                    current_step += 1
                    self.canvas.after(50, animate_step)
                else:
                    # Replace with permanent node
                    self.canvas.delete(rect_id)
                    self.canvas.delete(text_id)
                    self.draw_node(x, y, reversed_nodes[i], rect_width, rect_height, tag, color="blue")
                    mid_x, mid_y = x+rect_width//2, y+rect_height//2
                    self.rect_positions.append((mid_x, mid_y))

                    # Arrow from previous node
                    if i > 0:
                        prev_x, prev_y = self.rect_positions[i-1]
                        self.canvas.create_line(
                            prev_x + rect_width//2, prev_y,
                            mid_x - rect_width//2, mid_y,
                            width=2, fill="black", arrow="last", arrowshape=(10,15,5), tags=tag
                        )

                    # Header update
                    first_x, first_y = self.rect_positions[0]
                    head_x = first_x - rect_width//2 - spacing
                    head_y = first_y
                    self.canvas.delete("header")
                    self.canvas.create_text(head_x-10, head_y-58,
                                            text="head", font=('Bold',15), tags="header")
                    self.canvas.create_line(head_x-10, head_y-45,
                                            head_x-10, head_y,
                                            fill="black", width=3, tags="header")
                    self.canvas.create_line(head_x-10, head_y,
                                            first_x - rect_width//2, head_y,
                                            fill="black", width=3,
                                            arrow="last", arrowshape=(10,15,5), tags="header")

                    # Next node
                    self.canvas.after(300, lambda: animate_node(i+1))

            animate_step()

        animate_node(0)



    # Find operation finds an element in the linked list
    def execute_find(self):
        self.clear_all_status()   # clear old "Found" messages

        user_input = self.bottom_menu.data_entry1.get()

        if not user_input.isnumeric():
            self.execute_status_message("Invalid input, not a number", color="red")
            self.bottom_menu.data_entry1.delete(0, tk.END)
            return

        val = int(user_input)
        index = self.list_obj.search(val)

        if index == -1:
            self.bottom_menu.data_entry1.delete(0, tk.END)
            msg = "Item " + user_input + " not in list"
            self.execute_status_message(msg, color="red")
            return

        # Compute coordinates for the found node
        spacing, rect_width, rect_height = 45, 50, 30
        x_start = 50 + (index-1) * (rect_width + spacing)
        y_start = 270

        # Draw the node with highlight
        rect_id, text_id = self.draw_node(x_start, y_start, val, rect_width, rect_height, tag="found_node")
        self.canvas.itemconfig(rect_id, fill="green")

        # Animate upward movement
        def move_up():
            rect_coords = self.canvas.coords(rect_id)
            text_coords = self.canvas.coords(text_id)

            if rect_coords and text_coords and rect_coords[1] > 200:
                self.canvas.move(rect_id, 0, -5)
                self.canvas.move(text_id, 0, -5)
                self.parent.after(50, move_up)
            else:
                # Delete node after animation
                self.canvas.delete(rect_id)
                self.canvas.delete(text_id)

                # Status message
                self.canvas.create_rectangle(250, 125, 300, 155, fill="blue", tags="status_message")
                self.canvas.create_text(200, 140, text="Found", fill="blue", font=('Bold', 15), tags="status_message")
                self.canvas.create_text(275, 140, text=str(val), fill="white", font=('Bold', 15), tags="status_message")

        move_up()
        self.bottom_menu.data_entry1.delete(0, tk.END)


    # Append inserts the input at the end of the list
    def link_modify_append(self):

        self.clear_all_status() 

        user_input = self.bottom_menu.data_entry1.get()  
        self.draw_linked_list()
        if user_input.isnumeric(): 
            value = int(user_input)
            spacing = 45 

            success = self.list_obj.append(value)

            if not success:
                y_start = 100
                y_end = y_start + 30 
                print("length of list =", self.list_obj.length())
                x_start = 50 + (self.list_obj.length()-1) * (self.item_size + spacing)
                x_end = x_start + 50

                rect_id = self.canvas.create_rectangle(x_start, y_start, 
                                                       x_end, y_end, 
                                                       fill="green"
                                                      )
                text_id = self.canvas.create_text(x_start + 25, 
                                                  (y_start+y_end)//2, 
                                                  text=str(value), 
                                                  fill="white", 
                                                  font=('Bold', 15)
                                                 )
                self.text_to_rect[user_input] = rect_id

                def move_down():
                    """Moves the rectangle downward"""
                    current_coords = self.canvas.coords(rect_id)
                    if current_coords[1] < 200: 
                        self.canvas.move(rect_id, 0, 5)
                        self.canvas.move(text_id, 0, 5)
                        self.parent.after(50, move_down)
                    else:
                        self.canvas.delete(rect_id)
                        self.canvas.delete(text_id)
                        self.draw_linked_list()
                move_down()
                self.bottom_menu.data_entry1.delete(0, tk.END)

                # Create a status of successful apepend 
                msg = "Appended " + str(value) + " successfully" 
                self.execute_status_message(msg, color="green")

        else:
            self.bottom_menu.data_entry1.delete(0, tk.END)
            msg="Linked list full, append failed"
            self.execute_status_message(msg, color="red")



    # Prepend inserts the input at the beginning of the list
    def link_modify_prepend(self):

        self.clear_all_status()

        user_input = self.bottom_menu.data_entry1.get()  
        self.draw_linked_list()
        if user_input.isnumeric(): 
            value = int(user_input)
            spacing = 45 

            success = self.list_obj.prepend(value)

            if not success:
                y_start = 100
                y_end = y_start + 30 
                print("length of list =", self.list_obj.length())
                x_start = 50 
                x_end = x_start + 50

                rect_id = self.canvas.create_rectangle(x_start, y_start, x_end, 
                        y_end, fill="green")
                text_id = self.canvas.create_text(x_start + 25, 
                        (y_start+y_end)//2, text=str(value), fill="white", 
                        font=('Bold', 15))
                self.text_to_rect[user_input] = rect_id

                def move_down():
                    """Moves the rectangle downward"""
                    current_coords = self.canvas.coords(rect_id)
                    if current_coords[1] < 200: 
                        self.canvas.move(rect_id, 0, 5)
                        self.canvas.move(text_id, 0, 5)
                        self.parent.after(50, move_down)
                    else:
                        self.canvas.delete(rect_id)
                        self.canvas.delete(text_id)
                        self.draw_linked_list()
                move_down()
                self.bottom_menu.data_entry1.delete(0, tk.END)

                msg = "Prpended " + str(value) + " successfully" 
                self.execute_status_message(msg, color="green")

        else:
            msg="Linked list full, append failed"
            self.execute_status_message(msg, color="red")

    # Filters rectangle for corresponding text fields
    def find_rectangle_by_text(self,text):
        rect_id = self.text_to_rect.get(text)
        if rect_id:  
            self.canvas.itemconfig(rect_id, outline="red", width=3) 
            print(f"Rectangle found for text ID {text}: {rect_id}")
            return rect_id
        else:
            print("No rectangle found for this text ID.")
            return None

    def move_up(self, rect_id, text_id, x_end):
        def step():
            coords = self.canvas.coords(rect_id)
            x, y = coords[0], coords[1]

            if y > 100:
                self.canvas.move(rect_id, 0, -5)
                self.canvas.move(text_id, 0, -5)

            self.parent.after(50, step)

        step()

    # Creates movement to right
    def move_right(self, rect_id, text_id, x_end):
        def step():
            coords = self.canvas.coords(rect_id)
            x, y = coords[0], coords[1]

            if x < x_end:
                self.canvas.move(rect_id, 5, 0)
                self.canvas.move(text_id, 5, 0)

            self.parent.after(50, step)

        step()

    def clear_find_status(self):
        self.canvas.delete("find_status")

    def clear_copy_list(self):
        self.canvas.delete("copy_list")   # consistent tag
        self.clear_header_and_status()

    def clear_reverse_list(self):
        self.canvas.delete("reverse_list")  # consistent tag
        self.clear_header_and_status()

    def clear_header_and_status(self):
        self.canvas.delete("status_message")
        self.canvas.delete("header")

    def clear_all_status(self):
        self.clear_find_status()
        self.clear_reverse_list()
        self.clear_copy_list()
        self.clear_status_message(200, 320)
        self.clear_status_message(200, 150)


        
    def execute_command(self,var):
        self.clear_all_status()

        if var == "Copy":
            tmp = self.list_obj.head
            qlist = []
            while tmp:
                qlist.append(tmp.data)
                tmp = tmp.next
            self.animate_copy_list(qlist)

            self.execute_status_message("Duplicate list", x=200, y=150, color="green") 
            self.execute_status_message("Original list") 
            return

        if var == "Reverse":
            #self.execute_reverse()
            tmp = self.list_obj.reverse()
            rev_list = [] 
            print(rev_list)
            #reversed_nodes = []
            while tmp:
                rev_list.append(tmp.data)
                tmp = tmp.next
            
            self.animate_reverse_list(rev_list) 

           # self.animate_reverse_list(reversed_nodes)
            self.execute_status_message("Original list") 
            self.execute_status_message("Reverse list", x=200, y=150, color="green") 
            return

        else:
            list_len = len(self.list_obj.to_list())
            self.execute_print()
            msg = "Current linked list has " + str(list_len) + " elements"
            self.execute_status_message(msg)
            return

    def execute_print(self):
        if self.home_btn.winfo_ismapped():
            self.home_btn.place_forget()
            self.execute_status_message("List is empty")
        self.draw_linked_list()
        

    # Modifies links to delete the required element
    def link_modify_delete(self):
        self.clear_all_status()

        user_input = self.bottom_menu.data_entry1.get()  
        print("Entered :", user_input)

        self.draw_linked_list()

        if not user_input.isnumeric(): 
            self.execute_status_message("Invalid input", color="red")
            self.bottom_menu.data_entry1.delete(0, tk.END)
            return

        val = int(user_input)

        # No need for `if val == -1` here

        all_items = self.canvas.find_all()
        text_id = None
        for item in all_items:
            if self.canvas.type(item) == "text":
                if self.canvas.itemcget(item, "text") == user_input:
                    text_id = item

        rect_id = self.find_rectangle_by_text(user_input)

        index = self.list_obj.search(val)
        if index == -1:
            self.bottom_menu.data_entry1.delete(0, tk.END)
            msg = f"Item {user_input} not in list"
            self.execute_status_message(msg, color="red")
            return

        spacing = 45 
        x_start = 50 + (index-1) * (self.item_size + spacing)
        y_start = 310

        self.list_obj.delete(val)

        if rect_id and text_id:
            self.canvas.itemconfig(rect_id, fill="green")

            def move_up():
                rect_coords = self.canvas.coords(rect_id)
                text_coords = self.canvas.coords(text_id)

                if rect_coords and text_coords and rect_coords[1] > 100:
                    self.canvas.move(rect_id, 0, -5)
                    self.canvas.move(text_id, 0, -5)
                    self.parent.after(50, move_up)
                else:
                    self.canvas.delete(rect_id)
                    self.canvas.delete(text_id)
                    print(f"Deleted: {val}")
                    self.draw_linked_list()

            move_up()
            self.bottom_menu.data_entry1.delete(0, tk.END)
            msg = f"Deleted {val} successfully"
            self.execute_status_message(msg, color="green")
        else:
            msg = f"Item {val} not in list, delete failed"
            self.execute_status_message(msg, color="red")


    # Modifies links to insert a new element at a chosen position
    def link_modify_insert(self):

        self.clear_all_status()

        user_input1 = self.bottom_menu.data_entry1.get()  
        user_input2 = self.bottom_menu.data_entry2.get()  

        self.draw_linked_list()

        if user_input1.isnumeric() and user_input2.isnumeric(): 
            value = int(user_input1)
            pos = int(user_input2)

            success = self.list_obj.insertAt(value, pos)
            if success == -1:
                self.bottom_menu.data_entry1.delete(0, tk.END)
                self.bottom_menu.data_entry2.delete(0, tk.END)
                msg="Invalid position, enter valid position try again"
                self.execute_status_message(msg, color="red")
                return
            if success == -2:
                self.bottom_menu.data_entry1.delete(0, tk.END)
                self.bottom_menu.data_entry2.delete(0, tk.END)
                msg="Invalid position, insertion failed"
                self.execute_status_message(msg, color="red")
                return

            if not success:
                spacing = 45 
                y_start = 100
                y_end = y_start + 30 
                #print("length of list =", self.list_obj.length())
                x_start = 50 + (pos - 1) * (self.item_size + spacing) + 30
                x_end = x_start + 50

                rect_id = self.canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="green")
                text_id = self.canvas.create_text(x_start + 25, (y_start+y_end)//2, text=str(value), fill="white", font=('Bold', 15))
                self.text_to_rect[user_input1] = rect_id

                def move_down():
                    """Moves the rectangle downward"""
                    current_coords = self.canvas.coords(rect_id)
                    if current_coords[1] < 200: 
                        self.canvas.move(rect_id, 0, 5)
                        self.canvas.move(text_id, 0, 5)
                        self.parent.after(50, move_down)
                    else:
                        self.draw_linked_list()
                        self.canvas.delete(rect_id)
                        self.canvas.delete(text_id)

                move_down()


                self.bottom_menu.data_entry1.delete(0, tk.END)
                self.bottom_menu.data_entry2.delete(0, tk.END)

                msg = "Inserted " + str(value) + " at position " + str(pos) + " successfully"
                self.execute_status_message(msg, color="green")
        else:
            msg="Linked list full, insertion failed"
            self.execute_status_message(msg, color="red")

            return


    def open_pdf(self, fx):
        self.clear_main_content_area() # Hide other content first
        if self.home_btn.winfo_ismapped():
            self.home_btn.place_forget()

        # Make the canvas frame visible for PDF display
        self.canvas_display_frame.pack(padx=10, pady=(10,75), fill=tk.BOTH, expand=True) # pady bottom for close_btn
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

            # Store composite PIL image as an instance variable
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
        
        self.close_btn.place(relx=0.5, rely=0.85, anchor=tk.S) 
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
        self.txt_label1 = tk.Label(self.input_frame, text="Enter value", font=('Regular', 15))
        self.data_entry2 = tk.Entry(self.input_frame, width=20)
        self.txt_label2 = tk.Label(self.input_frame, text="Enter position", font=('Regular', 15))

        #self.txt_label1 = tk.Label(self.input_frame, text="Enter value", bg="#2E2E2E", fg="white")
        #self.data_entry1 = tk.Entry(self.input_frame, width=15)
        #self.txt_label2 = tk.Label(self.input_frame, text="Enter position", bg="#2E2E2E", fg="white")
        #self.data_entry2 = tk.Entry(self.input_frame, width=15)
        #self.setup_btn = tk.Button(self.input_frame, text="", bg="#383839", fg="white")
        self.setup_btn = tk.Button(self.input_frame, text="", 
                font=('Regular', 15), bg=self.bg_color, fg="white", 
                activebackground=self.bg_color, activeforeground="white" )


        # Dropdowns in bottom menu
        self.single_var = tk.StringVar()
        single_ops = ttk.OptionMenu(self.bottom_menu_frame, self.single_var, "Single Input Ops")
        single_ops.pack(side="left", padx=10, pady=5)
        single_ops["menu"].add_command(label="Append", command=lambda: self.widgets.setup_animation_ui("Append"))
        single_ops["menu"].add_command(label="Prepend", command=lambda: self.widgets.setup_animation_ui("Prepend"))
        single_ops["menu"].add_command(label="Remove", command=lambda: self.widgets.setup_animation_ui("Delete"))
        single_ops["menu"].add_command(label="Find", command=lambda: self.widgets.setup_animation_ui("Find"))

        self.no_var = tk.StringVar()
        no_ops = ttk.OptionMenu(self.bottom_menu_frame, self.no_var, "No Input Ops")
        no_ops.pack(side="left", padx=10, pady=5)
        no_ops["menu"].add_command(label="Copy", command=lambda: self.widgets.setup_animation_ui("Copy"))
        no_ops["menu"].add_command(label="Reverse", command=lambda: self.widgets.setup_animation_ui("Reverse"))
        no_ops["menu"].add_command(label="Print List", command=lambda: self.widgets.setup_animation_ui("Print List"))
        #no_ops["menu"].add_command(label="Copy", command=lambda: self.widgets.setup_animation_ui("Copy"))

        self.two_var = tk.StringVar()
        two_ops = ttk.OptionMenu(self.bottom_menu_frame, self.two_var, "Two Input Ops")
        two_ops.pack(side="left", padx=10, pady=5)
        two_ops["menu"].add_command(label="Insert", command=lambda: self.widgets.setup_animation_ui("Insert"))


    # --- Public API methods ---
    def clear_inputs(self):
        """Hide input frame and all input widgets."""
        for widget in (self.txt_label1, self.data_entry1, self.txt_label2, self.data_entry2, self.setup_btn):
            widget.pack_forget()

    def ensure_canvas(self):
        if not hasattr(self, "canvas"):
            self.canvas = tk.Canvas(self.parent, bg="white")
            # pack canvas before footer
            self.canvas.pack(side="top", fill="both", expand=True)


    

    def show_single_input(self, label_text="Enter value"):
        """Show only one input field + setup button."""
        self.clear_inputs()
        self.txt_label1.config(text=label_text)
        self.txt_label1.pack(side="left", padx=5, pady=5)
        self.data_entry1.pack(side="left", padx=5, pady=5)
        self.setup_btn.pack(side="left", padx=10, pady=5)

    def show_two_inputs(self, label1="Enter value", label2="Enter position"):
        """Show two input fields + setup button."""
        self.clear_inputs()
        self.txt_label1.config(text=label1)
        self.txt_label1.pack(side="left", padx=5, pady=5)
        self.data_entry1.pack(side="left", padx=5, pady=5)
        self.txt_label2.config(text=label2)
        self.txt_label2.pack(side="left", padx=5, pady=5)
        self.data_entry2.pack(side="left", padx=5, pady=5)
        self.setup_btn.pack(side="left", padx=10, pady=5)

    def show_no_input(self):
        """Show only setup button (no input required)."""
        self.clear_inputs()
        self.setup_btn.pack(side="left", padx=100, pady=5)

    def reset(self):
        """Clear inputs and reset dropdown selections."""
        self.clear_inputs()
        self.single_var.set("Single Input Ops")
        self.no_var.set("No Input Ops")
        self.two_var.set("Two Input Ops")


if __name__ == "__main__":
    App()


