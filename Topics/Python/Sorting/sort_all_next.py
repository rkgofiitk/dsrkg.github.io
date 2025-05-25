import tkinter as tk
import random
from tkinter import ttk
from tkinter import scrolledtext
import os
import fitz  # PyMuPDF
from PIL import Image, ImageTk

# PyPDF2 is not primarily used for image rendering from PDFs

''' Animation program for sorting algorithms consists of six algorithms: 

    Insertion sort and Bubble sort each has running time of O(n^2) 
    Best case and average case running time of bucket sort is with k 
    buckets is n+k. 

    Merge sort is of order n log n 
    Quick sort is of order n^2 in worst case but averge n log n
    The reader may extend to include selection sort '''

# Create the main window
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Insertion Sort Animation")
        self.geometry("750x750") # Display window

        self.delay = 10 # Default value
        self.widgets = Widgets(self) # Instance of widget class

        self.mainloop() 

''' Define widget class (buttons, entries and labels) and display area
    Display has two frames: header frame and main frame
    The header frame includes an icon for expanding toggle menu frame
    When expanded menu frame displays dropdown menus '''

class Widgets:
    def __init__(self, parent):  # Constructor function
        self.parent = parent
        self.bg_color = '#383839'
        self.create_widgets()
        self.toggle_menu_frame = None
        self.execute_home() # Shows animation details


    # Create widgets: frames, buttons, labels and canvas
    def create_widgets(self):

        self.parent.title("Sorting Animations & PDF Viewer") 

        self.bg_color = '#383839' # ensure self.bg_color is initialized

        # head_frame and other initial widget setups from previous code)
        self.head_frame = tk.Frame(self.parent, bg=self.bg_color, 
                highlightbackground='white', highlightthickness=1)

        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.configure(height=50)

        # Defines header title bar
        self.title_lb = tk.Label(self.head_frame, text='Data structure:', 
                bg=self.bg_color, fg='white', font=('Bold', 20))
        self.title_lb.pack(side=tk.LEFT)

        self.subtitle_lb = tk.Label(self.head_frame, text='Sorting Animation', 
                bg=self.bg_color, fg='white', font=('Regular', 15))
        self.subtitle_lb.place(relx=0.35, rely=0.2)

        # Input fields (delay and number of elements) 
        # Labels for input fields to let user know what to input
        self.data_entry = ttk.Entry(self.parent, font=("Arial", 15))
        self.delay_entry = ttk.Entry(self.parent, font=("Arial", 15))
        self.txt_label = tk.Label(self.parent, text="Number of bars", 
                font=('Regular', 14))
        self.delay_label = tk.Label(self.parent, text="Animation delay", 
                font=('Regular', 14))

        # Main action button, its text and command change based on context
        self.btn = tk.Button(self.parent, text="", bg=self.bg_color, fg='white',
                pady=5, font=('Arial', 15), activebackground=self.bg_color, 
                activeforeground='white')

        # Toggle button for expanding sidebar menu
        self.toggle_btn = tk.Button(self.head_frame, text='≡', 
                bg=self.bg_color, fg='white', font=('Bold', 20), 
                bd=0, activebackground=self.bg_color, activeforeground='white',
                command=self.toggle_menu)
        self.toggle_btn.pack(side=tk.RIGHT)


        # Frame to hold the canvas and its scrollbars Will be packed/unpacked 
        # by functions like open_pdf, initialize_bars
        self.canvas_display_frame = tk.Frame(self.parent)

        self.canvas = tk.Canvas(self.canvas_display_frame, bg="white")
        self.v_scrollbar = ttk.Scrollbar(self.canvas_display_frame,
                orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self.canvas_display_frame, 
                orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, 
                xscrollcommand=self.h_scrollbar.set)

        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # For displaying messages on canvas
        self.canvas_label = tk.Label(self.canvas, text="", font=('Bold', 15), 
                bg="white", fg="blue") 

        # Text area for displaying descriptions
        self.text_widget = scrolledtext.ScrolledText(self.parent, wrap=tk.WORD,
                width=75, height=25)

        # Define animation buttons
        self.start_btn = tk.Button(self.parent, text="Start", bg="#383839", 
                fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15))

        self.reset_btn = tk.Button(self.parent, text="Restart", bg="#383839", 
                fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15))

        self.close_btn = tk.Button(self.parent, text="Close", bg="#383839", 
                fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15),
                command=lambda: self.close_current_view)


    # Clear contents before displaying new fields, text, buttons, etc.
    def clear_main_content_area(self):
        '''Hides all main content widgets, input fields, and specific 
        labels/buttons.'''

        if self.canvas_display_frame.winfo_ismapped():
            self.canvas_display_frame.pack_forget()

        if self.text_widget.winfo_ismapped():
            self.text_widget.pack_forget()
        
        self.canvas_label.place_forget()
        self.data_entry.place_forget()
        self.delay_entry.place_forget()
        self.txt_label.place_forget()
        self.delay_label.place_forget()

        if self.btn.winfo_ismapped(): # Main action button 
            self.btn.place_forget()
        if self.start_btn.winfo_ismapped():
            self.start_btn.place_forget()
        if self.reset_btn.winfo_ismapped():
            self.reset_btn.place_forget()
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()

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
        
        # Reset canvas scrollregion to avoid affecting next view
        # Use small, fixed values as winfo_width/height might be 
        # 1 if frame just got hidden
        self.canvas.config(scrollregion=(0,0,1,1))
        
    def execute_btn(self, var): # var is the method name or PDF name
        self.clear_main_content_area() # Start by clearing everything

        methods = ["Insertion sort", "Bubble sort", "Merge sort", "Quick sort",
                   "Bucket sort", "Heap sort"]

        if var in methods: # Setup for sorting animation input

            # Display input fields
            self.data_entry.place(relx=0.5, y=100, anchor=tk.CENTER)
            self.delay_entry.place(relx=0.5, y=130, anchor=tk.CENTER)

            self.txt_label.place(relx=0.25, y=100, anchor=tk.E)
            self.delay_label.place(relx=0.25, y=130, anchor=tk.E)

            # Configure and place action button to proceed to animation setup
            self.btn.configure(text=f"Prepare {var}", 
                    command=lambda v=var: self.executePlacement(v))
            self.btn.place(relx=0.5, y=170, anchor=tk.CENTER)

        else: 
            # Assumed to be a PDF key
            self.open_pdf(var)

    # Display a text file
    def display_file(self): 
        self.clear_main_content_area()
        filename = "explanation.txt"
        # Ensuring it also places self.close_btn
        try:
            if not os.path.exists(filename):
                self.text_widget.insert(tk.END, 
                        f"Error: File '{filename}' not found.")
            else:
                with open(filename, 'r') as file:
                    contents = file.read()
                    self.text_widget.delete(1.0, tk.END)
                    self.text_widget.insert(tk.END, contents)
            
            self.text_widget.pack(padx=15, pady=(15, 70), fill="both", 
                    expand=True)

            # Place the close button
            self.close_btn.place(relx=0.5, rely=0.97, anchor=tk.S) 

        except Exception as e:
            self.text_widget.pack(padx=15, pady=(15,70), fill="both", 
                    expand=True) # Pack widget to show error
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, f"Error displaying file: {e}")
            self.close_btn.place(relx=0.5, rely=0.95, anchor=tk.S)



    def setup_animation_ui_and_bars(self, sort_method_name):
        # self.clear_main_content_area() 
        # Called by executePlacement or executeReset before this

        self.canvas_display_frame.pack(padx=10, pady=(10, 70), fill=tk.BOTH, 
                expand=True) # pady for buttons
        self.parent.update_idletasks() 
        self.canvas.delete("all") # Clear bars 

        items_str = self.current_num_bars_str # Assumes current_num_bars_str is set before calling
        delay_str = self.current_delay_str   # Assumes current_delay_str is set
        
        num_bars = int(items_str) if items_str.isdigit() and int(items_str) > 0 else 20
        self.delay = int(delay_str) if delay_str.isdigit() and int(delay_str) >= 0 else 100

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1: canvas_width = 600
        if canvas_height <= 1: canvas_height = 400

        self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))
        self.bars = [] 
        self.bar_width = canvas_width / num_bars
        self.data = [random.randint(10, max(20, int(canvas_height * 0.9))) for _ in range(num_bars)]

        for i, value in enumerate(self.data):
            x0 = i * self.bar_width
            y0 = canvas_height - value
            x1 = (i + 1) * self.bar_width - 2 
            y1 = canvas_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue", outline="black")

        # Place Start and Reset buttons; NO Close button here
        self.start_btn.place(relx=0.40, rely=0.97, anchor=tk.S) 
        self.reset_btn.configure(command=lambda: self.executeReset(sort_method_name))
        self.reset_btn.place(relx=0.60, rely=0.97, anchor=tk.S)


    def executeReset(self, var): # var is the sort method name
        self.clear_main_content_area() # HIde canvas_label and other elements
        self.execute_btn(var) # Drawinput screen for 'var', which includes a close_btn


    def add_label(self, text): # This is for the "Sort Complete" label
        """Configures and places the canvas_label."""
        # Ensure canvas_label is visible if canvas_display_frame is visible
        if self.canvas_display_frame.winfo_ismapped():
            self.canvas_label.config(text=text)
            self.canvas_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER) # Adjusted placement
        else:
            # Fallback if somehow called when canvas isn't primary 
            # view (should not happen)
            print(f"Debug: add_label called with text '{text}' but canvas_display_frame is not visible.")

    def close_file(self):
        self.canvas.delete("all")
        self.canvas.pack_forget()
        # If text_widget was used and is visible, clear and hide it
        if self.text_widget.winfo_ismapped():
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.pack_forget()
        
        if self.btn.winfo_ismapped(): # If the main action button is visible
            self.btn.place_forget()
            
        self.close_btn.place_forget()

        # Clear the reference to the PDF image if it exists
        if hasattr(self, 'pdf_image_tk'):
            del self.pdf_image_tk    # Function displays description of animation 
    def display_file(self):

        filename = "explanation.txt" # See animation explanation  
    
        try:
            # Clear existing text and place new text inside text widget
            with open(filename, 'r') as file:
                contents = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, contents)
                self.text_widget.pack(padx=15, pady=30)
                self.close_btn.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
        except Exception as e:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, f"Error: {e}")

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

    # Bubble Sort Animation
    def bubble_sort_step(self, i=0, j=0):
      
        if i < len(self.data):
            if j < len(self.data) - 1 - i:
                if self.data[j] > self.data[j + 1]:
                    # Swap the numbers
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]

                    # Update the bars visually
                    self.update_bars() 

                # Schedule the next step after 100ms
                self.canvas.after(self.delay, self.bubble_sort_step, i, j + 1) 

            else: # Move to the next iteration after 100ms
                self.canvas.after(self.delay, self.bubble_sort_step, i + 1, 0)  
        else: 

            # Label for sorting complete 
            self.add_label("Bubble sort complete")
            return

    # Insertion Sort Animation
    def insertion_sort_step(self):


        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i - 1
            while j >= 0 and key < self.data[j]:
                self.data[j + 1] = self.data[j]
                self.canvas.after(self.delay) 
                self.update_bars()
                j -= 1
            self.data[j + 1] = key
            self.canvas.after(self.delay)
            self.update_bars()

        self.add_label("Insertion sort complete")
        return
        

    # Bucket sort requires a helper function to sort elements in a bucket
    def bucket_insertion_sort(self):

        for i in range(1, len(self.data)):

            temp = self.data[i]
            j = i - 1
            while j >= 0 and temp < self.data[j]:
                self.data[j + 1] = self.data[j]
                j -= 1

            self.data[j + 1] = temp

            self.update_bars()
            self.canvas.after(self.delay)

        return self.data 

    # Distributes input into 5 (fiexed) different buckets 
    def bucket_sort_step(self):


        result = [] 
        no_of_buckets = 5 
        buckets = [[] for i in range(no_of_buckets)]
        max_elem, min_elem = max(self.data), min(self.data)

        # Maximum size of a bucket 
        bucket_size = (max_elem - min_elem) / no_of_buckets


        # Uiformly distribute elements into buckets
        for element in self.data:

            # Calculate the bucket index for each element 
            # Distribution formula uniformly distributes the elements
            index = int((element - min_elem) / bucket_size)
            if element == max_elem:
                index -= 1
            else:
                index = 0

            # Place element in bucket according to index
            buckets[index].append(element)


        # Sort the elements in each buckets then concatenate to the result
        for bucket in buckets:
            result.extend(self.bucket_insertion_sort())


        self.data = result

        self.add_label("Bucket sort is complete")

        return self.data

    # Main Quick sort function is partition
    def partition(self, low, high):
        i = ( low - 1 ) # First element is partion pivot
        x = self.data[high]
 
        for j in range(low , high):
            if   self.data[j] <= x:
 
                i = i+1
                self.data[i],self.data[j] = self.data[j],self.data[i]

        self.data[i+1],self.data[high] = self.data[high],self.data[i+1]
        self.update_bars()
        self.canvas.after(self.delay)
        return (i+1)
 
    # high  --> Ending index
    def quick_sort_step(self,low,high):
 
        #  auxiliary stack
        size = high - low + 1
        stack = [0] * (size)
 
        top = -1
 
        top = top + 1
        stack[top] = low
        top = top + 1
        stack[top] = high
 
        # Keep popping from stack while is not empty
        while top >= 0:
 
            # Pop high and low
            high = stack[top]
            top = top - 1
            low = stack[top]
            top = top - 1
 
            # sorted array
            p = self.partition( low, high )

            # push left side to stack
            if p-1 > low:
                top = top + 1
                stack[top] = low
                top = top + 1
                stack[top] = p - 1

            #  push right side to stack
            if p+1 < high:
                top = top + 1
                stack[top] = p + 1
                top = top + 1
                stack[top] = high
 
        self.add_label("Quick sort is complete")
        return 


    # Heapify function for creating max heap
    def heapify(self, heapSize, k):
        done = False

        while not done:
            largest = k    # root
            l = 2 * k + 1  # left
            r = 2 * k + 2  # right

            if l < heapSize and self.data[l] > self.data[k]: 
                largest = l
            else:
                largest = k
            if r < heapSize and self.data[r] > self.data[largest]: 
                largest = r

            if largest != k:
                self.data[k], self.data[largest] = self.data[largest], self.data[k]
                k = largest
            else:
                done = True    

            self.update_bars()
            self.canvas.after(self.delay)

    # Build max heap function
    def buildHeap(self):
        o = int((len(self.data) - 2) / 2)

        for k in range(o, -1, -1):
            self.heapify(len(self.data), k)

        return self.data  

    # Use max heap sort
    def heap_sort_step(self):
        self.data = self.buildHeap()
        heapSize = len(self.data)
        for i in range(len(self.data) - 1, 0, -1):
            self.data[0], self.data[heapSize - 1] = self.data[heapSize - 1], self.data[0]
            heapSize -= 1
            self.heapify(heapSize, 0)

        self.add_label("Heap sort is complete")
        return self.data


    # Merge function for two sorted list 
    def merge(self, temp, From, mid, to):
 
        # Define merge interval 
        a = From 
        b = From 
        c = mid + 1  
 
        while b <= mid and c <= to:
            if self.data[b] < self.data[c]:
                temp[a] = self.data[b] 
                b = b + 1
            else:
                temp[a] = self.data[c]
                c = c + 1
            a = a + 1
 
        # Remaining elements
        while b < len(self.data) and b <= mid:
            temp[a] = self.data[b]
            a = a + 1
            b = b + 1
 
        # Copy back the merged data
        for b in range(From, to + 1):
            self.data[b] = temp[b]
 
    # Iterative merge sort that makes viewing logical
    def merge_sort_step(self):
 
        low = 0
        high = len(self.data) - 1
 
        # Sort list
        temp = self.data.copy()
 
        d = 1
        while d <= high - low:
 
            for b in range(low, high, 2*d):
                From = b
                mid = b + d - 1
                to = min(b + 2*d - 1, high)
                self.merge(temp, From, mid, to)
                self.update_bars()
                self.canvas.after(self.delay)
                
            d = 2*d
 
        self.add_label("Merge sort complete")
        return
        
    def show_btn(self, xcord, ycord):
        if xcord < 1 and ycord < 1:
            self.btn.place(relx=xcord,rely=ycord, anchor=tk.CENTER)
        else:
            self.btn.place(x=xcord,y=ycord, anchor=tk.CENTER)

    def hide_btn(self):
        self.btn.place_forget()
    
