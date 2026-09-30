---
title: Heap and its Animation
layout: default
---
{% include head-custom.html %}


## Heap and its Animation

A heap, also known as a priority queue, is a binary tree that satisfies the priority queue property. The elements in a heap are ordered by a partial order relation. A partial order relation is characterized by being reflexive, asymmetric, and transitive. The heap property is specified by the elements held at three nodes: a node and its two children. The property should hold at each node in a heap except for the leaves. Heap does not specify any relationship between the siblings and leaves. It means some pairs of elements are not comparable. There are two types of heaps: Max heap and Min heap:
- Max Heap: The value at a node is greater than the values held by its two child nodes.
- Min Heap: The value at a node is greater than the values held by its two child nodes.

The picture below shows an example of a max heap and a min heap. 

| Max Heap Example | Min Heap Example|
|:----- | :-----|
| <img src="images/max_heap.png"> | <img src="images/min_heap.png">|

A heap allows two mutating operations:
- Insert: Allows insertion of a new element and restores the heap property.
- DeletMax: This operation works only in a Max Heap, allowing deletion of the maximum element and restoring the heap property after deletion.
- DeletMin: This operation works only in a Min Heap, allowing deletion of the minimum element and restoring the heap property after deletion.

Creating and maintaining a heap poses two basic challenges:
- Building a heap from a given set of elements.
- Restoring the heap property after an insertion or a deletion.
  
A heap is maintained as a complete binary tree. In a complete binary tree, nodes at all levels of the tree are fully populated except for the last and the level one up. As shown in the examples above, nodes at levels above $i-1$ are fully populated (each with two children). To build a heap, we start with an empty node and insert the elements from a given set one by one. The next element is inserted into the leftmost vacant position on the deepest level, then compared and swapped along the path up towards the root. The new element settles in the position where it can no longer move up the tree path. While moving up the tree, the new node can be involved in 2 compare-swap operations. To understand why?,  consider three elements $a$, $b$, and $c$:
- $a$ is parent, $b$ is an existing child of $a$
- $c$ is the new node being inserted.

Let the relative order of elements be: $c > a$ but $c < b$. In this case, when we move $c$ up and push down $a$ to $c$'s previous position, $c$ also becomes the parent of $b$, replacing $a$. However, as $c < b$, the heap property is not valid at $c$ unless we move $b$ to $c$'s current position. It is possible that $c$ may have to be pushed down the path to a leaf after being pushed to $b$'s previous position. However, the movement of $c$ is limited by the depth of the tree from $b$'s previous position. It means $c$'s movement to its correct position in the heap is limited by the height of the tree representing the heap.  

Since we are building the tree level by level, the total number of compare-and-swap operations can be obtained by knowing:
- Find the number of nodes at each level
- Find the number of levels generated for consuming all elements in the given set.

Only the last level will not be fully occupied. However, for worst-case time complexity, we can assume that the last level is also fully occupied. Assuming $n$ as the cardinality of the initial set of elements, we progress as follows:
- At level 0, there is just $2^0$ node,
- At level 1, there can be at most $2^1$ nodes,
- At level 2, there can be at most $2^2$ nodes, and so on
- In general, at level $i$ at most $2^{i}$, for $0 \le i\le \log n - 1$.

At most 2 compare-and-swap operations may be needed in the worst case when inserting a node. So, while building a heap at height $i$, the worst-case total cost is $2.2^i$ compare-and-swap operations. Summing it over the insertion of all $n$ nodes, the total worst-case cost is

$2 + 2^2 + \ldots + 2.2^{\log n - 1} = 2\left\{\frac{2^{\log n} - 1}{2-1}\right\} \le 2^{\log n} = n$

  

