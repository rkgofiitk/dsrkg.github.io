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
        self.toggle_menu_frame = None

        self.root = parent 
        self.root.title("Binary Search Tree Visualizer")
        self.toggle_menu_frame = None

        self.create_widgets()

        # Keep canvas display frame open for BSTVisualizer
        self.canvas_display_frame.pack(padx=10, pady=(50,75), fill=tk.BOTH,
                expand=True)

        self.bst = BSTVisualizer(self.canvas) # Create an instance of BST visualizer

        # Default display for explanation of animation
        self.execute_home()

    def create_widgets(self):

        self.bg_color = '#383839'
        self.head_frame = tk.Frame(self.root, bg=self.bg_color, 
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


        # Toggle button for side menubar expansion and collapse 
        self.toggle_btn = tk.Button(self.head_frame, text='≡', bg=self.bg_color,
                fg='white', font=('Bold', 20), bd=0, 
                activebackground=self.bg_color, activeforeground='white', 
                command=self.toggle_menu)
        self.toggle_btn.pack(side=tk.RIGHT)


        # Define canvas frame and canvas
        self.canvas_display_frame = tk.Frame(self.root)
        self.canvas = tk.Canvas(self.canvas_display_frame, bg="white")

        # Create a frame to hold canvas and vertical scrollbar side by side
        canvas_scroll_frame = tk.Frame(self.canvas_display_frame)
        canvas_scroll_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas inside the scroll frame
        self.canvas = tk.Canvas(canvas_scroll_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create text label for display messages on Canvas 
        self.canvas_label = tk.Label(self.canvas, text="", font=('Bold', 15), 
                bg="white", fg="blue") 

        # Vertical scrollbar next to canvas
        self.v_scrollbar = ttk.Scrollbar(canvas_scroll_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Horizontal scrollbar below the canvas
        self.h_scrollbar = ttk.Scrollbar(self.canvas_display_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(fill=tk.X)

        # Connect scrollbars to canvas
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)


        # Text Widget (correct placement inside viewing window)
        self.text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.WORD,
                width=75, height=10)

        # Define input frame for accepting user input
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Fields for input entries
        self.entry = tk.Entry(self.input_frame, width=20)
        self.txt_label = tk.Label(self.input_frame, text="Enter value", font=('Regular', 15))

        self.close_btn = tk.Button(self.root, text="Close", bg="#383839", 
                fg="white", activebackground="#383839", 
                activeforeground="white", font=('Bold', 15), 
                command=lambda: self.close_current_view)


        self.insert_btn = tk.Button(self.input_frame, text="Insert", command=self.insert_value)

        self.delete_btn = tk.Button(self.input_frame, text="Delete", command=self.delete_value)

        self.search_btn = tk.Button(self.input_frame, text="Search", command=self.find_value)


    def toggle_menu(self):
        if self.toggle_menu_frame and self.toggle_menu_frame.winfo_ismapped():
            self.toggle_menu_frame.place_forget() 
            self.toggle_btn.config(text='≡') 
        else:
            if not self.toggle_menu_frame: 
                self.toggle_menu_frame = tk.Frame(self.root, bg=self.bg_color)
                SidebarMenu(self.root, self) 

            # Toggle sidebar menu
            self.toggle_menu_frame.place(relx=0.7, y=50,
                    height=self.root.winfo_height(),
                    relwidth=0.3) 
            # Update to close button icon 
            self.toggle_btn.config(text='X')  


    def execute_operation(self, opcode):
        self.close_current_view()
        self.hide_input_frame()

        self.txt_label.grid(row=0,column=0, padx=5, pady=5)
        self.entry.grid(row=0,column=1, padx=5, pady=5)

        if opcode == "Insert":
            self.show_input_frame("Insert")
        if opcode == "Delete":
            self.show_input_frame("Delete")
        if opcode == "Search":
            self.show_input_frame("Search")

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
        


    # Clear contents before displaying new fields, text, buttons, etc.
    def clear_main_content_area(self):
        '''Hides all main content widgets, input fields, and specific 
        labels/buttons.'''

        if self.text_widget.winfo_ismapped():
            self.text_widget.pack_forget()
        
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()

    def hide_input_frame(self):
        '''Hides input frame and buttons on input frame'''

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


    def show_input_frame(self,optype):

        if optype == "Insert":
            self.insert_btn.grid(row=0,column=2, padx=5, pady=5)
        if optype == "Delete":
            self.delete_btn.grid(row=0,column=2, padx=5, pady=5)
        if optype == "Search":
            self.search_btn.grid(row=0,column=2, padx=5, pady=5)

        self.input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)


    def insert_value(self):
        try:
            value = int(self.entry.get())
            self.bst.insert(value)
            self.entry.delete(0,tk.END)
        except ValueError:
            self.entry.delete(0,tk.END)
            pass

    def delete_value(self):
        try:
            value = int(self.entry.get())
            self.bst.delete(value)
            self.entry.delete(0,tk.END)
        except ValueError:
            self.entry.delete(0,tk.END)
            pass

    def add_label(self, text): # This is for search result label
        self.canvas_label.config(text=text)
        self.canvas_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER) # Adjusted placement

    def find_value(self):
        try:
            value = int(self.entry.get())
            print(self.bst.find(value))
            if self.bst.find(value) is True:
                self.add_label(var) 
            else:
                self.add_label(var) 

            self.entry.delete(0,tk.END)
        except ValueError:
            pass


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
        if self.close_btn.winfo_ismapped():
            self.close_btn.place_forget()

        self.bst.redraw()
        

    def open_pdf(self, fx):
        self.clear_main_content_area() # Hide other content first

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

        subList1.add_command(label="Insert", 
                command=lambda: self.widgets.execute_operation("Insert"))
        subList1.add_command(label="Delete", 
                command=lambda: self.widgets.execute_operation("Delete"))
        subList1.add_command(label="Search", 
                command=lambda: self.widgets.execute_operation("Search"))
        subList2.add_command(label="Preorder", 
                command=lambda: self.widgets.tree_traversal("Preorder"))
        subList2.add_command(label="Inorder", 
                command=lambda: self.widgets.tree_traversal("Inorder"))
        subList2.add_command(label="Postorder", 
                command=lambda: self.widgets.tree_traversal("Postorder"))
        subList2.add_command(label="Draw", 
                command=lambda: self.widgets.execute_redraw())

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
        subList3.add_command(label="BST", 
                command=lambda: self.BSTApp.open_pdf("Trees"))




if __name__ == "__main__":
    App()