# In class Widgets:
    def execute_btn(self, var): # var is the method name or PDF name
        self.clear_main_content_area() # Start by clearing everything

        methods = ["Insertion sort", "Bubble sort", "Merge sort", "Quick sort",
                   "Bucket sort", "Heap sort"]

        if var in methods: # Setup for sorting animation
            # Display input fields and the main action button (self.btn)
            self.data_entry.place(relx=0.5, y=100, anchor=tk.CENTER) # Adjusted y
            self.txt_label.place(relx=0.25, y=100, anchor=tk.E)    # Adjusted x
            self.delay_entry.place(relx=0.5, y=130, anchor=tk.CENTER) # Adjusted y
            self.delay_label.place(relx=0.25, y=130, anchor=tk.E)   # Adjusted x

            self.btn.configure(text=f"Prepare {var}", command=lambda v=var: self.executePlacement(v))
            self.btn.place(relx=0.5, y=170, anchor=tk.CENTER) # Adjusted y
           # self.close_btn.place(relx=0.5, rely=0.95, anchor=tk.S) # General close button

        else: # This branch is for opening PDFs (About, Insrt, Bubsrt, etc.)
           # self.display_file()
            self.open_pdf(var) # open_pdf will call clear_main_content_area and pack canvas_display_frame


    # fix_input_labels is effectively merged into execute_btn's logic for animations.
    # hide_entry_fields and hide_labels are now part of clear_main_content_area or handled by it.


    def clear_content(self):
        self.text_widget.delete(1.0, tk.END) 

    # Hide labels
    def hide_labels(self):
        if self.txt_label.winfo_ismapped():
            self.txt_label.place_forget()
        if self.delay_label.winfo_ismapped():
            self.delay_label.place_forget()
        if self.start_btn.winfo_ismapped():
            self.start_btn.place_forget()
        if self.reset_btn.winfo_ismapped():
            self.reset_btn.place_forget()
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()

    # Hide the input fields and corresponding labels
    def hide_entry_fields(self, var):

        self.data_entry.place_forget()
        self.delay_entry.place_forget()


    # Show only required widgets (includes labels, button and entries)
    def fix_input_labels(self, var):
       
        sort_commands = ["Insertion sort", "Bubble sort", "Merge sort", "Quick sort", "Heap sort", "Bucket sort"]

        if var in sort_commands:

            if self.text_widget.winfo_ismapped():
                self.text_widget.pack_forget()

            if self.close_btn.winfo_ismapped():
                self.close_btn.place_forget()

            # Requre inputs: number of elements and animation delay
            self.data_entry.place(relx=0.5, y=150, anchor=tk.CENTER)
            self.delay_entry.place(relx=0.5, y=180, anchor=tk.CENTER)
            self.txt_label.place(relx=0.2, y=150, anchor=tk.CENTER)
            self.delay_label.place(relx=0.2, y=180, anchor=tk.CENTER)

            # Place button for starting sorting animation 
            self.btn.configure(text=var)
            self.btn.place(relx=0.5, y=250, anchor=tk.CENTER)

        else: 
            # Only place the close button for closing description file
            self.close_btn.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    # Hide canvas and its label
    def hide_canvas_and_label(self):
        if self.canvas_label.winfo_ismapped():
            self.canvas_label.place_forget()
        if self.canvas.winfo_ismapped():
            self.canvas.place_forget()

    # Hide start and restart button
    def hide_start_restart_btn(self):
        if self.start_btn.winfo_ismapped():
            self.start_btn.place_forget()
        if self.reset_btn.winfo_ismapped():
            self.reset_btn.place_forget()

    # Execute reset show input labels and entry fields and sort button 
