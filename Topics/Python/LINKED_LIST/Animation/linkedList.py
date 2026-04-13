class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head == None

    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def append(self, data):
        if self.head == None:
            self.head = Node(data)
            return

        tmp = self.head
        while tmp.next != None:
            tmp = tmp.next
        new_node = Node(data)
        tmp.next = new_node 

    def delete(self, data):
        #if self.head == None:
        #    return None 

        prev = None 
        tmp = self.head

        while tmp.data != data and tmp.next != None:
            prev = tmp
            tmp = tmp.next
        if tmp.data == data:
            if prev == None:
                self.head = tmp.next 
            else:
                prev.next = tmp.next
            return  True

        return False



    def insert_after(self,data1, data2):
        print("data1 = ", data1, "data2 = ", data2)
        if self.head == None:
            return

        tmp = self.head
        while tmp.data != data1 and tmp.next != None:
            tmp = tmp.next

        if tmp.data == data1:
            new_node = Node(data2)
            new_node.next = tmp.next
            tmp.next = new_node

    def get_list_data(self):
        elements = []
        curr = self.head
        while curr:
            elements.append(curr.data)
            curr = curr.next
        return elements

    def print_list_data(self):
        print("List data = ", self.get_list_data())

    def reverse(self):
        prev = None
        curr = self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    def sort(self):
        # naive sort: collect, sort, rebuild
        elements = self.get_list_data()
        elements.sort()
        # rebuild linked list
        self.head = None
        for val in reversed(elements):
            new_node = Node(val)
            new_node.next = self.head
            self.head = new_node

    def length(self):

        return (len(self.get_list_data()))


#L = LinkedList()
#L.append(10)
#L.append(20)
#L.append(30)
#L.append(40)
#L.append(50)

#L.print_list_data()

#print(L.delete(10))
#print(L.delete(90))

#L.print_list_data()
