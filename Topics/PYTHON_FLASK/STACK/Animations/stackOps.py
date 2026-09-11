class Stack:

    def __init__(self):
        self.stack = []
        self.limit = 8

    def is_empty(self):
        return self.stack == [] 

    def is_full(self):
        return len(self.stack) == self.limit 

    def top(self):
        if self.is_empty():
            return [] 
        return self.stack[-1] 

    def pop(self):
        if self.is_empty():
            return
        else:
            return self.stack.pop()

    def push(self, item):
        if self.is_full():
            return 
        self.stack.append(item)

    def size(self):
        return len(self.stack)

    def makenull(self):
        self.__init__() 

    def print(self):
        if self.is_empty():
            return [] 
        else:
            return self.stack