# In class Widgets:
    def executeReset(self, var): # var is the sort method name
        self.clear_main_content_area()
        # Go back to the state where user can input N and delay for this 'var'
        self.execute_btn(var) # This will call clear_main_content_area and then set up inputs

    # Places start and reset button for animation
    def animation_btn_reconfiguration(self, var):
        self.btn.config(text=var)
        self.initialize_bars()
        self.start_btn.place(relx=0.35,rely=0.85)
        self.reset_btn.config(command=lambda:self.executeReset(var))
        self.reset_btn.place(relx=0.5,rely=0.85)

    # Creates two input fields and button to execute preferred sorting 
    def executePlacement(self, var): 
        # Store input values before hiding fields
        self.current_num_bars_str = self.data_entry.get()
        self.current_delay_str = self.delay_entry.get()

        # Clear input fields and the 'Prepare' button
        self.data_entry.place_forget()
        self.delay_entry.place_forget()
        self.txt_label.place_forget()
        self.delay_label.place_forget()
        if self.btn.winfo_ismapped():
            self.btn.place_forget()
        
        # Setup the animation view
        self.setup_animation_ui_and_bars(var)

        # Configure the Start button for the specific sort
        if var == "Insertion sort":
            self.start_btn.config(command=self.insertion_sort_step)
        elif var == "Bubble sort":
            self.start_btn.config(command=self.bubble_sort_step)
        elif var == "Merge sort":
            self.start_btn.config(command=self.merge_sort_step)
        elif var == "Quick sort":
            self.start_btn.config(command=lambda: self.quick_sort_step(0, len(self.data)-1))
        elif var == "Heap sort":
            self.start_btn.config(command=self.heap_sort_step)
        elif var == "Bucket sort":
            self.start_btn.config(command=self.bucket_sort_step) 


    # Initialize the data set and draw bars for data elements
    def setup_animation_ui_and_bars(self, sort_method_name):

        # Clear again, esp. if called from reset
        self.clear_main_content_area()

        # Make canvas_display_frame visible for animation
        self.canvas_display_frame.pack(padx=10, pady=(10, 75), 
                fill=tk.BOTH, expand=True) 

        # Ensure frame and canvas have dimensions
        self.parent.update_idletasks() 

        self.canvas.delete("all")

        items_str = self.current_num_bars_str
        delay_str = self.current_delay_str
        
        num_bars = int(items_str) if items_str.isdigit() and int(items_str) > 0 else 20
        self.delay = int(delay_str) if delay_str.isdigit() and int(delay_str) >= 0 else 100

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1: canvas_width = 600
        if canvas_height <= 1: canvas_height = 400

        # Set scrollregion for animation (typically non-scrolling or matches canvas size)
        self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))

        self.bars = [] # List to store bar rectangle objects if needed for direct manipulation
        self.bar_width = canvas_width / num_bars
        self.data = [random.randint(10, max(20, int(canvas_height * 0.9))) for _ in range(num_bars)]


        for i, value in enumerate(self.data):
            x0 = i * self.bar_width
            y0 = canvas_height - value
            x1 = (i + 1) * self.bar_width - 2 # -2 for a small gap
            y1 = canvas_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue", outline="black")

        # Place Start, Reset, and Close buttons
        self.start_btn.place(relx=0.4, rely=0.95, anchor=tk.S)
        self.reset_btn.configure(command=lambda: self.executeReset(sort_method_name))
        self.reset_btn.place(relx=0.55, rely=0.95, anchor=tk.S)

