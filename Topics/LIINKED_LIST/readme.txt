           Readme file for linked list operations
           --------------------------------------

Initially, the program displays a window with two frames:
     - a head frame strip of small width at the top, and
     - a main frame for rest of the window at the bottom 

User can see one single button at the center of main frame.
The button is marked "Instructions".

Clicking it will display this "readme.txt" file describing 
program and the instructions for using the application. 

             Description of the head frame
             -----------------------------

1. It displays an expand icon '≡' to the right end margin of 
   the window. Clicking it expands a side menubar with 
   cascading menus.

2. First set of menu class is for Modifier methods. It
   consists of insert and delete operations on linked list.
   Linked list allows three insert operations: append,
   prepend and insertAt. 

   - Append insert new element at the end of the linked list
     which a user gives in the data entry slot displayed on 
     the main frame.
   - Prepend insert new element at the beginning of the linked list
     which a user gives in the input entry slot displayed on 
     the main frame.
   - InsertAt is slightly different, it brings two data entry
     slots for accepting user's input. The first slot is for
     the element value and second slot is for the position after
     which the value will be inserted.
   - Remove is for removing a given element. The user inputs the
     value in the input slot.
   - RemoveAt removes the element at a given position. The user
     inputs the position in the input slot.

3. The second set of menu class is for accessing different 
   elements of the linked list. It does not change the linked
   list neither the order of elements nor their values. So
   this set of operations are non-mutatinng.

   - Getposition searches the user's input in the linked list.
     If the value exists then it returns the position the 
     element in the linked list.
   - Predecessor accesses the predecessor of an element specified
     by the user as input.
   - Successor accesses the successor of an element specified
     by the user as input.
   - First accesses the first element of the list. It requires
     no input from the user.
   - Last accesses the last element of the list. It requires
     no input from the user.

                  Description of the main frame
                  -----------------------------
 
    Main frame has one button which changes dynamically according
    to the operation that the user may want to perform. After performing
    each opration, it displays message describing the nature of 
    the operation and also the changes in linked list. The output
    displayed is self explanatory.

                  Requirements for executing the program
                  --------------------------------------
    The program requires Python3 programming environment. Should
    be executed in a sandbag virtual environment.

    It requires three files for execution:
      1. readme.txt: this file
      2. linkedListOps.py: Class file specifying linked list operation.
      3. linked_list_gui.py: tkinter Python script code for 
         performing linked list operations as discussed here.

              Button configuration for command execution 
              ------------------------------------------

    The program uses only one command button which is dynamically 
    modified and bound to the selected function for execution.  
    The button's label, placement and command changed each time
    the user clicks on the selected sidebar menu. 

    The main window initially displays "Instructions" button. Clicking
    it displays this file and reverts back by the clicking "Close" 
    button. 

    The function of "Close" button is to delete the text-widget from
    the main window and replace itself by "Instructions" button.

    If any menu is selected from the sidebar menu then corresponding button
    is displayed replacing existing content of the main window.

    We have two sets of cascading menu options. One set is for 
    modifier menu and the other set is accessor.

    Modifier consist of "Append", "Prepend", "InsertAt", "Remove", 
    "RemoveAt".  First three are insert operations and last two are
    delete operations. Except for InsertAt all other functions require
    one input from user. InsertAt requires two inputs: index and value. 
    RemoveAt requires index as input while Prepend, Append, Remove
    require a value.

    For set of accessor menus, we require one value input for 
    "Successor", "Predecessor" and "Search". First and last 
    are fixed indexes respectively retrieving element at 
    the index positon first and index position last. 

    The input field and corresponding label of input field is 
    displayed along with the button for the function execution.

    "InsertAt" requires two inputs: value and the index. All other
    functions "First", "Last", "Print" do no require any input from the
    user. So mapped input fields are removed from the main window
    for these buttons.
