import tkinter as tk
from linkedListOps import LinkedList # Import your Stack class
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
        self.geometry("750x750") # Display window

        self.delay = 10 # Default value
        self.widgets = LLAnimation(self) # Instance of widget class

        self.mainloop() 


class LLAnimation:
    def __init__(self, parent):
        self.parent = parent 
        self.list_obj = LinkedList()  # Initialize stack

        self.create_widgets()
        self.toggle_menu_frame = None
        
        self.execute_home()


    def create_widgets(self):
        self.bg_color = "#383839" # Define widget background color

        self.delay = 50
        self.rect_positions = []
        # Header frame
        self.head_frame = tk.Frame(self.parent, bg=self.bg_color, 
                highlightbackground='white', highlightthickness=1)
        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.configure(height=50)

        # Title bar for the header frame
        self.title_lb = tk.Label(self.head_frame, text='Data structure:', 
                bg=self.bg_color, fg='white', font=('Bold', 20))
        self.title_lb.pack(side=tk.LEFT, padx=10)

        self.subtitle_lb = tk.Label(self.head_frame, text='Linked List Animation', 
                bg=self.bg_color, fg='white', font=('Regular', 15))
        self.subtitle_lb.place(relx=0.35, rely=0.2)

        # Toggle button for side menubar expansion and collapse 
        self.toggle_btn = tk.Button(self.head_frame, text='≡', bg=self.bg_color,
                fg='white', font=('Bold', 20), bd=0, 
                activebackground=self.bg_color, activeforeground='white', 
                command=self.toggle_menu)
        self.toggle_btn.pack(side=tk.RIGHT)


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

        # Define input frame for accepting user input
        self.input_frame = tk.Frame(self.parent)
        self.input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)


        self.data_entry1 = tk.Entry(self.input_frame, width=20)
        self.txt_label1 = tk.Label(self.input_frame, text="Enter value", font=('Regular', 15))
        self.data_entry2 = tk.Entry(self.input_frame, width=20)
        self.txt_label2 = tk.Label(self.input_frame, text="Enter position", font=('Regular', 15))

        # Stack and queue operation buttons: enguque, pop, push and dequeue
        self.setup_btn = tk.Button(self.input_frame, text="", 
                font=('Regular', 15), bg=self.bg_color, fg="white", 
                activebackground=self.bg_color, activeforeground="white" )

        # Home button
        self.home_btn = tk.Button(self.input_frame, text="Home", 
                font=('Regular', 15), bg=self.bg_color, fg="white", 
                activebackground=self.bg_color, activeforeground="white" )

        # Close Button for closing pdf viewer 
        self.close_btn = tk.Button(self.parent, text="Close", bg="#383839", 
                fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15), 
                command=lambda: self.close_current_view)

        # Set window title
        self.parent.title("Linked List Animation")

        self.item_size = 30 # Define a size for items 

        self.text_to_rect = {}

        self.current_title = None
        self.current_line1 = None
        self.current_line2 = None
        self.current_box = None

    # Function to expand/collapse sidebar frame, initially collapsed
    # For expanding click on expand icon
    def toggle_menu(self):
        if self.toggle_menu_frame and self.toggle_menu_frame.winfo_ismapped():
            self.toggle_menu_frame.place_forget() 
            self.toggle_btn.config(text='≡') 
        else:
            if not self.toggle_menu_frame: 
                self.toggle_menu_frame = tk.Frame(self.parent, bg=self.bg_color)
                SidebarMenu(self.parent, self) 

            # Toggle sidebar menu
            self.toggle_menu_frame.place(relx=0.7, y=50,
                    height=self.parent.winfo_height(),
                    relwidth=0.3) 
            # Update to close button icon 
            self.toggle_btn.config(text='X')  


    # Clear contents before displaying new fields, text, buttons, etc.
    def clear_main_content_area(self):
        '''Hides all main content widgets, input fields, and specific 
        labels/buttons.'''

        if self.canvas_display_frame.winfo_ismapped():
            self.canvas_display_frame.pack_forget()
        if self.input_frame.winfo_ismapped():
            self.input_frame.pack_forget()

        if self.text_widget.winfo_ismapped():
            self.text_widget.pack_forget()
        
        #self.canvas_label.place_forget()
        self.data_entry1.place_forget()
        self.txt_label1.place_forget()

        self.data_entry2.place_forget()
        self.txt_label2.place_forget()
  
        if self.setup_btn.winfo_ismapped(): # Main action button 
            self.setup_btn.place_forget()
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()
        if self.home_btn.winfo_ismapped():
            self.home_btn.place_forget()
        
        
    # Set up requires clearing screen and setting up new screen for operation
    def setup_animation_ui(self, var):
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()
        if self.home_btn.winfo_ismapped():
            self.home_btn.place_forget()
        self.input_frame.pack_forget()  # Remove existing packing
        self.canvas_display_frame.pack_forget()  # Remove existing packing

        self.input_frame.pack(fill=tk.X, padx=10, pady=5)  
        self.canvas_display_frame.pack(padx=10, pady=(50,75), fill=tk.BOTH, expand=True)


        # Define two sets of operations one for stack another fore queue
        if var in ["Append", "Prepend", "Delete", "Find"]: # Only map push and pop buttons
            self.data_entry1.grid_forget()
            self.data_entry2.grid_forget()
            self.txt_label1.grid_forget()
            self.txt_label2.grid_forget()

            self.txt_label1.grid(row=0,column=0, pady=5,padx=5)
            self.data_entry1.grid(row=0, column=1, pady=5,padx=5)
            self.setup_btn.grid(row=0, column=2, pady=5,padx=5)
            self.setup_btn.configure(text=f"{var}", command=lambda: self.animate_command(var))

        if var in ["Reverse", "Print List"]: # Only map Reverse button
            self.setup_btn.grid(row=0,column=0, padx=100, pady=10)
            self.setup_btn.configure(text=f"{var}", command=lambda: self.execute_command(var))
            self.data_entry1.grid_forget()
            self.data_entry2.grid_forget()
            self.txt_label1.grid_forget()
            self.txt_label2.grid_forget()

        if var == "Insert": # Only map Reverse button

            self.txt_label1.grid(row=0, column=0, padx=5, pady=0) 
            self.data_entry1.grid(row=0, column=1, padx=5, pady=0) 

            self.txt_label2.grid(row=1, column=0, padx=5, pady=0)
            self.data_entry2.grid(row=1, column=1, padx=5, pady=0)

            self.setup_btn.grid(row=0, column=2, rowspan=2, padx=15, pady=10)
            self.setup_btn.configure(text="Insert At", command=lambda: self.link_modify_insert())


        
        self.parent.update_idletasks()
        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1: canvas_width = 600
        if canvas_height <= 1: canvas_height = 500


    def close_current_view(self):
        '''Clears the current view (PDF, Text, Animation Input/Setup) and 
           associated resources.'''
        
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
        if self.home_btn.winfo_ismapped():
            self.home_btn.place_forget()
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()
        
        # Optionally, show a default view or home screen elements
        #self.execute_home() # I have a problem here to be fixed 
        self.home_btn.configure(text="Home",command=lambda: self.execute_home())
        self.home_btn.place(relx=0.5,y=170)


    def draw_linked_list(self):

        self.canvas_display_frame.pack(padx=10, pady=(50,75), fill=tk.BOTH,
                expand=True)
        self.canvas.delete("all")

        #if not self.list_obj.isEmpty():
        qlist = self.list_obj.to_list()
        size = self.list_obj.length()
        print("Size of list =", size)

        item_width = 50
        spacing = 45
        x_start = 50
        y_start = 270
        y_end = 300


        for i, val in enumerate(qlist):
            x1 = x_start +  i * (self.item_size + spacing)
            x2 = x1 + item_width

            # Draw rectangle
            rect = self.canvas.create_rectangle(x1, y_start, x2, y_end, fill="blue",
                        tags=f"block_{i}")
            # Draw text
            self.canvas.create_text((x1+x2)//2, (y_start+y_end)//2,
                    text=str(val), font=('Bold', 15),  fill="white", 
                    tags=f"text_{i}")
            self.text_to_rect[str(val)] = rect
            self.canvas.create_line(x1+50, (y_start+y_end)//2, x2, 
                (y_start+y_end)//2, fill="black", width=3, arrow="first")


            if i <= size:
                self.canvas.create_line(x2, (y_start + y_end) // 2, x2+30, 
                        (y_start + y_end) // 2, fill="black", width=3, 
                        arrow="last", arrowshape=(10,15,5))

        # Display "None" at the end of the list
        x_next = x_start + (self.item_size + spacing) * size 
        self.canvas.create_rectangle(x_next, y_start, x_next+50, y_end, 
                fill="blue", tags=f"tail")
        self.canvas.create_text(x_next + 25, (y_start + y_end) // 2, text="NIL", 
                font=("Arial", 15), fill="white")

        self.canvas.create_rectangle(x_start-40, y_start-100, x_start-10, 
                y_start-75, fill="white", tags=f"header")
        self.canvas.create_line(x_start-25, y_start-85, x_start-25,  y_start+15,
                fill="black", width=3) #, ast", arrowshape=(10,15,5))
        self.canvas.create_line(x_start-25, y_start+15, x_start,  y_start+15,
                fill="black", width=3, arrow="last", arrowshape=(10,15,5))

        self.canvas.create_text(x_start - 20, y_start-110, text="head", 
                font=("Arial", 15)) 






    def animate_command(self, var):

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
            mb.showerror(title="Invalid command", message="Give correct command")
             


    def execute_find(self):
        user_input = self.data_entry1.get()  

        self.draw_linked_list()
        if not user_input.isnumeric(): 
            mb.showerror(title="Invalid input", message="Enter a number")
            self.data_entry1.delete(0, tk.END)
            return

        val = int(user_input)

        if val == -1:
            self.draw_linked_list()
            self.data_entry1.delete(0, tk.END)
            mb.showerror(title="Invalid Input", message="Value not found")
            return
        else:
            all_items = self.canvas.find_all()
            for item in all_items:
                if self.canvas.type(item) == "text":
                    if self.canvas.itemcget(item, "text") == user_input:
                        text_id = item

            rect_id = self.find_rectangle_by_text(user_input)

            index = self.list_obj.search(val)
            if index == -1:
                self.data_entry1.delete(0, tk.END)
                mb.showerror(title="Invalid input", message="Enter an item in list")
            
                return
            spacing = 45 
            x_start = 50 + (index-1) * (self.item_size + spacing)
            y_start = 310

            if rect_id and text_id:
                self.canvas.itemconfig(rect_id, fill="green")
                def move_up():
                    rect_coords = self.canvas.coords(rect_id)
                    text_coords = self.canvas.coords(text_id)

                    if rect_coords and text_coords and rect_coords[1] > 200:
                        self.canvas.move(rect_id, 0, -5) # Move block
                        self.canvas.move(text_id, 0, -5)  # Move text 
                        self.parent.after(50, move_up) # Move effect on canvas 
                    else:
                        self.canvas.delete(rect_id)  # Remove rectangle
                        self.canvas.delete(text_id)   # Remove text
                        print(f"Found: {val}") # Print on console
                        self.draw_linked_list() # Draw queue after deletion
                        self.canvas.create_rectangle(250, 125, 300, 155, fill="blue")
                        self.canvas.create_text(200, 140, text="Found", fill="blue", font=('Bold', 15))
                        self.canvas.create_text(275, 140, text=str(val), fill="white", font=('Bold', 15))

                move_up()
                self.data_entry1.delete(0, tk.END)
            else:
                mb.showerror(title = "wrong rect_id", message = "Delete failed")
                print("rect_id = ", rect_id, "text_id = ", text_id)


    def link_modify_append(self):

        user_input = self.data_entry1.get()  
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

                rect_id = self.canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="green")
                text_id = self.canvas.create_text(x_start + 25, (y_start+y_end)//2, text=str(value), fill="white", font=('Bold', 15))
                self.text_to_rect[user_input] = rect_id

                def move_down():
                    """Moves the rectangle downward"""
                    current_coords = self.canvas.coords(rect_id)
                    if current_coords[1] < 200: 
                        self.canvas.move(rect_id, 0, 5)
                        self.canvas.move(text_id, 0, 5)
                        self.parent.after(50, move_down)
                    else:
                        self.draw_linked_list()
                move_down()
                self.data_entry1.delete(0, tk.END)

        else:
            self.data_entry1.delete(0, tk.END)
            mb.showerror(title="Linked list full", message="Append failed")

    def link_modify_prepend(self):

        user_input = self.data_entry1.get()  
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
                        self.draw_linked_list()
                move_down()
                self.data_entry1.delete(0, tk.END)

        else:
            mb.showerror(title="Linked list full", message="prepend failed")

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

    def move_right(self, rect_id, text_id, x_end):
        def step():
            coords = self.canvas.coords(rect_id)
            x, y = coords[0], coords[1]

            if x < x_end:
                self.canvas.move(rect_id, 5, 0)
                self.canvas.move(text_id, 5, 0)

            self.parent.after(50, step)

        step()

    def move_rectangles(self, list_array, index=0):
        if index >= len(list_array):
            return

        spacing = 30
        rect_width = 50
        rect_height = 30


        # Final position relative to NIL box
        target_x = 180 + index * (spacing + rect_width)
        target_y = 100

        # Start position (off-screen or lower)
        start_x = target_x
        start_y = 340

         # Create rectangle and text at start position
        rect_id = self.canvas.create_rectangle(start_x, start_y, start_x + 
                rect_width, start_y + rect_height, fill="green")
        text_id = self.canvas.create_text(start_x + rect_width // 2, 
                start_y + rect_height // 2, text=str(list_array[index]), 
                fill="white", font=('Bold', 15))

        steps = 20
        dy = (target_y - start_y) / steps 
        current_step = 0

        # Fixes header for the reverse list
        def fix_header_in_reverse():
            hmid_x = target_x + rect_width + spacing
            hmid_y = target_y + rect_height//2 

            if self.current_title:
                self.canvas.delete(self.current_title)
                self.current_title = None
            if self.current_line1:
                self.canvas.delete(self.current_line1)
                self.current_line1 = None
            if self.current_line2:
                self.canvas.delete(self.current_line2)
                self.current_line2 = None
            if self.current_box:
                self.canvas.delete(self.current_box)
                self.current_box = None

            self.current_box = self.canvas.create_rectangle(hmid_x-20, hmid_y-60,
                    hmid_x+10, hmid_y-35, fill="white", tags=f"header")

            self.current_line1 = self.canvas.create_line(hmid_x-5, hmid_y-45,
                    hmid_x-5,  hmid_y, fill="black", width=3) 

            self.current_line2 = self.canvas.create_line(hmid_x-5, hmid_y,
                    hmid_x-30,  hmid_y, fill="black", width=3, arrow="last", 
                    arrowshape=(10,15,5))

            self.current_title = self.canvas.create_text(hmid_x, hmid_y - 70,
                    text='head', fill="black", font=('Regular',15))

        # Animation function
        def animate_step():
            nonlocal current_step


            if current_step < steps:
                self.canvas.move(rect_id, 0, dy)
                self.canvas.move(text_id, 0, dy)

                current_step += 1

                self.canvas.after(100, animate_step)
            else:
                mid_x = target_x + rect_width//2 
                mid_y = target_y + rect_height//2
                self.rect_positions.append((mid_x, mid_y))
                if index > 0: 
                    from_x, from_y = self.rect_positions[index]
                    to_x, to_y = self.rect_positions[index-1]
                    self.canvas.create_line(from_x - rect_width//2, 
                            from_y, to_x + rect_width//2, to_y, width=3, 
                            fill="black", arrow = "last", arrowshape=(10,15,5))
                self.move_rectangles(list_array, index + 1) 
                self.canvas.create_line(180, 115, 150, 115, fill="black", 
                        width=3, arrow = "last", arrowshape=(10,15,5))
                fix_header_in_reverse()

        animate_step()

    def execute_command(self,var):
        if var == "Reverse":
            self.execute_reverse()
        else:
            self.execute_print()

    def execute_print(self):
        self.draw_linked_list()

    def execute_reverse(self):
        mylist = self.list_obj.to_list()
        print("list = ", mylist, "length = ", len(mylist))
        self.draw_linked_list()  # Gives a snapshot of the original list

        spacing = 45

        # Draw the NIL rectangle first
        self.canvas.create_rectangle(100, 100, 150, 130, fill="green")
        self.canvas.create_text(125, 115, text="NIL", fill="white", font=('Bold', 15))
        hmid_x = 180 
        hmid_y = 115
        self.current_box = self.canvas.create_rectangle(hmid_x-20, hmid_y-60,
                    hmid_x+10, hmid_y-35, fill="white", tags=f"header")

        self.current_line1 = self.canvas.create_line(hmid_x-5, hmid_y-45,
                    hmid_x-5,  hmid_y, fill="black", width=3) 

        self.current_line2 = self.canvas.create_line(hmid_x-5, hmid_y,
                    hmid_x-30,  hmid_y, fill="black", width=3, arrow="last", 
                    arrowshape=(10,15,5))

        self.current_title = self.canvas.create_text(hmid_x, hmid_y - 70,
                    text='head', fill="black", font=('Regular',15))

        self.rect_positions = []
        arr = array('i', mylist)
        if arr:
            # Start animated drawing of rectangles one by one
            self.move_rectangles(list_array=arr, index=0)
            # Once animation is done, schedule the next step (if needed)
            # For true recursion, handle logic after animation ends
        else:
            return

 
    def link_modify_delete(self):

        user_input = self.data_entry1.get()  
        print("Entered :", user_input)

        self.draw_linked_list()
        if not user_input.isnumeric(): 
            mb.showerror(title="Invalid input", message="Enter a number")
            self.data_entry1.delete(0, tk.END)
            return

        val = int(user_input)

        if val == -1:
            self.draw_linked_list()
            self.data_entry1.delete(0, tk.END)
            mb.showerror(title="Delete failed", message="Enter an item in list")
            return
        else:
            all_items = self.canvas.find_all()
            for item in all_items:
                if self.canvas.type(item) == "text":
                    if self.canvas.itemcget(item, "text") == user_input:
                        text_id = item

            rect_id = self.find_rectangle_by_text(user_input)

            index = self.list_obj.search(val)
            if index == -1:
                self.data_entry1.delete(0, tk.END)
                mb.showerror(title="Invalid input", message="Enter an item in list")
            
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
                        self.canvas.move(rect_id, 0, -5) # Move block
                        self.canvas.move(text_id, 0, -5)  # Move text 
                        self.parent.after(50, move_up) # Move effect on canvas 
                    else:
                        self.canvas.delete(rect_id)  # Remove rectangle
                        self.canvas.delete(text_id)   # Remove text
                        print(f"Deleted: {val}") # Print on console
                        self.draw_linked_list() # Draw queue after deletion

                move_up()
                self.data_entry1.delete(0, tk.END)
            else:
                mb.showerror(title = "wrong rect_id", message = "Delete failed")
                print("rect_id = ", rect_id, "text_id = ", text_id)

    def link_modify_insert(self):

        user_input1 = self.data_entry1.get()  
        user_input2 = self.data_entry2.get()  
        self.draw_linked_list()

        if user_input1.isnumeric() and user_input2.isnumeric(): 
            value = int(user_input1)
            pos = int(user_input2)

            success = self.list_obj.insertAt(value, pos)
            if success == -1:
                self.data_entry1.delete(0, tk.END)
                self.data_entry2.delete(0, tk.END)
                mb.showerror(title="Position invalid", message="Enter valid position")
                return
            if success == -2:
                self.data_entry1.delete(0, tk.END)
                self.data_entry2.delete(0, tk.END)
                mb.showerror(title="Position invalid", message="List empty: prepend/append allowed")
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
                move_down()
                self.data_entry1.delete(0, tk.END)
                self.data_entry2.delete(0, tk.END)

        else:
            mb.showerror(title="Linked list full", message="Insert failed")
            return



    def open_pdf(self, fx):
        self.clear_main_content_area() # Hide other content first

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



# Define sidebar menu
class SidebarMenu:
    def __init__(self, parent, widgets):
        self.parent = parent
        self.widgets = widgets
        self.create_menu()

    def create_menu(self):
        win_height = self.parent.winfo_height()
        self.widgets.toggle_menu_frame = tk.Frame(self.parent, 
                bg=self.widgets.bg_color)
        self.widgets.toggle_menu_frame.place(relx=0.7, y=50, height=win_height,
                relwidth=0.3)

        # First dropdown menu
        var = tk.StringVar()
        optionMenu = ttk.OptionMenu(self.widgets.toggle_menu_frame, var, 
                "Operations")
        optionMenu.pack(pady=20)

        menu = optionMenu['menu']
        subList1 = tk.Menu(menu, tearoff=False)
        subList2 = tk.Menu(menu, tearoff=False)

        menu.add_cascade(label="Modifiers", menu=subList1)
        menu.add_cascade(label="Accessors", menu=subList2)

        subList1.add_command(label="Append", 
                command=lambda: self.widgets.setup_animation_ui("Append"))
        subList1.add_command(label="Prepend", 
                command=lambda: self.widgets.setup_animation_ui("Prepend"))
        subList1.add_command(label="Delete", 
                command=lambda: self.widgets.setup_animation_ui("Delete"))
        subList1.add_command(label="Insert", 
                command=lambda: self.widgets.setup_animation_ui("Insert"))
        subList2.add_command(label="Find", 
                command=lambda: self.widgets.setup_animation_ui("Find"))
        subList2.add_command(label="Reverse", 
                command=lambda: self.widgets.setup_animation_ui("Reverse"))
        subList2.add_command(label="Print List", 
                command=lambda: self.widgets.setup_animation_ui("Print List"))

        # Second dropdown menu describing algorithms
        var1 = tk.StringVar()
        optionMenu1 = ttk.OptionMenu(self.widgets.toggle_menu_frame, var1, 
                "Decriptions")
        optionMenu1.pack(pady=20)

        menu1 = optionMenu1['menu']
        subList3 = tk.Menu(menu1, tearoff=False)
        #subList4 = tk.Menu(menu1, tearoff=False)

        menu1.add_cascade(label="Animation", menu=subList3)
        #menu1.add_cascade(label="Description", menu=subList3)

        subList3.add_command(label="Home", 
                command=lambda: self.widgets.execute_home())
        subList3.add_command(label="Linked list", 
                command=lambda: self.widgets.open_pdf("Stacks"))


if __name__ == "__main__":
    App()


