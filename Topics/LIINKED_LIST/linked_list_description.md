# Linked List

Linked list consists of finite number of objects where each object is represented by a node. The object may be as simple as an integer,
float or character or as complex as a student record with multiple fields like roll, name, age, grades. There is an explicit sequencing 
of objects represented by a linked list. Each node of a linked list has at least two fields: info and
next as in the figure below. 

<p style=align:"center">
 <img src="./header_node.pdf">
</p>

The <b>info</b> field stores the object, while <p>next</p> is a pointer to the node that represents the successor object. We can 
access the objects of linked list only from the beginning of the list. It essentially means we have a pointer only to head or the first
node. To access a node in the middle of a linked list then we must navigate the list following the next pointer starting from the 
beginning or the first node. In other words, a linked list allows ordered access to the objects sequentially starting at the first
object. We may not know eactly how many objects are stored in a linked list. It means, we need to have a way of detecting the last 
object or node in a linked list. Most programming language provisions for definine a field as <p>None</p> or a <p>NULL</p>. If a
pointer field is assigne <p>None</p> in Python then it cannot lead to a valid node. Therefore, the end of a linked list is reached
when a node's next field is <p>None</p>.

    I defined linear data structure for accessing, modifying, and storing objects.  Every object has a successor 
