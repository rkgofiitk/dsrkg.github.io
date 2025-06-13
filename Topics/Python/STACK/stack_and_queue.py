import tkinter as tk
from stackOps import Stack  # Import your Stack class
from queueOps import QueueArray # Import your Queue class
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox as mb 
import os
import fitz 
from PIL import Image, ImageTk

# Create the main window
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Insertion Sort Animation")
        self.geometry("750x750") # Display window

        self.delay = 10 # Default value
        self.widgets = StackAnimation(self) # Instance of widget class


        self.mainloop() 


class StackAnimation:
    def __init__(self, parent):
        self.parent = parent 
        self.stack_obj = Stack()  # Initialize stack
        self.queue_obj = QueueArray()  # Initialize stack

        self.create_widgets()
        self.toggle_menu_frame = None
        
        self.execute_home()


    def create_widgets(self):
        self.bg_color = "#383839" # Define widget background color

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

        self.txt_label = tk.Label(self.input_frame, text="Enter", font=('Regular', 15))

        self.data_entry = tk.Entry(self.input_frame, width=20)

        # Stack and queue operation buttons: enguque, pop, push and dequeue
        self.push_btn = tk.Button(self.input_frame, text="Push", 
                font=('Regular', 15), bg=self.bg_color, fg="white", 
                activebackground=self.bg_color, activeforeground="white" )

        self.pop_btn = tk.Button(self.input_frame, text="Pop", 
                font=('Regular', 15), bg=self.bg_color, fg="white", 
                activebackground=self.bg_color, activeforeground="white" )

        self.enqueue_btn = tk.Button(self.input_frame, text="Enqueue", 
                font=('Regular', 15), bg=self.bg_color, fg="white", 
                activebackground=self.bg_color, activeforeground="white" )

        self.dequeue_btn = tk.Button(self.input_frame, text="Dequeue", 
                font=('Regular', 15), bg=self.bg_color, fg="white", 
                activebackground=self.bg_color, activeforeground="white" )

        # Close Button for closing pdf viewer 
        self.close_btn = tk.Button(self.parent, text="Close", bg="#383839", 
                fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15), 
                command=lambda: self.close_current_view)

        # Home button takes user to description of animation
        self.home_btn = tk.Button(self.parent, text="Home", bg="#383839", 
                fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15), 
                command=lambda: self.close_current_view)

        # User can invoke stack operation features with this button
        self.stk_btn = tk.Button(self.parent, text="Stack operations",
                bg="#383839", fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15), 
                command=lambda: self.setup_animation_ui("stack"))

        # User can invoke queue operation features with this button
        self.queue_btn = tk.Button(self.parent, text="Queue operations",
                bg="#383839", fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15), 
                command=lambda: self.setup_animation_ui("queue"))

        # Set window title
        self.parent.title("Stack Animation")

        self.item_size = 30 # Define a size for items 

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
        self.data_entry.place_forget()
        self.txt_label.place_forget()
  
        if self.pop_btn.winfo_ismapped(): # Main action button 
            self.pop_btn.place_forget()
        if self.push_btn.winfo_ismapped():
            self.push_btn.place_forget()
        if self.enqueue_btn.winfo_ismapped():
            self.enqueue_btn.place_forget()
        if self.dequeue_btn.winfo_ismapped():
            self.dequeue_btn.place_forget()
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


        if self.home_btn.winfo_ismapped():
            self.home_btn.pack_forget()
        self.txt_label.pack(side=tk.LEFT, padx=5)
        self.data_entry.pack(side=tk.LEFT, padx=5)

        # Define two sets of operations one for stack another fore queue
        if var == "stack": # Only map push and pop buttons
            self.push_btn.configure(command=lambda: self.animate_push())
            self.pop_btn.configure(command=lambda: self.animate_pop())
            self.push_btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.pop_btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.enqueue_btn.pack_forget() # Forget if mapped earlier
            self.dequeue_btn.pack_forget() # Forget if mapped earlier

        if var == "queue": # Only map enqueue and dequeue buttons
            self.enqueue_btn.configure(command=lambda: self.animate_enqueue())
            self.enqueue_btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.dequeue_btn.configure(command=lambda: self.animate_dequeue())
            self.dequeue_btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.push_btn.pack_forget() # Forget if mapped earlier
            self.pop_btn.pack_forget() # Forget if mapped earlier

        
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


    def draw_queue(self):

        self.canvas.delete("all")

        if not self.queue_obj.is_empty():
            qlist = self.queue_obj.to_list()

            item_width = 50
            spacing = 30
            x_start = 100
            y1 = 310
            y2 = 340

            for i, val in enumerate(qlist):
                x1 = x_start +  i * (self.item_size + spacing)
                x2 = x1 + item_width
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags=f"block_{i}")
                self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(val), font=('Bold', 15),  fill="white", tags=f"text_{i}")
        

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
            label_id3 = self.canvas.create_text(350, 100, text="Current status of Queue", font=("Arial", 15), fill="blue")
        else:
            label_id4 = self.canvas.create_text(350, 100, text="Queue is Empty", font=("Arial", 15), fill="blue")




    def animate_dequeue(self):

        # Dequeue return dequeued value if queue is not empty
        if not self.queue_obj.is_empty():

            # Front item is always mapped to first block on canvas 
            # So, block 0 is selected for animation 
            block_items = self.canvas.find_withtag(f"block_0")
            text_items = self.canvas.find_withtag(f"text_0")  
            if block_items: 
                block_id = block_items[0]
                text_id = text_items[0]
            else:
                print("Error") # Error if there no block 0
                return

            dequeued_val = self.queue_obj.dequeue()

            if block_id and text_id:
                self.canvas.itemconfig(block_id, fill="green")
                def move_up():
                    rect_coords = self.canvas.coords(block_id)
                    text_coords = self.canvas.coords(text_id)

                    if rect_coords and text_coords and rect_coords[1] > 100:
                        self.canvas.move(block_id, 0, -5) # Move block
                        self.canvas.move(text_id, 0, -5)  # Move text 
                        self.parent.after(50, move_up) # Move effect on canvas 
                    else:
                        self.canvas.delete(block_id)  # Remove rectangle
                        self.canvas.delete(text_id)   # Remove text
                        print(f"Dequeued: {dequeued_val}") # Print on console
                        self.draw_queue() # Draw queue after deletion

                move_up()
            else:
                mb.showerror(title = "Queue is empty", message = "Dequeue failed")
                print("Queue is empty!")


    def animate_enqueue(self):
        
        user_input = self.data_entry.get()  
        if user_input.isnumeric():  # Ensure input validity

            # Create a vertical solid line with an arrowhead at the top
            value = int(user_input)
            spacing = 30
            print("value to be inserted = ", value)

            success = self.queue_obj.enqueue(value)

            print(success)
            if success:
                y_start = 100
                y_end = y_start + 30
                print("length of queue = ", self.queue_obj.length())
                x_start = 100 + (self.queue_obj.length()-1) * (self.item_size + spacing) 
                x_end = x_start + 50
                rect_id = self.canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="green")
                text_id = self.canvas.create_text(x_start + 25, y_start+15, text=str(value), fill="white", font=('Bold', 15))
      
                def move_down():
                    """Moves the rectangle downward"""
                    current_coords = self.canvas.coords(rect_id)
                    if current_coords[1] < 310: 
                        self.canvas.move(rect_id, 0, 5)
                        self.canvas.move(text_id, 0, 5)
                        self.parent.after(50, move_down)
                    else:
                        self.draw_queue()
                move_down()
                self.data_entry.delete(0, tk.END)

            else:
                print("Queue is full")
                mb.showerror(title = "Queue us full", message = "Enqueue denied")
        else:
            self.data_entry.delete(0, tk.END)
            mb.showerror(title = "Invalid input", message = "Enter a number")

    def animate_pop(self):
        """Animates pop operation"""
        if not self.stack_obj.is_empty():
            top_index = self.stack_obj.size() - 1

            # Find the top of stack gets its ID
            block_id = self.canvas.find_withtag(f"block_{top_index}")
            text_id = self.canvas.find_withtag(f"text_{top_index}")  

            popped_value = self.stack_obj.pop()

            if block_id and text_id:
                def move_up():
                    self.canvas.itemconfig(block_id, fill="green")
                    rect_coords = self.canvas.coords(block_id)
                    text_coords = self.canvas.coords(text_id)

                    if rect_coords and text_coords and rect_coords[1] > 50:
                        self.canvas.move(block_id, 0, -5)
                        self.canvas.move(text_id, 0, -5)  # Move text along with rectangle
                        self.parent.after(50, move_up)
                    else:
                        self.canvas.delete(block_id)  # Remove rectangle
                        self.canvas.delete(text_id)   # Remove text
                        print(f"Popped: {popped_value}")
                        self.draw_stack()

                move_up()
        else:
            mb.showerror(title = "Stack is empty", message = "Pop failed")
            print("Stack is empty!")



    def draw_stack(self):
        """Redraws the stack visually"""
        self.canvas.delete("all")
        for i, val in enumerate(self.stack_obj.get_stack()):
            x1, y1 = 300, 450 - (i * self.item_size)
            x2, y2 = 400, 480 - (i * self.item_size)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags=f"block_{i}")
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(val), fill="white", font=('Regular',15), tags=f"text_{i}")
            self.canvas.create_line(x1, y2 + 2, x2, y2 + 2, fill="white", width=2)
        line_id1 = self.canvas.create_line((x1+x2)//2, y1, (x1+x2)//2, y1-40, fill="black", width=3, arrow="first")
        # Add a label at the tail of the line
        label_id1 = self.canvas.create_text((x1+x2)//2,y1-50, text="Top", font=("Arial", 12), fill="black")

        line_id2 = self.canvas.create_line(x1-8, 485, x2+8, 485, fill="black", width=3)
        line_id3 = self.canvas.create_line(x1-8, 485, x1-8, 180, fill="black", width=3)
        line_id4 = self.canvas.create_line(x2+8, 485, x2+8, 180, fill="black", width=3)
        line_id5 = self.canvas.create_line(x1-8, 180, x1-24, 180, fill="black", width=3)
        line_id6 = self.canvas.create_line(x2+8, 180, x2+24, 180, fill="black", width=3)
        label_id2 = self.canvas.create_text((x1+x2)//2,100, text="Current status of stack", font=("Arial", 15), fill="blue")


    def animate_push(self):
        """Animates push operation with user input"""

        user_input = self.data_entry.get()  #self.data_entry.get() #self.data_entry.get()
        if user_input.isnumeric():  # Ensure valid input
            value = int(user_input)

            if self.stack_obj.is_full():
                mb.showerror(title = "Stack is full", message = "Push failed")

            success = self.stack_obj.push(value)

            if success:
                y_start = 50
                y_end = 450 - (self.stack_obj.size() - 1) * self.item_size
                rect_id = self.canvas.create_rectangle(300, y_start, 400, y_start + 30, fill="green")
                text_id = self.canvas.create_text(350, y_start + 15, text=str(value), fill="white", font=('Bold', 15))

                def move_down():
                    current_coords = self.canvas.coords(rect_id)
                    if current_coords[1] < y_end:
                        self.canvas.move(rect_id, 0, 5)
                        self.canvas.move(text_id, 0, 5)
                        self.parent.after(50, move_down)
                    else:
                        self.draw_stack()

                move_down()
                self.data_entry.delete(0, tk.END)  # Clear input field after push
        else:
            print("Invalid input! Enter a number.")
            mb.showerror(title = "Invalid input", message = "Enter a number")


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
                "Modifier")
        optionMenu.pack(pady=20)

        menu = optionMenu['menu']
        subList1 = tk.Menu(menu, tearoff=False)
        #subList2 = tk.Menu(menu, tearoff=False)

        menu.add_cascade(label="Operations", menu=subList1)

        subList1.add_command(label="Stacks", 
                command=lambda: self.widgets.setup_animation_ui("stack"))
        subList1.add_command(label="Queue", 
                command=lambda: self.widgets.setup_animation_ui("queue"))

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
        subList3.add_command(label="Stack", 
                command=lambda: self.widgets.open_pdf("Stacks"))
        subList3.add_command(label="Queue", 
                command=lambda: self.widgets.open_pdf("Queues"))


if __name__ == "__main__":
    App()


