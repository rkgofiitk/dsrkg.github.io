import ctypes

# Stack implementation using dynamic array

MAXSIZE = 10 
def addOne(i):
    return (i + 1) % MAXSIZE

class Queue(object):

    SIZE = MAXSIZE

    def __init__(self):
        self._front = 0
        self._size = MAXSIZE - 1
        self._rear = self._size 
        self._data = [None] * Queue.SIZE 

    def makenull(self):
        self.__init__()

    def is_empty(self):
        if addOne(self._rear) == self._front:
            return 1
        return 0

    def is_full(self):
        if self._front == addOne(addOne(self._rear)):
            return 1
        return 0

    def __len__(self):
        if self.is_empty():
            return 0
        if self._front > self._rear:
            return (MAXSIZE - self._front + self._front + 1)
        return self._rear - self._front + 1

    def length(self):
        return self.__len__()

    def get_front(self):
        if (self.is_empty()):
            print('Queue is empty') 
            return None 
        return self._data[self._front] 

    def get_rear(self):
        if (self.is_empty()):
            print('Queue is empty') 
            return None 
        return self._data[self._rear] 

    def enqueue(self, ele):
        if self.is_full():
            print("Queue is full: ", ele, " not inserted") 
            return False
        self._rear = addOne(self._rear)
        self._data[self._rear] = ele
        return True
        

    def dequeue(self):
        x = self._data[self._front] 
        self._data[self._front] = None
        self._front = addOne(self._front)
        return x

    def to_list(self):
        prnt = []
        indx = self._front

        if self._data[indx] is not None:
            prnt =[self._data[indx]] 

        while indx != self._rear: 
            indx = addOne(indx)
            if self._data[indx] is not None:
                prnt.append(self._data[indx])
        return prnt

