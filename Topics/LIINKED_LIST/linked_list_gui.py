import tkinter as tk
from tkinter import ttk
import os
import linkedListOps  # Include linked list module 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg="white") 
        self.geometry('600x700') # Define window size for display 
        self.title('Linked list operation')  # Window title

        L = linkedListOps.LinkedList()  # Create an empty linked list 
        self.widgets = Widgets(self, L) # Creates required widgets

        self.mainloop()

class Widgets:
    def __init__(self, parent, linked_list):
        self.parent = parent
        self.L = linked_list
        self.bg_color = '#383839'
        self.toggle_menu_frame = None
        self.create_widgets()

    # Create widgets: button and labels 
    def create_widgets(self):
        # For printing title
        self.lb = tk.Label(self.parent, text='', font=('bold', 16), bg="white",
                fg="black", anchor=tk.CENTER)
        self.lb.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # For printing contents
        self.llb = tk.Label(self.parent, text='', font=('bold', 12),
                bg="white", fg="black", anchor=tk.CENTER)
        self.llb.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Additional labels printing for reverse list
        self.lb1 = tk.Label(self.parent, text='', font=('bold', 16), bg="white",
                fg="black", anchor=tk.CENTER)
        self.lb1.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        self.llb1 = tk.Label(self.parent, text='', font=('bold', 12),
                bg="white", fg="black", anchor=tk.CENTER)
        self.llb1.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        
        # Define the button that is reconfigured according
        # to function to be executed
        self.btn = tk.Button(self.parent, text="Instructions", bg=self.bg_color,
                fg='white', pady=5, font=('Arial', 15),
                activebackground=self.bg_color, activeforeground='white',
                command=self.display_file)

        # Map the button
        self.btn.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        # Labels for data entry fields to let user know 
        # the nature of input required in the entry field 
        self.txt_label = tk.Label(self.parent, text="Enter value",
                bg='white', font=('Regular',14))
        self.txt_label1 = tk.Label(self.parent, text="Enter index", 
                bg='white', font=('Regular',14))

        self.data_entry = ttk.Entry(self.parent, font=("Arial", 15))

        # Needed only for insertAt operation 
        self.second_data_entry = ttk.Entry(self.parent, font=("Arial", 15))

        self.head_frame = tk.Frame(self.parent, bg=self.bg_color,
                highlightbackground='white', highlightthickness=1)
        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.configure(height=50)

        # Define toggle button for expanding side menubar
        self.toggle_btn = tk.Button(self.head_frame, text='≡', bg=self.bg_color,
                fg='white', font=('Bold', 20), bd=0,
                activebackground=self.bg_color, activeforeground='white',
                command=self.toggle_menu)
        self.toggle_btn.pack(side=tk.RIGHT)

        # Title bar label
        self.title_lb = tk.Label(self.head_frame, text='Data structure:',
                bg=self.bg_color, fg='white', font=('Bold', 20))
        self.title_lb.pack(side=tk.LEFT)

        # Subtitle bar label
        self.subtitle_lb = tk.Label(self.head_frame,
                text='Linked list operations', bg=self.bg_color, fg='white',
                font=('Regular', 15))
        self.subtitle_lb.place(relx=0.35, rely=0.2)

        # Text widget for displaying instructions
        self.text_widget = tk.Text(self.parent, wrap="word")


    def executeDefault(self):
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.pack_forget() 

        self.btn.configure(text="Instructions", command=self.display_file)
        self.btn.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

    def display_file(self):

        self.text_widget.pack(padx=10, pady=50)
        self.btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.btn.configure(text="Close", command=self.executeDefault)

        # Open the file readme file
        filename = "readme.txt"
    
        try:
            # Clear existing text content and
            # place file contents into text widget
            with open(filename, 'r') as file:
                contents = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, contents)
        except Exception as e:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, f"Error: {e}")

    # Function for toggling sidebar frame
    def toggle_menu(self):
        if self.toggle_menu_frame and self.toggle_menu_frame.winfo_ismapped():
            self.toggle_menu_frame.place_forget() # Hide the sidebar
            self.toggle_btn.config(text='≡')  # Reset button to default state
        else:
            if not self.toggle_menu_frame: # Create sidebar if it doesn't exist
                self.toggle_menu_frame = tk.Frame(self.parent, bg=self.bg_color)
                SidebarMenu(self.parent, self)  # Initialize the sidebar menu

            self.toggle_menu_frame.place(relx=0.7, y=50,
                    height=self.parent.winfo_height(),
                    relwidth=0.3) # Show the sidebar
            self.toggle_btn.config(text='X')  # Update button to "close" state

    def hide_labels(self):
        if self.lb.winfo_ismapped():
            self.lb.place_forget()
        if self.llb.winfo_ismapped():
            self.llb.place_forget()
        if self.lb1.winfo_ismapped():
            self.lb1.place_forget()
        if self.llb1.winfo_ismapped():
            self.llb1.place_forget()
        if self.txt_label.winfo_ismapped():
            self.txt_label.place_forget()
        if self.txt_label1.winfo_ismapped():
            self.txt_label1.place_forget()

    def hide_entry_fields(self,var):
        self.hide_labels() # Hide all labels from main window

        list1 = ["Last", "First", "Print", "Instructions", "Reverse"] 
        if var in list1:
            # Hide the input fields and corresponding labels
            if self.data_entry.winfo_ismapped():
                self.data_entry.place_forget() # Hide first data field 
            if self.second_data_entry.winfo_ismapped():
                self.second_data_entry.place_forget() # Hide second data field 

        # Hide second data entry field for insertAt
        list2 = ["Append", "Prepend", "Remove", "RemoveAt"]
        if var in list2: 
            if self.second_data_entry.winfo_ismapped():
                self.second_data_entry.place_forget() # Hide data entry 

    # Define input fields and corresponding labels for each function 
    def fix_input_labels(self, var):
        self.btn.configure(text=var)
        list1 = ["Successor", "Predecessor"] 
        list2 = ["Append", "Prepend", "Remove", "InsertAt", "Search"]
       
        if var in list1 or var in list2:
            self.data_entry.place(relx=0.5, y=150, anchor=tk.CENTER)
            self.txt_label.place(relx=0.2, y=150, anchor=tk.CENTER)

        if var == "InsertAt":
            self.second_data_entry.place(relx=0.5, y=200, anchor=tk.CENTER)
            self.txt_label1.place(relx=0.2, y=200, anchor=tk.CENTER)

        if var == "RemoveAt":
            self.second_data_entry.place(relx=0.5, y=150, anchor=tk.CENTER)
            self.txt_label1.place(relx=0.2, y=150, anchor=tk.CENTER)


    # Switch case for selection of command button 
    def execute_btn(self, var):

        # Reset to default button before reconfiguring 
        # the button to selected command in the menu 
        if self.btn.cget("text") == "Close":
            self.executeDefault()

        if var == "Append": # Append an element
            self.hide_entry_fields(var)
            self.fix_input_labels(var)
            self.btn.configure(text=var, command=self.executeAppend)

        elif var == "Prepend": # Prepend an element 
            self.hide_entry_fields(var)
            self.fix_input_labels(var)
            self.btn.configure(text=var, command=self.executePrepend)

        elif var == "InsertAt": # Insert an element at given position
            self.hide_entry_fields(var)
            self.fix_input_labels(var)
            self.btn.configure(text=var, command=self.executeInsertAt)

        elif var == "Remove": # Remove an element 
            self.hide_entry_fields(var)
            self.fix_input_labels(var)
            self.btn.configure(text=var, command=self.executeRemove)

        elif var == "RemoveAt": # Remove an element at a given position 
            self.hide_entry_fields(var)
            self.fix_input_labels(var)
            self.btn.configure(text=var, command=self.executeRemoveAt)

        elif var == "Predecessor": # Find predecessor of an element 
            self.hide_entry_fields(var)
            self.fix_input_labels(var)
            self.btn.configure(text=var, command=self.executePredecessor)

        elif var == "Successor": # Find successor of an element 
            self.hide_entry_fields(var)
            self.fix_input_labels(var)
            self.btn.configure(text=var, command=self.executeSuccessor)

        elif var == "Search": # Searches for an element 
            self.hide_entry_fields(var)
            self.fix_input_labels(var)
            self.btn.configure(text=var, command=self.executeSearch)

        elif var == "First": # Find the first element
            self.hide_entry_fields(var)
            self.btn.configure(text=var, command=self.executeFirst)

        elif var == "Last": # Find the last element
            self.hide_entry_fields(var)
            self.btn.configure(text=var, command=self.executeLast)

        elif var == "Print": # Print the linked list
            self.hide_entry_fields(var)
            self.btn.configure(text=var, command=self.executePrintList)

        elif var == "Instructions": # View the instructions
            self.hide_entry_fields(var)
            self.btn.configure(text=var, command=self.executeDefault)
            self.executeDefault()

        elif var == "Reverse": # View the instructions
            self.hide_entry_fields(var)
            self.hide_labels()
            self.btn.configure(text=var,  command=self.executeReverse)

    # All execute methods remain unchanged

    def executeReverse(self):
        title = "Original list"
        self.executePrint(title) # Print the original list

        title = "Reverse List"
        self.L.reverse()
        self.executeReversePrint(title) # Print the reverse list

    def executeInsertAt(self):
        var = self.data_entry.get()
        var1 = self.second_data_entry.get()
        if self.L.isEmpty(): 
            title = "Invalid index " + var + " for empty list"
            if int(var1) != 1:
                self.executePrint(title)
            else:
                title = "Inserted " + var + " at position " + var1 + "\n"
                self.executePrint(title)
        if int(var1) > self.L.length() or  int(var1) < 1:
            title = "Invalid index " + var1
            self.executePrint(title)
        else:
            self.L.insertAt(var, int(var1))
            title = "Inserted " + var + " at position " + var1 + "\n"
            self.executePrint(title)

    def executeAppend(self):
        var = self.data_entry.get()
        self.L.append(var)
        title = "Appended " + var + "\n"
        self.executePrint(title)

    def executePrepend(self):
        var = self.data_entry.get()
        self.L.prepend(var)
        title = "Prepended " + var + "\n"
        self.executePrint(title)

    def executeRemove(self):
        var = self.data_entry.get()
        if self.L.getPosition(var) == -1:
            title = "Empty list or " + var + " not found \n"
            self.lb.config(text=title)
        else:
            self.L.delete(var)
            title = "Removed " + var + "\n"
            self.executePrint(title)

    def executeRemoveAt(self):
        var = self.data_entry.get()
        self.L.deleteAt(int(var))
        title = "Removed element at index " + var + "\n"
        self.executePrint(title)

    def executeAppend(self):
        var = self.data_entry.get()
        self.L.append(var)
        title = "Appended " + var + "\n"
        self.executePrint(title)

    def executePredecessor(self):
        var = self.data_entry.get()
        result = self.L.predecessor(var)
        if result == -1:
            title = var + " not in the list"
        elif result == 1:
            title = "First has no predecessor\n"
        else:
            pred = self.L.getValue(result-1)
            title = "Predecessor of " + var + " is " + str(pred) + "\n"
        self.executePrint(title)

    def executeSuccessor(self):
        var = self.data_entry.get()
        result = self.L.successor(var)
        if result == -1:
            title = var + " not in the list"
        elif result == self.L.length(): 
            title = "Last element has no successor\n"
        else:
            succ = self.L.getValue(result+1)
            title = "Successor of " + var + " is " + str(succ) + "\n"
        self.executePrint(title)

    def executeSearch(self):
        var = self.data_entry.get()
        result = self.L.search(var)
        if result != -1:
            title = var + " is at index " + str(result) + " of list\n"  
            self.executePrint(title)
        else:
            title = var + " is not in the list\n"  
            self.executePrint(title)

    def executeFirst(self):
        result = self.L.getFirst()
        title = "First element is " + str(result) + "\n"
        self.executePrint(title)

    def executeLast(self):
        result = self.L.getLast()
        title = "Last element is " + str(result) + "\n"
        self.executePrint(title)

    def executePrintList(self):
        title = "Printing List\n"
        self.executePrint(title) 

    def executePrint(self, var):
        self.lb.config(text=var)
        self.llb.config(text=self.L.printList() + "\n")
        self.lb.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.llb.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.data_entry.delete(0, tk.END)
        if self.second_data_entry.winfo_ismapped():
            self.second_data_entry.delete(0, tk.END)

    def executeReversePrint(self, var):
        self.lb1.config(text=var)
        self.llb1.config(text=self.L.printList() + "\n")
        self.lb1.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        self.llb1.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

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
        menu.add_cascade(label="Insert", menu=subList1)
        menu.add_cascade(label="Delete", menu=subList2)

        subList1.add_command(label="Append", 
                command=lambda: self.widgets.execute_btn("Append"))
        subList1.add_command(label="Prepend", 
                command=lambda: self.widgets.execute_btn("Prepend"))
        subList1.add_command(label="InsertAt", 
                command=lambda: self.widgets.execute_btn("InsertAt"))
        subList2.add_command(label="Remove", 
                command=lambda: self.widgets.execute_btn("Remove"))
        subList2.add_command(label="RemoveAt", 
                command=lambda: self.widgets.execute_btn("RemoveAt"))
        subList2.add_command(label="Reverse", 
                command=lambda: self.widgets.execute_btn("Reverse"))

        # Second dropdown menu
        var1 = tk.StringVar()
        optionMenu1 = ttk.OptionMenu(self.widgets.toggle_menu_frame, var1, 
                "Accessor")
        optionMenu1.pack(pady=20)

        menu1 = optionMenu1['menu']
        subList3 = tk.Menu(menu1, tearoff=False)
        subList4 = tk.Menu(menu1, tearoff=False)
        subList5 = tk.Menu(menu1, tearoff=False)
        menu1.add_cascade(label="Position", menu=subList3)
        menu1.add_cascade(label="Values", menu=subList4)
        menu1.add_cascade(label="Rest", menu=subList5)

        subList3.add_command(label="Predecessor", 
                command=lambda: self.widgets.execute_btn("Predecessor"))
        subList3.add_command(label="Successor",
                command=lambda: self.widgets.execute_btn("Successor"))
        subList3.add_command(label="Search",
                command=lambda: self.widgets.execute_btn("Search"))
        subList4.add_command(label="First", 
                command=lambda: self.widgets.execute_btn("First"))
        subList4.add_command(label="Last", 
                command=lambda: self.widgets.execute_btn("Last"))
        subList5.add_command(label="Print", 
                command=lambda: self.widgets.execute_btn("Print"))
        subList5.add_command(label="Instructions", 
                command=lambda: self.widgets.execute_btn("Instructions"))

if __name__ == '__main__':
    App()