# In class Widgets:
    def initialize_bars(self):
        self.clear_main_content_area()
        # Make canvas_display_frame visible for animation
        # For animations expecting a fixed size canvas as per original self.canvas.place(x=25,y=50)
        # It's better to give self.canvas_display_frame a fixed size and place it.
        # Or, if animations can use a resizable canvas:
        self.canvas_display_frame.pack(padx=10, pady=(10,80), fill=tk.BOTH, expand=True) # For resizable animation canvas
        # If fixed size like original:
        # self.canvas_display_frame.place(x=25, y=50, width=600, height=400) # Example

        self.canvas.delete("all")

        # Get number of bars
        items = self.data_entry.get()
        sleep_time = self.delay_entry.get()
        # ... (your existing logic for delay and num_bars) ...
        num_bars = int(items) if items.isdigit() else 20 # Default if invalid
        self.delay = int(sleep_time) if sleep_time.isdigit() and int(sleep_time) > 0 else 10


        self.bars = []
        self.bar_lbs = []
        
        # Important: configure canvas for animation (non-scrolling or specific scrollregion)
        # Assuming animation draws within the visible area of the canvas.
        # If canvas_display_frame is packed to fill, then canvas width/height are dynamic.
        self.parent.update_idletasks() # Ensure dimensions are updated
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        self.bar_width = canvas_width / num_bars # Use actual canvas width
        self.data = [random.randint(10, canvas_height - 20) for _ in range(num_bars)] # Scale to canvas height

        # For animation, usually, you don't want the huge scrollregion from a PDF
        self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))


        # Draw the bars (similar to your existing logic, but adapt to canvas_width/height)
        for i, value in enumerate(self.data):
            x0 = i * self.bar_width
            y0 = canvas_height - value # Base on canvas_height
            x1 = x0 + self.bar_width - 2
            y1 = canvas_height       # Base on canvas_height
            label_x = (x0 + x1) / 2
            label_y = y0 - 10

            bar = self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
            # length = self.canvas.create_text(label_x, label_y, text=str(value)) # Optional: display value
            self.bars.append(bar)
            # self.bar_lbs.append(length)

        # Place entry fields, labels, and animation control buttons as needed
        self.data_entry.place(relx=0.5, y=150, anchor=tk.CENTER) # Example placement
        self.txt_label.place(relx=0.2, y=150, anchor=tk.CENTER)
        self.delay_entry.place(relx=0.5, y=180, anchor=tk.CENTER)
        self.delay_label.place(relx=0.2, y=180, anchor=tk.CENTER)
        # Start/Reset buttons are placed by animation_btn_reconfiguration


    # Update the bars visually
