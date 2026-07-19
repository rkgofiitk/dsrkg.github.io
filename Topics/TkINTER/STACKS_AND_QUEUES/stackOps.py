class Stack:

    def __init__(self):
        self.stack = []
        self.limit = 8

    def size(self):
       return len(self.stack)

    def get_stack(self):
       return self.stack 

    def is_empty(self):
        return len(self.stack) == 0

    def is_full(self):
        return len(self.stack) == self.limit 

    def top(self):
        if self.is_empty():
            return None
        return self.stack[-1] 

    def pop(self):
        if self.is_empty():
            print("Pop failed! Stack is empty.")
            return None
        popped_item = self.stack.pop(-1)
        print("Popped:", popped_item, "Remaining Stack:", self.stack)
        return popped_item

    def push(self, item):
        if self.is_full():
            print("Push failed! Stack is full.")
            return False  # Return failure
        self.stack.append(item)
        print("Push successful. Stack:", self.stack)
        return True  # Return success

    def makenull(self):
        self.__init__() 

    def print(self):
        if self.is_empty():
            return "Stack is empty"
        else:
            return self.stack

    def to_list(self):
        """Return a copy of the current stack as a list."""
        return list(self.stack)



