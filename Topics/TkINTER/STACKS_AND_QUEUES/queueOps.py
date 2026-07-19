import ctypes

# Stack implementation using dynamic array

MAXSIZE = 10 
def addOne(i):
    return (i + 1) % MAXSIZE

class QueueArray(object):

    SIZE = MAXSIZE

    def __init__(self):
        self._front = 0
        self._limit = MAXSIZE 
        self._rear = self._limit-1 
        self._data = [None] * QueueArray.SIZE 

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
            l = self._limit-self._front+self._rear +1
            print("here length = ",l) 
            return (self._limit - self._front + self._rear + 1)

        return self._rear - self._front + 1

    def length(self):
        return self.__len__()

    def getFront(self):
        if (self.is_empty()):
            print('Queue is empty') 
            return None 
        return self._data[self._front] 

    def front_index(self):
        return self._front

    def getRear(self):
        if (self.is_empty()):
            print('Queue is empty') 
            return None 
        return self._data[self._rear] 

    def enqueue(self, ele):
        if self.is_full():
            print("Queue is full: " +str(ele)+ " not inserted") 
            return False
        self._rear = addOne(self._rear)
        self._data[self._rear] = ele
        return True 
        

    def dequeue(self):
        if self.is_empty():
            print("Queue is empty, deletion not possible")
            return -999 

        x = self._data[self._front] 
        self._front = addOne(self._front)
        return x

    def to_list(self):
        qlist = [] 
        if self.is_empty():
            return qlist 
        
        indx = self._front
        #print("index = " + str(indx))
        while indx != self._rear: 
            qlist.append(self._data[indx])
            indx = addOne(indx)
            #print("index = " + str(indx))
        qlist.append(self._data[self._rear])
        return qlist 

#q = QueueArray()

#q.enqueue(10)
#q.enqueue(20)
#q.enqueue(30)
#q.enqueue(40)
#q.enqueue(50)
#q.enqueue(60)
#q.enqueue(70)
#q.enqueue(80)
#q.enqueue(90)
#q.enqueue(100)
#print(q.to_list())
#print("length = " , str(q.length()))
#print("front = " , q.front_index())
#q.dequeue()
#q.dequeue()
#q.dequeue()
#print(q.to_list())
#print("length = " , str(q.length()))
#print("front = " , q.front_index()) 
#q.enqueue(110)
#print(q.to_list())
#print("length = " , str(q.length()))
#print("front = " , q._front, "rear = ", q._rear)
#q.enqueue(120)
#print(q.to_list())
#print("length = " , str(q.length()))
#print("front = " , q._front, "rear = ", q._rear)
#print("Size = ",  len(q))
#q.dequeue()
#print("Size:",len(q))
#print(q.to_list())
#
#print(q.to_list())
#q.enqueue(40)
#q.enqueue(50)
#print(q.to_list())
#print("Rear:",q.getRear()," Front:",q.getFront())
#print("Size:",len(q))
#
#q.enqueue(60)
#q.enqueue(70)
#q.enqueue(80)
#q.enqueue(90)
#print(q.to_list())
#q.enqueue(100)
#q.enqueue(110)
#print("Size:",len(q))
#print(q.to_list())
#print("Deleted:", q.dequeue())
#q.enqueue(110)
#print(q.to_list())
#print("Deleted:", q.dequeue())
#print("Deleted:" , q.dequeue())
#print("Rear:",q.getRear()," Front:",q.getFront())
#print("Size:",len(q))

#print("Deleted:" , q.dequeue())
#print("Deleted:" , q.dequeue())
#print("Deleted:" , q.dequeue())
#print("Deleted:" , q.dequeue())
#print("Size:",len(q))
#print(q.to_list())
#print("Rear:",q.getRear()," Front:",q.getFront())

#print("Deleted:", q.dequeue())
#print("Deleted:", q.dequeue())
#print("Deleted:", q.dequeue())
#print("Deleted:", q.dequeue())
#
#print("Rear:",q.getRear()," Front:",q.getFront())
##
#print("Size:",q.length())
#print(q.to_list())
