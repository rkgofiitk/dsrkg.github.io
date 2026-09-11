# Python program for hashing with chaining
# Constants

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size
        self.deleted = object()

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value, col=0):
        if col == 0:
            success, probes = self.linear_resolution(key, value)
        else:
            success, probes = self.quadratic_resolution(key, value)

        return {
            "success": success,
            "table": self.to_dict(),
            "probes": probes
        }
    

    def quadratic_resolution(self, key, value):
        first_deleted = None
        idx = self._hash(key)
        probes = []

        for i in range(self.size):
            new_idx = (idx + i**2) % self.size
            probes.append(new_idx)

            if self.table[new_idx] is None:
                target = first_deleted if first_deleted is not None else new_idx
                self.table[target] = (key, value)
                return True, probes

            if self.table[new_idx] == self.deleted:
                if first_deleted is None:
                    first_deleted = new_idx

            elif self.table[new_idx][0] == key:
                self.table[new_idx] = (key, value)
                return True, probes

        return False, probes


    def linear_resolution(self, key, value):
        first_deleted = None
        idx = self._hash(key)
        probes = []

        for i in range(self.size):
            probes.append(idx)

            if self.table[idx] is None:
                target = first_deleted if first_deleted is not None else idx
                self.table[target] = (key, value)
                return True, probes

            if self.table[idx] == self.deleted:
                if first_deleted is None:
                    first_deleted = idx

            elif self.table[idx][0] == key:
                self.table[idx] = (key, value)  # update existing
                return True, probes

            idx = (idx + 1) % self.size

        return False, probes
    
    

    def get(self, key):
        index = self._hash(key)
        for _ in range(self.size):
            if self.table[index] is None:
                return None  # Key not found
            if self.table[index] != self.deleted and self.table[index][0] == key:
                return index, self.table[index][1]
            index = (index + 1) % self.size
        return None

    def find_linear(self, key, val):
        idx = self._hash(key)
        probes = []

        for i in range(self.size):
            probes.append(idx)
            if self.table[idx] is None:
                return None, probes
            if self.table[idx] != self.deleted and \
               self.table[idx][0] == key and self.table[idx][1] == val:
                return idx, probes
            idx = (idx + 1) % self.size

        return None, probes


    def find_quadratic(self, key, val):
        idx = self._hash(key)
        probes = []

        for i in range(self.size):
            new_idx = (idx + i**2) % self.size
            probes.append(new_idx)
            if self.table[new_idx] is None:
                return None, probes
            if self.table[new_idx] != self.deleted and \
               self.table[new_idx][0] == key and self.table[new_idx][1] == val:
                return new_idx, probes

        return None, probes


    def delete(self, key, val, col=0):
        idx, probes = self.find(key, val, col)
        if idx is not None:
            self.table[idx] = self.deleted
            return True, probes, idx
        return False, probes, None

    def find(self, key, val, cr=0):
        if cr != 0:
            return self.find_quadratic(key, val)
        else:
            return self.find_linear(key, val)
    

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
    
    


#H = HashTable(size=5)
#print(H.insert("A", 1, 0))   # expect True
#print(H.table)               # should show ("A",1) in some slot

   
#if __name__ == "__main__":
# Driver code
#    H = HashTable()
#    H.insert(10, "Data1", 1)
#    H.insert(17, "Data2", 1)
#    H.insert(24, "Data3", 1)
#    print(H.to_dict())
#    print(H.find(24, "Data3", 1))
#    print(H.find(24, "Data1", 1))
#    for i in range(10):
#        for j in range(2):
#            H.insert(i+5, i+10)
        
#    H.display()

#    print("collision count = ", H.collision_count())
#    print("maximum chain length = ", H.max_chain_length())
#    print("average chain length = ", H.average_chain_length())

#    H.find(11)          # → Key 1 has values: ['Alice', 'Bob']
#
#    H.find(11, 11)   # → Pair (1, 'Bob') is present

#    H.delete(1, 10)   # deletes only Alice
#    H.insert(11, 15)
#    H.find(11)              # → Key 1 has values: ['Bob']

#    H.delete(11)            # deletes all values for key 1
#    H.find(11)              # → absent
#    H.display()

