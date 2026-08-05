# Python program for hashing with chaining
import random
# Constants
CAPACITY = 20
MAX_NODES = 10
SIZE = 10

# Node for linked list
class Node:
    def __init__(self, key: int, val: int):
        self.val = val
        self.key = key
        self.next = None

class List:
    def __init__(self):
        self.head = None
    
    def is_empty(self):
        return self.head is None

    def prepend(self, key: int, val: int):
        new_node = Node(key, val)
        new_node.next = self.head
        self.head = new_node

    def delete(self, key: int, val=None):
        prev, tmp = None, self.head # Set prev to None and tmp to head
        deleted = False # Flag is false initially
        while tmp:
            # Delete all values if val == None and at least one exists 
            if tmp.key == key and (val is None or tmp.val == val):
                deleted = True 
                if prev is None:
                    self.head = tmp.next
                else:
                    prev.next = tmp.next

                if val is not None:  # Delete only one value 
                    return True

                # continue deleting all with same key if val=None
            else:
                prev = tmp
            tmp = tmp.next
        return deleted    

    def find(self, key: int, val=None):
        tmp = self.head
        results = []
        while tmp:
            if tmp.key == key and (val is None or tmp.val == val):
                results.append(tmp) # Append multiple values to result 
            tmp = tmp.next # Check next node in the list 
        return results if results else None # Return None or result

class Hash:
    def __init__(self, size=10, capacity=20):
        self.size = size
        self.capacity = capacity
        self.count = 0
        self.table = [List() for _ in range(self.size)]

    def to_dict(self):
        """Return a JSON-friendly structure of buckets and chains."""
        buckets = []
        for i, bucket in enumerate(self.table):
            chain = []
            tmp = bucket.head
            while tmp:
                chain.append({"key": tmp.key, "val": tmp.val})
                tmp = tmp.next
            buckets.append({"bucket": i, "chain": chain})
        return {"size": self.size, "capacity": self.capacity, "buckets": buckets}


    # Apply hash on key not on value
    def _hash(self, key: int):
        return hash(key) % self.size

    # Value is associated with a key
    def insert(self, key: int, val: int):
        if self.count >= self.capacity:
            print("Limit exceeded, current size", self.count)
            return -1 
        index = self._hash(key)
        print(f"Inserting ({key}, {val}) at bucket {index}")
        self.table[index].prepend(key, val)
        self.count += 1
        return 0 

    def find(self, key: int, val=None):
        index = self._hash(key)
        locs = self.table[index].find(key, val)
        if locs is None:
            return None, index  # not found, but still return bucket index
        else:
            return locs, index

    def delete(self, key: int, val=None):
        index = self._hash(key)
        deleted = self.table[index].delete(key, val)
        if deleted:
            if val is None:
                print("Deleted all values for key", key)
            else:
                print("Deleted pair", (key, val))
            self.count -= 1
            return True
        else:
            print("Element", key, "is absent")
            return False

    def display(self):
        print("\nHash Table Contents:")
        for i, bucket in enumerate(self.table):
            tmp = bucket.head
            chain = []
            while tmp:
                chain.append(f"({tmp.key}:{tmp.val})")
                tmp = tmp.next
            print(f"Bucket {i}:", " -> ".join(chain) if chain else "Empty")

    def collision_count(self):
        """Returns total number collisions"""
        # The formula is total - occupied
        total_items = 0
        occupied = 0
        for bucket in self.table:
            tmp = bucket.head
            if tmp:
                occupied += 1
            while tmp:
                total_items += 1
                tmp = tmp.next
        return total_items - occupied


    def max_chain_length(self):
        """Return the length of the longest chain in any bucket."""
        max_len = 0
        for bucket in self.table:
            tmp, length = bucket.head, 0
            while tmp:
                length += 1
                tmp = tmp.next
            max_len = max(max_len, length)
        return max_len
    
    def average_chain_length(self):
        """Return the average chain length across non-empty buckets."""
        lengths = []
        for bucket in self.table:
            tmp, length = bucket.head, 0
            while tmp:
                length += 1
                tmp = tmp.next
            if length > 0:
                lengths.append(length)
            
            total_elements = sum(lengths)
            average_length = total_elements/len(lengths) if lengths else 0
        return total_elements, average_length 



# Driver code
#if __name__ == "__main__":
    

#    H = Hash()
#    for i in range(10):
#       for j in range(2):
#            H.insert(i+5, i+10)

#    H.delete(11, 16)   # deletes only Alice
#    H.delete(11, 16)   # deletes only Alice
#    H.delete(10, 15)   # deletes only Alice

        
#    H.display()

#    print("collision count = ", H.collision_count())
#    print("maximum chain length = ", H.max_chain_length())
#    print("average chain length = ", H.average_chain_length())

#    H.find(11)          # → Key 1 has values: ['Alice', 'Bob']

#    H.find(11, 11)   # → Pair (1, 'Bob') is present

#    H.delete(1, 10)   # deletes only Alice
#    H.insert(11, 15)
#    H.find(11)              # → Key 1 has values: ['Bob']

#    H.delete(11)            # deletes all values for key 1
#    H.find(11)              # → absent
#    H.display()