# In class Widgets:
    def update_bars(self):
        self.canvas.delete("all") # Clears everything, including any 'canvas_label' text
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 : canvas_width = 600 # Fallback
        if canvas_height <= 1 : canvas_height = 400 # Fallback

        if not self.data or len(self.data) == 0: # Should not happen if initialized
            return
            

        for i, value in enumerate(self.data):
            x0 = i * self.bar_width
            y0 = canvas_height - value
            x1 = (i + 1) * self.bar_width - 2
            y1 = canvas_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue", outline="black")
        
        self.canvas.update_idletasks()

    # Function for placing completion label on the canvas 
    def add_label(self, text):
        self.canvas_label.config(text=text)
        self.canvas_label.place(relx=0.3, rely=0.1) 

    def display_page(self, page_num):
        if 0 <= page_num < len(self.pdf_doc):
            pix = self.pdf_doc[page_num].get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            self.img_tk = ImageTk.PhotoImage(img)
            self.label = tk.Label(self.inner_frame, image=self.img_tk)
            self.label.pack()

            # Update canvas scroll region
            self.inner_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))


    def prev_page(self):
        # Logic to navigate to the previous PDF page
        if self.current_page > 0:
            self.current_page -= 1
            self.clear_canvas()
            self.display_page(self.current_page)

    def next_page(self):
        # Logic to navigate to the next PDF page
        if self.current_page < len(self.pdf_doc) - 1:
            self.current_page += 1
            self.clear_canvas()
            self.display_page(self.current_page)

    def clear_canvas(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

    def close_pdf_viewer(self):
        # Logic to close the PDF viewer
        self.inner_frame.destroy()  # Closes the application (modify as needed)
        self.pdf_canvas.destroy()
        self.v_scroll.destroy()
        self.h_scroll.destroy()
        self.button_frame.destroy()
        self.executePlacement('16')
        

        # also destroy scroll bars
        # also remove buttons 

# Inside the Widgets class

    def open_pdf(self, fx):
        self.clear_main_content_area() # Hide other content first

        # Make the canvas frame visible for PDF display
        self.canvas_display_frame.pack(padx=10, pady=(10,75), fill=tk.BOTH, expand=True) # pady bottom for close_btn
        self.canvas.delete("all") # Clear previous canvas content

        file_name = ""
        if fx == "Qsrt": file_name = "quick_sort_algo.pdf"
        elif fx == "Hpsrt": file_name = "heap_sort_algo.pdf"
        elif fx == "Mrgsrt": file_name = "merge_sort_algo.pdf"
        elif fx == "Bubsrt": file_name = "bubble_sort_algo.pdf" # Ensure this file exists
        elif fx == "Insrt": file_name = "insertion_sort_algo.pdf"
        elif fx == "Bktsrt": file_name = "bucket_sort_algo.pdf"
        elif fx == "About": file_name = "explanation.pdf" # e.g., "about_app.pdf"
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

            if not page_images_pil: return

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

# In class Widgets:
    def close_current_view(self):
        """Hides the currently active main content view and its specific 
           resources."""

        # Hide canvas_display_frame and text_widget
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
        if self.btn.winfo_ismapped():
            self.btn.place_forget()
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()
        
        # Optionally, show a default view or home screen elements
        #self.execute_home() # I have a problem here to be fixed 
        self.btn.configure(text="About",command=lambda: self.execute_home())
        self.btn.place(relx=0.5,y=170)

    # In execute_home, if it opens a PDF: This should be modifed now
    def execute_home(self):
        # Original: self.close_btn.configure(command=self.close_file)
        self.close_btn.configure(command=self.close_current_view)
        self.open_pdf("About") # It will use the scrollable PDF viewer

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
        subList2 = tk.Menu(menu, tearoff=False)

        # Two sublists for first menu 
        menu.add_cascade(label="Square n sort", menu=subList1)
        menu.add_cascade(label="Log n sort", menu=subList2)

        subList1.add_command(label="Insertion", 
                command=lambda: self.widgets.execute_btn("Insertion sort"))
        subList1.add_command(label="Bubble sort", 
                command=lambda: self.widgets.execute_btn("Bubble sort"))
        subList1.add_command(label="Bucket sort", 
                command=lambda: self.widgets.execute_btn("Bucket sort"))

        subList2.add_command(label="Merge sort", 
                command=lambda: self.widgets.execute_btn("Merge sort"))
        subList2.add_command(label="Quick sort", 
                command=lambda: self.widgets.execute_btn("Quick sort"))
        subList2.add_command(label="Heap sort", 
                command=lambda: self.widgets.execute_btn("Heap sort"))

        # Second dropdown menu describing algorithms
        var1 = tk.StringVar()
        optionMenu1 = ttk.OptionMenu(self.widgets.toggle_menu_frame, var1, 
                "Schemes")
        optionMenu1.pack(pady=20)

        menu1 = optionMenu1['menu']
        subList3 = tk.Menu(menu1, tearoff=False)
        subList4 = tk.Menu(menu1, tearoff=False)

        menu1.add_cascade(label="Animation", menu=subList3)
        menu1.add_cascade(label="Algorithms", menu=subList4)

        subList3.add_command(label="About", 
                command=lambda: self.widgets.execute_btn("About"))
        subList4.add_command(label="Insertion sort",
                command=lambda: self.widgets.execute_btn("Insrt"))
        subList4.add_command(label="Bubble sort",
                command=lambda: self.widgets.execute_btn("Bubsrt"))
        subList4.add_command(label="Bucket sort",
                command=lambda: self.widgets.execute_btn("Bktsrt"))
        subList4.add_command(label="Merge sort", 
                command=lambda: self.widgets.execute_btn("Mrgsrt"))
        subList4.add_command(label="Heap sort", 
                command=lambda: self.widgets.execute_btn("Hpsrt"))
        subList4.add_command(label="Quick sort", 
                command=lambda: self.widgets.execute_btn("Qsrt"))

if __name__ == "__main__":
    App()

