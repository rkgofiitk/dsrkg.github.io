# Node class
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Linked list class
class LinkedList:
    def __init__(self):
        self.head = None

    # Returns a null linked list
    def makeEmpty(self):
        return self.__init__()

    # Retutns true if linked list is empty
    def isEmpty(self):
        return self.head == None

    # Returns a pointer to the last node if list nonempty
    # Returns None if list is empty
    def end(self):
        if self.isEmpty():
            return None
        curr = self.head
        while curr.next != None:
            curr = curr.next
        return curr

    # Returns a pointer to the first node if list nonempty
    # Returns None if list is empty
    def first(self):
        if self.isEmpty():
            return None
        else:
            return self.head


    # Returns the item value given a valid position  
    # Otherwise returns None
    def getValue(self,pos):
        cnt = 1
        curr = self.head
        while curr is not None:  
            if cnt == pos:
                return curr.data
            else:
                curr = curr.next
                cnt += 1
        return None    

    # Returns position of the item if it present
    # Otherwise returns -1
    def getPosition(self, val):
        cnt = 1
        if self.isEmpty():
            return -1 
        curr = self.head
        while curr is not None:
            if curr.data == val:
                return cnt
            else:
                cnt += 1
                curr = curr.next
        return -1 

    # Returns item value in the last node if list is nonempty
    # Otherwise returns None
    def getLast(self):
        if self.end() != None:
            return self.end().data
        else:
            return self.end() 

    # Returns item value in the first node if list is nonempty
    # Otherwise returns None
    def getFirst(self):
        if self.first() != None:
            return self.head.data 
        else:
            return self.first

    # Returns length or the number of nodes in the linked list
    def length(self):
        len = 0
        curr = self.head
        while curr != None:
            len += 1
            curr = curr.next
        return len

    # Returns Found or not found
    def search(self, item):
        return self.getPosition(item)

    # Find successor 
    def successor(self, item):
        return self.getPosition(item)
        
        #if pos == -1:
        #    return pos  
        #if item == self.end().data:
        #    return "last"
        #else:
        #    return self.getValue(pos+1) 

    # Find predecessor 
    def predecessor(self, item):
        return self.getPosition(item) 
#        if post == -1:
#            return "not in the list"
#        if pos == 1:
#            return "first"
#        return self.getValue(pos-1)

    # Returns the string of elements representing the list
    def printList(self):
        if self.isEmpty():
            return "head -> None (List is empty)"
        lstring = "head -> "
        temp = self.head
        cnt = -1
        ln = 1 
        while(temp.next):
            cnt += 1
            ln += 1
            if cnt == 6:
                lstring += "\n        "
                cnt = 0
            lstring += str(temp.data) + " -> "
            temp = temp.next
        lstring += str(temp.data) + "-> None\n" 

        lstring += "List has " + str(ln) + " elements"  
        return lstring


    # Inserts a new node at the beginning of the list
    def prepend(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node
        return 

    # Inserts a new node at the end of the list 
    def append(self, new_val):
        new_node = Node(new_val)

        if self.isEmpty():
            self.head = new_node
            return
        last = self.end()
        last.next = new_node
        return

    # Returns the list inserting item after given value val. 
    # if val is present. Otherwise returns the original list
    def insertAt(self, new_val, pos):

        # Insertion is possible if pos belongs to range [1, end] 
        if pos == 0 or pos > self.length()+1:
            print("position does not exist")
            return

        # For empty list insertion possible only at pos = 1
        if self.isEmpty():
            if pos == 1:
                self.prepend(new_val)
                return 
            else:
                return

        # Insertion for nonempty list 
        if pos == self.length()+1:
            # insert at end if pos = end+1
            self.append(new_val)
            return
        if pos == 1:
            # insert at beginning if pos=1 
            self.prepend(new_val)
            return
          
        # Find the position where insertion will take place
        cnt=1 # Initialize position count
        prev = self.head # Previous navigation ptr 
        curr = self.head # Current navigation ptr
        while curr is not None:
            if cnt == pos: # Check if position reached
                new_node = Node(new_val)  
                new_node.next = curr
                prev.next = new_node
                return 
            else: # Continue to advance navigation ptrs
                cnt += 1
                prev = curr 
                curr = curr.next
        
    # Returns list inserting a new value after an existing 
    # value in the list if it exists
    def insertAfter(self, val, new_val):
        pos = self.getPosition(val)
        self.insertAt(new_val, pos+1)

        return

    # Returns list inserting a new value before an existing 
    # value in the list if it exists
    def insertBefore(self, val, new_val):
        pos = self.getPosition(val)
        self.insertAt(new_val, pos+1)

        return


    # Returns list inserting multiple inputs at one go
    # it is convenient for experimenting accessor functions
    def multipleInserts(self, my_list):

        for index,my_list in enumerate(my_list):
            self.append(my_list)
        return


    # Returns list deleting an element at a given
    # valid positions, returns an error otherwise
    def deleteAt(self,pos):

        if pos < 1 or pos > self.length():
            return

        if pos == 1:
            self.head = self.head.next
            return

        cnt = 1
        curr = self.head 
        while curr is not None:
            if cnt == pos - 1:
                curr.next = curr.next.next
                return
            cnt += 1
            curr = curr.next
        return

    # Returns the list after deletion, if the element exists 
    # in the list, otherwise returns the original list
    def delete(self,val):

        pos = self.getPosition(val)
        self.deleteAt(pos)

        return 


    # Returns the string for reverse of the linked list
    def reverse(self):
        prev = None
        curr = self.head

        if self.isEmpty() or self.length() == 1:
            return

        while curr is not None:
            succ = curr.next
            curr.next = prev
            prev = curr
            curr = succ

        self.head = prev 
        return

#ll = LinkedList()
#ll.multipleInserts(['a','b','c','d','e'])
#print(ll.search('d'))
#print(ll.search('f'))
#print(ll.search('e'))
#print(ll.search('a'))
#ll.insertAt('f', 5)
#print(ll.printList())
#ll.append(20)
#ll.append(30)
#ll.append(40)
#ll.append(50)
#ll.append(60)
#ll.append(70)
#print(ll.printList())
#ll.reverse()

