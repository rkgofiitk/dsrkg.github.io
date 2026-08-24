# Python program for hashing with open addressing 

class HashTable:
    def __init__(self, size=10, crm = 0):
        self.size = size
        self.table = [None] * self.size
        self.deleted = "<deleted>" 
        self.crm = crm # Collision resolution: 0 -> linear, nonzero for quadratic

    def _hash(self, key):
        return hash(key) % self.size 

    def is_empty(self, index):
        # Vacant slot either marked empty or deleted
        return self.table[index] is None or self.table[index] == self.deleted





    def linear_resolution(self, key, value):
        first_deleted = None
        idx = self._hash(key)
        probes = []

        for i in range(self.size):
            probes.append(idx)

            if self.table[idx] is None:
                target = first_deleted if first_deleted is not None else idx
                return probes, target

            if self.table[idx] == self.deleted:
                if first_deleted is None:
                    first_deleted = idx

            elif self.table[idx][0] == key:
                # Found existing key → overwrite
                return probes, idx

            idx = (idx + 1) % self.size

        # If no empty slot found, reuse first_deleted if available
        if first_deleted is not None:
            return probes, first_deleted

        return probes, None


    def quadratic_resolution(self, key, value):
        first_deleted = None
        idx = self._hash(key)
        probes = []

        for i in range(self.size):
            new_idx = (idx + i**2) % self.size
            probes.append(new_idx)

            if self.table[new_idx] is None:
                target = first_deleted if first_deleted is not None else new_idx
                return probes, target

            if self.table[new_idx] == self.deleted:
                if first_deleted is None:
                    first_deleted = new_idx

            elif self.table[new_idx][0] == key:
                # Found existing key → overwrite
                return probes, new_idx

        if first_deleted is not None:
            return probes, first_deleted

        return probes, None


    def get(self, key):
        idx, _ = self.find(key)
        return None if idx is None else (idx, self.table[idx][1])

    def find_linear(self, key):
        idx = self._hash(key)
        probes = []

        for i in range(self.size):
            probes.append(idx)
            if self.table[idx] is None:
                return None, probes
            if self.table[idx] != self.deleted and self.table[idx][0] == key:
                return idx, probes
            idx = (idx + 1) % self.size

        return None, probes
    

    def find_quadratic(self, key):
        idx = self._hash(key)
        probes = []

        for i in range(self.size):
            new_idx = (idx + i**2) % self.size
            probes.append(new_idx)

            if self.table[new_idx] is None:
                return None, probes
            if self.table[new_idx] != self.deleted and self.table[new_idx][0] == key:
                return new_idx, probes

        return None, probes
    
    def insert(self, key, value):

        if self.crm == 0: # Linear resolution
            probes, idx = self.linear_resolution(key, value)
            print(probes)
        else: # Quadratic resolution
            probes, idx = self.quadratic_resolution(key, value)
            print(probes)

        if idx is not None: 
            # Always write into the returned slot
            self.table[idx] = (key, value)
            return True
        else:
            #print("insertion unsuccessful") # debug statement
            return False


    def delete(self, key):
        idx, probes = self.find(key)
        if idx is not None:
            val_deleted = self.table[idx]
            self.table[idx] = self.deleted
            print("index = ", idx)
            return True, probes, idx, val_deleted
        return False, probes, None, None


    def find(self, key):
        if self.crm == 0:
            return self.find_linear(key)
        else:
            return self.find_quadratic(key)
    
    
    def to_dict(self):
        result = []
        for i, slot in enumerate(self.table):
            if slot is None:
                result.append({"index": i, "status": "empty"})
            elif slot == self.deleted:
                result.append({"index": i, "status": "deleted"})
            else:
                k, v = slot
                result.append({"index": i, "status": "filled", "key": k, "value": v})
        return result
    

    def display(self):
        my_dict = self.to_dict()
        for i, key in enumerate(my_dict):
            print(i, key)


# Uncomment driver code to debug
   
#if __name__ == "__main__":
#    H = HashTable(10)
#    index = H._hash(10)
#    if H.is_empty(index):
#        print("index postion is empty")
#    else:
#        print("index postion is occupied")


#    H.insert(10, "Data0")
#    H.insert(1, "Data1")
#    H.insert(12, "Data2")
#    H.insert(13, "Data3")
#    H.insert(14, "Data4")
#    H.insert(15, "Data5")
#    H.insert(16, "Data6")
#    H.insert(10, "Changed data")
#    H.insert(17, "Data7")
#    H.insert(18, "Data8")
#    H.insert(19, "Data9")

#    H.insert(22, "Data_new")
#    
#    index = H._hash(22)
#    if H.is_empty(index):
#        print("index postion is empty")
#    else:
#        print("index postion is occupied")



#    print("index postion is ", H.is_empty(H._hash(1)))
#
#    print(H.find(20))
       
#    H.display() 

    #print("collision count = ", H.collision_count())
    #print("maximum chain length = ", H.max_chain_length())
    #print("average chain length = ", H.average_chain_length())

#    H.find(11)          # → Key 1 has values: ['Alice', 'Bob']
#

#    success, probes, index, deleted_val = H.delete(1)   # deletes only Alice
#    if success:
#        print(f"Deleted {deleted_val} at table index {index} with {probes} probes")
#    else:
#        print("No entries found for key 1")

#    H.insert(11, 15)
#
#    H.find(11)              # → Key 1 has values: ['Bob']

#    success, probes, index, deleted_val = H.delete(10)  
#    if success:
#        print(f"Deleted {deleted_val} at table index {index} with {probes} probes")
#    else:
#        print("No entries found for key 11")

#    success, probes, index, deleted_val = H.delete(20) 
#    if success:
#        print(f"Deleted {deleted_val} at table index {index} with {probes} probes")
#    else:
#        print("No entries found for key 24")

#    print("\nDisplay after three deletions\n")
#    H.display()


    #H.insert(30, "Data5")
   # print("\nDisplay after one insertion\n")
    #H.find(11)              # → absent
   # H.display()

