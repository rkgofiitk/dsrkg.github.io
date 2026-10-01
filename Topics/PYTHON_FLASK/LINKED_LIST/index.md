---
title: Animation of Operations on Linked List
layout: default
---
{% include head-custom.html %}

## Animation of Operations on Linked List

A linked list is a linear list that stores each element in an indivisible structure called a node that has two fields: information and a link. The information field contains the item of data or the element, while the link contains the address of the next node. A linked list has a special address called the head that can access the first node. If we have access to the head node of the list, we can access the successive elements from the first node by the link field.  The link field of a node is typically referred to as next because it points to the next element in the list order. The image below depicts a node and a linked list. 

| Node | Linked list|
|:-----|:-----------|
|<img src="images/node_of_list.png"> |<img src="images/linked_list.png"> |

A linked list allows insert, delete, and search operations. But the worst-case cost of a search operation is the same as the order of the length of the list. Since a linked list is a linear list, accessing any particular element will require accessing each and every element that precedes the search element from the beginning of the list. However, the cost of an insert or a delete will depend on the element of interest. An insertion may be of three types: Append, Prepend, or Insert after. A prepend inserts the incoming element as the first element. Append on the other hand, insert the incoming element at the end of the list. The cost of a prepend is O(1) because we always have a pointer to the first element of the list. But an append costs us because we have to reach the end of the list to insert the incoming element. So, the cost of an append is O($n$) assuming that the list has $n$ elements. If we maintain a pointer to the end of the list, we can also append in O(1) time. However, insert after (before) is essentially a combination of search and insert. It requires two elements:
- Element to be inserted, say $E_{new}$
- Element, say $E_{aft}$. specifying the position in the list after which the new element should be inserted.

The following possibilities exist, depending on $E_a$ and $E_{new}$.
- If $E_{aft}$ is the last element, then the new element $E_{new}$ must be appended.
- If $E_{aft}$ does not exist in the list, then the insertion should generate an error.
- If $E_{aft}$ exists in the list between the 1st and the element before the last, then locate $E_{aft}$ and insert $E_{new}$ as the next element.
