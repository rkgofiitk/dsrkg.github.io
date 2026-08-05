## Chain Hashing

Hashing is a faster method to store, retrieve and search data compared to more structured way of storing data. A hash table is a table of fixed size. Its operations use a simple mathematical function called hash function. The hash function maps an incoming data to an index of the hash table. Insert, delete, or search operations are performed on the table entry corresponding to the hash value. There are two types of hash tables:
- Chaining: It is basically a table of pointer where each pointer give a chain or linked list of data that have same hash value.
- Open addressing: Use a fixed sized table where data items are directly stored in the hash table.

Typically, hashing is used for storring values from a large universe. It means that fixed sized table may run out of space and require expansion of the table, especially, in the case of open addressing. We will deal with open addressing separately. However, in the case of chaining the chain length may lead to time consuming operations. Therefore, we need also to expand the table. However, only a small subset of values of the universe form the set of data being operated implying that average length will be a constant. Therefore, an operation on a hash table takes O(1) time in average.  

The directory contains two python files. 
- hash_class.py; Backend code for hash operations
- animate_hash.py: Frontend code for animation of the hash operation.

We did not provide a pdf file which the program requires. The reader can create their specific files appropriate for the code.
